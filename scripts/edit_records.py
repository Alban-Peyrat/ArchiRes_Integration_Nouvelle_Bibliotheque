# -*- coding: utf-8 -*- 

# external imports
import re
import pymarc
import dotenv
import os
import logging
import datetime
import pandas as pd
from enum import Enum

# internal imports
import logs
import archires_coding_convention_resources as accr

# Load paramaeters
dotenv.load_dotenv()
FILE_IN = os.getenv("EDIT_RECORDS_FILE_IN")
FILE_OUT = os.path.dirname(FILE_IN) + "/RECORDS_FOR_KOHA.mrc"
FILE_ERRORS = os.path.dirname(FILE_IN) + "/edit_records_errors.csv"
FILE_MAPPING_IDS = os.getenv("EDIT_RECORDS_IDS_MAPPING_FILE")
ORIGIN_ID_NAME = os.getenv("EDIT_RECORDS_ORIGIN_ID_NAME")
LOGS_PATH = os.getenv("LOGS_FOLDER")
LOGGER_LEVEL = accr.define_logger_level(os.getenv("LOGGER_LEVEL"))

# ----------------- Mappings -----------------
class Errors(Enum):
    CHUNK_ERR = "Chunk error : check logs"
    NO_ORIGIN_ID_IN_RECORD = f"No {ORIGIN_ID_NAME} in the record"
    TOO_MUCH_ORIGIN_ID_IN_LIST = f"{ORIGIN_ID_NAME} matched multiple lines in provided list"
    NO_ORIGIN_ID_IN_LIST = f"{ORIGIN_ID_NAME} was not found in provided list"
    TOO_MUCH_BIBNB_FOR_ID = f"Multiples biblionumbers provided for this {ORIGIN_ID_NAME}"
    MATCH_IS_NOT_A_BIBNB = f"Something is mapped to this {ORIGIN_ID_NAME} but it's not a biblionumber"
    NO_DOCTYPE = "Item has no doctype"
    ITEM_TYPEDOC_NOT_MAPPED = "Item TYPEDOC is not mapped"
    ITEM_ITEMTYPE_NOT_MAPPED = "Item itemtype is not mapped"

TYPEDOC_mapping = {
    "DOCMUL":"MULT",
    "LIVRE":"LIV",
    "PERI":"REV",
    "THESE":"TE",
    "LIV":"LIV",
    "DVD":"AUDIOV"
    }

itemtype_mapping = {
    "DOCMUL":"LIV",
    "LIVRE":"LIV",
    "PERI":"REV",
    "THESE":"TE",
    "LIV":"LIV"
}

# ----------------- Functions definition -----------------

def show_datafield(field):
    """Returns the field as a string because pymarc doesn't work"""
    output =  field.tag + " " + "".join(field.indicators)
    for index, str in enumerate(field.subfields):
        # On even, is the subfield code
        if index % 2 == 0:
            output += "$" + str
        else:
            output += str            
    return output

def add_subfield(field, code, value):
    """Adds the subfield to provided field or replace existing subfield"""
    if (field[code]):
        field[code] = value
    else:
        field.add_subfield(code, value)

def generate_error(err: Errors, logger: logging, f, index: int, id="", additional_info=None):
    """Logs an error and write it to the error file.
    Takes as argument :
        - err {Errors entry}
        - logger : the logger
        - f : the error file
        - index : the record index
        - [optional] id : the record id if it is accessible """
    last = ""
    if additional_info:
        last = " : " + str(additional_info)
    logger.error(f"{err.value}{last}")
    f.write(f"{index};{id};{err.value}{last}\n")


# ----------------- Preparing Main -----------------

# Open in and out files
# BINARY is mandatory for MARC files
MRC_READER = pymarc.MARCReader(open(FILE_IN, 'rb'), to_unicode=True, force_utf8=True) # DON'T FORGET ME
MRC_WRITER = open(FILE_OUT, "wb") # DON'T FORGET ME
F_ERRORS = open(FILE_ERRORS, "w", encoding="utf-8") # DON'T FORGET ME
df = pd.read_csv(FILE_MAPPING_IDS, sep=";", usecols=[ORIGIN_ID_NAME, "bibnb"], dtype={ORIGIN_ID_NAME: str, "bibnb": str})

# Init logger
service = "ThisProject_Edit_Records"
logs.init_logs(LOGS_PATH, service,'DEBUG')
logger = logging.getLogger(service)

# ----------------- Main -----------------

logger.info("Starting main function...")

F_ERRORS.write(f"record_nb;{ORIGIN_ID_NAME};error\n")

# Generate fixed fields
# Adds a new 801
field_801 = pymarc.field.Field(tag="801", indicators=[" ", "3"])
field_801.add_subfield("9", "ThisProject_import")
field_801.add_subfield("b", "DBNAME")
logger.info(f"Field created : {show_datafield(field_801)}")

