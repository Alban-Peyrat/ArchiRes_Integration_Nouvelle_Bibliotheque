# -*- coding: utf-8 -*- 

# external imports
import os
from dotenv import load_dotenv
import re
import pymarc
from enum import Enum
import csv

# Internal import
from utils.errors_manager import Errors_Manager, Errors

# ---------- Init ----------
load_dotenv()

RECORDS_FILE_PATH = os.getenv("ADD_BIBNB_RECORDS_FILE")
ID_MAPPING_FILE_PATH = os.getenv("ADD_BIBNB_ID_MAPPING_FILE")
FILE_OUT = os.getenv("ADD_BIBNB_FILE_OUT")
ERRORS_FILE_PATH = os.path.abspath(os.getenv("ADD_BIBNB_ERRORS_FILE"))
ERR_MAN = Errors_Manager(ERRORS_FILE_PATH) # DON'T FORGET ME
PREPEND_ORIGIN_DB_ID = os.getenv("ADD_BIBNB_PREPEND_ORIGIN_DB_ID")
PREPEND_TARGET_DB_ID = os.getenv("ADD_BIBNB_PREPEND_TARGET_DB_ID")
BARCODE_PREFIX = os.getenv("ADD_BIBNB_BARCORDE_PREFIX")
BARCODE_CITY = os.getenv("ADD_BIBNB_BARCORDE_CITY")
MAPPED_IDS = {}

# ---------- Class definition ----------

# ----- Mapping origin ID / target ID -----
class Mapping_File_Headers(Enum):
    ORIGIN_ID = "origin_db_id"
    TARGET_ID = "target_db_id"

# ---------- Func def ----------
def add_mapped_id(origin_id:str, target_id:str, check_valid_target_id:bool=True) -> None:
    """Adds a new mapped ID"""
    # Checks if it already exists
    if origin_id in MAPPED_IDS:
        ERR_MAN.trigger_error(-1, origin_id, Errors.ALREADY_MAPPED, "This origin ID is alredy mapped", f"Target ID : {target_id}")
        return
    
    # Checks if target ID is valid nb
    if check_valid_target_id:
        match = re.search("^\d+$", target_id)
        if not match:
            ERR_MAN.trigger_error(-1, origin_id, Errors.MATCHED_ID_NOT_A_INT, "Matched ID is invalid", f"Target ID : {target_id}")
            return

    MAPPED_IDS[origin_id] = target_id

def get_mapped_id(origin_id:str) -> str|None:
    """Returns the mapped ID based of the origin ID"""
    if origin_id in MAPPED_IDS:
        return MAPPED_IDS[origin_id]
    return None

# ---------- Preparing Main ----------
MARC_READER = pymarc.MARCReader(open(RECORDS_FILE_PATH, 'rb'), to_unicode=True, force_utf8=True) # DON'T FORGET ME
MARC_WRITER = open(FILE_OUT, "wb") # DON'T FORGET ME
# ----- Load mapped IDs -----
with open(ID_MAPPING_FILE_PATH, "r") as f:
    reader = csv.DictReader(f, fieldnames=[elem.value for elem in Mapping_File_Headers], delimiter=";")
    next(reader) # Skip header line
    for row in reader:
        add_mapped_id(f"{PREPEND_ORIGIN_DB_ID}{row[Mapping_File_Headers.ORIGIN_ID.value]}", f"{PREPEND_TARGET_DB_ID}{row[Mapping_File_Headers.TARGET_ID.value]}")

# ---------- Main ----------
bibnb_added = 0
barcode_fixed = 0
barcode_added = 0
# Loop through records
for record_index, record in enumerate(MARC_READER):
    # If record is invalid
    if record is None:
        ERR_MAN.trigger_error(record_index, "", Errors.CHUNK_ERROR, "", "")
        continue # Fatal error, skipp

    # Gets the record ID
    if not record["035"]:
        ERR_MAN.trigger_error(record_index, "", Errors.NO_RECORD_ID, "No 001 or 035", "")
    elif not record["035"]["a"]:
        ERR_MAN.trigger_error(record_index, "", Errors.NO_RECORD_ID, "No 001 or 035$a", "")
    else:
        record_id = record["035"]["a"]
    
    # Checks if this record is in the record mapping
    matched_id = get_mapped_id(record_id)

    # Generates the 001
    if record["001"]:
        record.remove_field(record["001"])
    if matched_id:
        field_001 = pymarc.field.Field(tag="001", data=matched_id)
        record.add_ordered_field(field_001)
        bibnb_added += 1
   
    # Generates the barcodes if needed
    for item_index, field in enumerate(record.get_fields("995")):
        # Checks if there are too many barcodes
        if len(field.get_subfields("f")) > 1:
            ERR_MAN.trigger_error(record_index, record_id, Errors.TOO_MUCH_BARCODES, "Multiple barcodes were found for this item", field)
            continue

        barcode = BARCODE_PREFIX + "A" + BARCODE_CITY + re.sub(r"\D", "", str(record_id)) + "I" + str(item_index)
        
        # If no barcode is found, adds it
        if not (field["f"]):
            field.add_subfield("f", barcode)
            barcode_added += 1
        # If the barcode is strictly equal to the prefix, rewrite the barcode
        elif field["f"] == BARCODE_PREFIX:
            field["f"] = barcode
            barcode_fixed += 1
        # Else, keep the barcode

    # Writes the record
    MARC_WRITER.write(record.as_marc())

MARC_READER.close()
MARC_WRITER.close()
ERR_MAN.close()

# print some nb
print(f"Bibnb added : {bibnb_added}")
print(f"Barcode fixed : {barcode_fixed}")
print(f"Barcode added : {barcode_added}")