# Date
today = datetime.date.today().strftime('%Y-%m-%d')
logger.info(f"Date : {today}")

# Loop through records
for index, record in enumerate(MRC_READER):
    logger.info(f"--- Starting Record {index}")
    err = None

    # If record is invalid
    if record is None:
        logger.error(f"Current chunk: {MRC_READER.current_chunk} was ignored because the following exception raised: {MRC_READER.current_exception}")
        F_ERRORS.write(f"{index};;{Errors.CHUNK_ERR.value}\n")
        continue

    logger.debug("Record is valid")
    
    # ---------- Record ----------
    origin_id = None
    if record["001"]:
        origin_id = record["001"].data
    if not origin_id:
        generate_error(Errors.NO_ORIGIN_ID_IN_RECORD, logger, F_ERRORS, index)
        continue

    edit_record = True
    # Checks if a bibnb is provided for this PPN
    if (record["001"]):
        logger.debug(f"ID : {record['001'].data}")
        matched_rows = df.loc[df[ORIGIN_ID_NAME] == record['001'].data]
        #Multiple match in the file, leaves
        if len(matched_rows) > 1:
            generate_error(Errors.TOO_MUCH_ORIGIN_ID_IN_LIST, logger, F_ERRORS, index, origin_id)
            continue
        elif len(matched_rows) == 0:
            generate_error(Errors.NO_ORIGIN_ID_IN_LIST, logger, F_ERRORS, index, origin_id)
            continue

        # PPN was found in the list, has at least a bibnb
        if not pd.isna(matched_rows["bibnb"].iloc[0]):
            if len(matched_rows["bibnb"].iloc[0].split(",")) > 1:
                generate_error(Errors.TOO_MUCH_BIBNB_FOR_ID, logger, F_ERRORS, index, origin_id)
                continue

            # No number in the data
            match = re.search("\d+", matched_rows["bibnb"].iloc[0])
            if not match:
                generate_error(Errors.MATCH_IS_NOT_A_BIBNB, logger, F_ERRORS, index, origin_id)
                continue
            
            # We can edit the record
            bibnb = match.group()
            logger.debug(f"Biblionumber successfully found : {bibnb}") #errors['cell_nan']
            edit_record = False
    
    if not edit_record:
        record["001"].data = bibnb
    else:
        # Deletes fields
        record.remove_fields("001")
        record.remove_fields("090")
        record.remove_fields("610")
        record.remove_fields("098")
        
        # Adds a new 801
        record.add_field(field_801)

        # Edit 099
        for field in record.get_fields("099"):
            # Last Sudoc import
            field.delete_subfield("e")
            
            # Koha creation date
            add_subfield(field, "c", today)
            
            # Koha last edit date
            add_subfield(field, "d", today)
            
            # Converts item typedoc to record typedoc
            if (field["t"]):
                field.delete_subfield("t")
            for item in record.get_fields("995"):
                if not (item["r"]):
                    generate_error(Errors.NO_DOCTYPE, logger, F_ERRORS, index, origin_id, show_datafield(item))
                    continue
                if (item["r"] in TYPEDOC_mapping):
                    field.add_subfield("t", TYPEDOC_mapping[item["r"]])
                else:
                    generate_error(Errors.ITEM_TYPEDOC_NOT_MAPPED, logger, F_ERRORS, index, origin_id, item['r'])
                    continue
                    
    # ---------- Items ----------
    for item in record.get_fields("995"):
        # Hold type
        if (item["r"] in itemtype_mapping):
            add_subfield(item, "r", itemtype_mapping[item["r"]])
        else:
            generate_error(Errors.ITEM_ITEMTYPE_NOT_MAPPED, logger, F_ERRORS, index, origin_id, item['r'])
            continue
        item.delete_subfield("h")

        # Homebranch
        add_subfield(item, "b", "CODE")

        # Holding branch
        add_subfield(item, "c", "CODE")


        # Delete subfields
        item.delete_subfield("1") # unless this can be somewhere else
        item.delete_subfield("9")
        item.delete_subfield("j")
        item.delete_subfield("n")
        item.delete_subfield("p")
        item.delete_subfield("t")
        item.delete_subfield("x")

        # Move subfields
        
        # Wrong notes
        if (item["7"]):
            add_subfield(item, "u", item["7"])
            item.delete_subfield("7")

    logger.info("Record fully processed")

    # Writes the record
    MRC_WRITER.write(record.as_marc())

logger.info("Main function just ended")

# Close in and out files
MRC_READER.close()
MRC_WRITER.close()
F_ERRORS.close()

logger.info("<(^-^)> <(^-^)> Script fully executed without errors <(^-^)> <(^-^)>")