# -*- coding: utf-8 -*- 

# external imports
import os
import dotenv
import pymarc
from unidecode import unidecode
import re
from typing import List

# Internal import
from utils.errors_manager import Errors_Manager, Errors
import utils.marc_utils as marc_utils
from utils.logs_manager import Logger

# Load paramaters
dotenv.load_dotenv()

SERVICE = os.getenv("FIX_RECORDS_SERVICE_NAME")
LOGS_FOLDER = os.path.abspath(os.getenv("FIX_RECORDS_LOGS_FOLDER"))
LOGS_LEVEL = os.getenv("FIX_RECORDS_LOGS_LEVEL")
FILE_IN = os.getenv("FIX_RECORDS_FILE_IN")
directory, filename = os.path.split(FILE_IN)
FILE_OUT = os.path.join(directory, f"010_FIXED_{filename}")
FILE_OUT_SKIPPED = os.path.join(directory, f"010_SKIPPED_{filename}")
ERRORS_FILE_PATH = os.getenv("FIX_RECORDS_ERRORS_FILE")
ERR_MAN = Errors_Manager(ERRORS_FILE_PATH) # DON'T FORGET ME
W_ETUD_MAPPING = {
    unidecode("CESP").upper():"CESP",
    unidecode("DEP").upper():"PFE",
    unidecode("Mémoire").upper():"MEMU",
    unidecode("Mémoire ENSP").upper():"MES",
    unidecode("Thèse").upper():"THES",
    unidecode("TPFE").upper():"TPFE",
    unidecode("Atelier régional").upper():"TATE",
    unidecode("Travaux d'atelier").upper():"TATE",
    "default":"TATE"
}
DOCTYPE_LEADER_MAPPING = {
    "JEU":"rm",
    "ECH":"rm",
    "MULT":"mm",
    "DOCG":"km",
    "DOCS":"im",
    "DOCA":"gm",
    "CART":"em",
    "REV":"as",
    "COLL":"as",
    "DOS":"ac",
    "ART":"aa",
    "MES":"am",
    "TPFE":"am",
    "LIV":"am",
    "PFE":"am",
    "THES":"am",
    "ECART":"im",
    "EDOCA":"im",
    "ELIV":"im",
    "RESELEC":"im",
    "REVELEC":"im",
    "default":"am"
}

# ----------------- Functions definition -----------------
def get_date_from_lists(data:List[str]) -> List[int]:
    """Takes a list of strings with maybe years and return all 4-digit years found as ints"""
    output = []
    for txt in data:
        output += re.findall(r"\b\d{4}\b", re.sub(r"(DL|COP\.|COPYRIGHT|COP|C)", "", txt, flags=re.IGNORECASE))
    output_as_int = []
    for date in output:
        output_as_int.append(int(date))
    return output_as_int

def generate_100_a_pos_9_16(dates:List[int]) -> str:
    """Returns a 8 character long string for UNIMARC 100 $a pos.9-16"""
    dates = sorted(dates)
    if len(dates) == 0:
        return " " * 8
    elif len(dates) == 1:
        return str(dates[0]) + " " * 4
    else:
        return str(dates[0]) + str(dates[len(dates)-1])

def generate_leader_pos_6_7_from_ArchiRes_doctype(doctype:str) -> str:
    """Returns a 2 character long string for UNM leader pos.6-7"""
    if doctype in DOCTYPE_LEADER_MAPPING:
        return DOCTYPE_LEADER_MAPPING[doctype]
    else:
        return DOCTYPE_LEADER_MAPPING["default"]

def ENSP_edit_7XX(record:pymarc.record.Record, tag:str):
    """Agregate function to call multiple functions on 7XX"""
    # Put COLLECTIF in lower case
    for field in record.get_fields(tag):
        marc_utils.edit_specific_repeatable_subfield_content_with_regexp(field, ["a"], r"^\s*COLLECTIF\s*$", r"Collectif")
    # Split if multiple authors in the same tag
    marc_utils.split_merged_tags(record, tag)
    # Delete field if author is "s. a"
    marc_utils.delete_field_if_all_subfields_match_regexp(record, tag, "a", r"^\s*[s|S]\s*\.\s*[a|A]\s*\.\s*$")
    # Delete multiple $4
    marc_utils.delete_multiple_subfield_for_tag(record, tag, "4")
    # Add mising $4
    marc_utils.add_missing_subfield_to_field(record, tag, "4", "070")
    # Old way, but was not taking into account that some 7XX have different $4 in them
    # # Split if multiple $a
    # marc_utils.split_tags_if_multiple_specific_subfield(record, tag, "a")
    # Sort the subfields
    marc_utils.sort_subfields_for_tag(record, tag, ["a", "b", "*", "4"])
    # Forces indicators
    if tag[1] == "0":
        marc_utils.force_indicators(record, tag, [" ", "1"])
    else:
        marc_utils.force_indicators(record, tag, ["0", "2"])
    # Delete if there's only spaces in $a or no $a
    marc_utils.delete_field_if_all_subfields_match_regexp(record, tag, "a", r"^\s+$", keep_if_no_subf=False)

def get_ArchiRes_W_etud_from_ENSP_doctype(doctype:str) -> str:
    """Returns the mapped ArchiRès thesis type based on ENSP document type"""
    doctype = unidecode(doctype).upper()
    if doctype in W_ETUD_MAPPING:
        return W_ETUD_MAPPING[doctype]
    else:
        return W_ETUD_MAPPING["default"]

def generate_ENSP_029_for_ArchiRes(kentika_nb:str, w_etud:str, dates:List[int]) -> pymarc.field.Field:
    """Generates a ENSp's 029 for ArchiRès, returns a pymarc field
    
    Takes as argument :
        - kentika_nb : the kentika nb (without ENSP) (str)
        - w_etud : the thesis type
        - dates (List of int) : the dates as returned by the generation of 100$a"""
    
    # Get the date
    dates = sorted(dates)
    date = "9999"
    if len(dates) > 0:
        date = str(dates[0])

    # Generates the field
    field = pymarc.field.Field("029", indicators=[" ", " "])
    field.add_subfield("a", "FR")
    field.add_subfield("m", f"{date}_{w_etud}_ENSP_ENSP{kentika_nb}")
    
    # Return the field
    return field

def generate_ENSP_328_for_ArchiRes(kentika_doctype:str, reference:str, dates:List[int]) -> pymarc.field.Field:
    """Generates a ENSp's 328 for ArchiRès, returns a pymarc field
    
    Takes as argument :
        - kentika_doctype : the kentika document type
        - reference : str 214$c
        - dates (List of int) : the dates as returned by the generation of 100$a"""
    
    # Get the date
    dates = sorted(dates)
    date = "[s. d.]"
    if len(dates) > 0:
        date = str(dates[0])

    # Generates the field
    field = pymarc.field.Field("328", indicators=[" ", "0"])
    field.add_subfield("b", kentika_doctype)
    field.add_subfield("c", "Paysage")
    if not reference:
        field.add_subfield("e", "École nationale supérieure de paysage")
    else:
        field.add_subfield("e", reference)
    field.add_subfield("d", date)
    
    # Return the field
    return field

# ----------------- Class definitions -----------------

# ----------------- Preparing Main -----------------
# Open in and out files
# BINARY is mandatory for MARC files
MARC_READER = pymarc.MARCReader(open(FILE_IN, 'rb'), to_unicode=True, force_utf8=True) # DON'T FORGET ME
MARC_WRITER = open(FILE_OUT, "wb") # DON'T FORGET ME
SKIPPED_MARC_WRITER = open(FILE_OUT_SKIPPED, "wb") # DON'T FORGET ME

# Init logger & error
LOG = Logger(LOGS_FOLDER, SERVICE, LOGS_LEVEL)
LOG.info(f"Input file : {FILE_IN}")
LOG.info(f"Output file : {FILE_OUT}")
LOG.info(f"Error file : {ERRORS_FILE_PATH}")

# ----------------- Main -----------------
LOG.info("Starting main function...")

# Loop through records
for record_index, record in enumerate(MARC_READER):
    LOG.info(f"--- Starting Record {record_index}")

    # If record is invalid
    if record is None:
        ERR_MAN.trigger_error(record_index, "", Errors.CHUNK_ERROR, "Chunk error : check logs", "")
        LOG.error_in_record_loop(record_index, "", f"Current chunk: {MARC_READER.current_chunk} was ignored because the following exception raised: {MARC_READER.current_exception}")
        continue

    LOG.debug("Record is valid")

    # ---------- Record ----------
    # Ensure previous iterations do not interfere
    leave_loop = False
    kentika_nb = None
    all_099 = None
    u099_subfields = None
    archires_doctype = None
    kentika_doctype = None
    new_100 = None
    all_210_4 = None
    dates = []
    split_items = None
    all_subfields = None
    all_7X0 = None

    # Delete empty subfields then empty fields
    marc_utils.delete_empty_subfields(record)
    marc_utils.delete_empty_fields(record)

    # Get the Kentika number
    for field in record.get_fields("035"):
        for subfield in field.get_subfields("a"):
            if subfield[:12] == "Kentika_ENSP":
                kentika_nb = subfield[12:]
    if not kentika_nb:
        ERR_MAN.trigger_error(record_index, "", Errors.NO_RECORD_ID, "No Kentika number was found in the record", "")
        LOG.error_in_record_loop(record_index, "", Errors.NO_RECORD_ID.name)
        continue
    LOG.simple_debug("Kentika number", kentika_nb)

    # Merge 099
    # We take all 099, add to the first every subfied from the others
    # and delete the others
    # Then we chack if the remaining has no duplicate subfields 
    marc_utils.merge_all_fields_by_tag(record, "099")
    # Extra check, but should never occur
    all_099 = record.get_fields("099")
    if len(all_099) > 1:
        ERR_MAN.trigger_error(record_index, kentika_nb, Errors.TOO_MUCH_099, "More than 1 099 were found in the record after the merge", str(len(all_099)))
        LOG.error_in_record_loop(record_index, kentika_nb, Errors.TOO_MUCH_099.name)
        continue
    # Check if there are duplicate subfields
    u099_subfields = all_099[0].subfields_as_dict()
    for code in u099_subfields.keys():
        if len(u099_subfields[code]) > 1:
            ERR_MAN.trigger_error(record_index, kentika_nb, Errors.DUPLICATE_SUBFIELD_099, "The same subfield was found multiple times in the 099", f"${code} : {len(u099_subfields[code])}")
            LOG.error_in_record_loop(record_index, kentika_nb, Errors.DUPLICATE_SUBFIELD_099.name)
            LOG.simple_info("099 duplicate subfield", code)
            leave_loop = True
    # Leave if duplicate subfield
    if leave_loop:
        continue

    # Get ArchiRès doctype
    archires_doctype = record["099"]["t"]
    if archires_doctype == None:
        ERR_MAN.trigger_error(record_index, kentika_nb, Errors.NO_ARCHIRES_DOCTYPE, "ArchiRès document type was not found", "")
        LOG.error_in_record_loop(record_index, kentika_nb, Errors.NO_ARCHIRES_DOCTYPE.name)
        continue
    LOG.simple_debug("ArchiRès doctype", archires_doctype)

    # Skip ArchiRès typedoc REV & Chapitre
    if archires_doctype in ["REV", "Chapitre"]:
        LOG.info(f"Skipping this record because its ArchiRès doctype is {archires_doctype}")
        SKIPPED_MARC_WRITER.write(record.as_marc())
        continue

    # Fix the leader
    new_leader = record.leader[0:6] # No pb first 5 pos
    new_leader += generate_leader_pos_6_7_from_ArchiRes_doctype(archires_doctype)
    new_leader += "##" # Fix pos 8 + 9
    new_leader += record.leader[10:17] # Keep pos 10 to 16
    if record.leader[17] == "#":
        new_leader += " "
    else:
        new_leader += record.leader[17]
    new_leader += record.leader[18:22] # Keep pos 18 to 21
    new_leader += "0" # Fix pos 22
    new_leader += record.leader[23] # Keep pos 23
    record.leader = new_leader

    # Leave if no 100
    if not (record["100"]):
        ERR_MAN.trigger_error(record_index, kentika_nb, Errors.NO_100, "No 100 was found in the record", "")
        LOG.error_in_record_loop(record_index, kentika_nb, Errors.NO_100.name)
        continue
    # Leave if no 100$a
    if not (record["100"]["a"]):
        ERR_MAN.trigger_error(record_index, kentika_nb, Errors.NO_100_A, "No $a was found in the first 100 found in the record", record["100"])
        LOG.error_in_record_loop(record_index, kentika_nb, Errors.NO_100_A.name)
        continue
    # Fix 100$a
    new_100 = f"{record['100']['a'][:8]}d" # pos 0-8 with pos. 8 fix
    all_210_4 = record.get_fields("210", "214") # pos. 9-16 fix
    for field in all_210_4:
        if "d" in field.subfields_as_dict():
            dates += get_date_from_lists(field.subfields_as_dict()["d"])
    new_100 += generate_100_a_pos_9_16(dates)
    new_100 += record['100']['a'][16:25] # pos. 17 to 25 fix (needs to be moved 1 pos)
    new_100 += "50" + " " * 6 # pos26 to 33 fix
    new_100 += record['100']['a'][-3:-1] # pos. 34-35
    record["100"]["a"] = new_100

    # Check if the 100$a is 36 char long
    if not len(record["100"]["a"]) == 36:
        ERR_MAN.trigger_error(record_index, kentika_nb, Errors.INVALID_LENGTH_100_A, "100$a length is invalid despite modifications", f"100$a : length : {len(record['100']['a'])}, content : {record['100']['a']}")
        LOG.error_in_record_loop(record_index, kentika_nb, Errors.INVALID_LENGTH_100_A.name)
        continue

    # Generates 029 & 328 if it's a thesis
    # Here because we reuse dates from the 100 generation
    if archires_doctype == "TE":
        # Get Thesis type
        if record["971"] == None:
            ERR_MAN.trigger_error(record_index, kentika_nb, Errors.NO_971, "No 971 was found in the record", "")
            LOG.error_in_record_loop(record_index, kentika_nb, Errors.NO_971.name)
            continue
        if record["971"]["a"] == None:
            ERR_MAN.trigger_error(record_index, kentika_nb, Errors.NO_ORIGIN_DB_DOCTYPE, "Kentika document type was not found", record["971"])
            LOG.error_in_record_loop(record_index, kentika_nb, Errors.NO_ORIGIN_DB_DOCTYPE.name)
            continue
        kentika_doctype = record["971"]["a"]

        # Adds the 029
        record.add_ordered_field(generate_ENSP_029_for_ArchiRes(kentika_nb, get_ArchiRes_W_etud_from_ENSP_doctype(kentika_doctype), dates))

        # Adds the 328
        if record["214"] == None:
            record.add_ordered_field(generate_ENSP_328_for_ArchiRes(kentika_doctype, None, dates))
        else:
            record.add_ordered_field(generate_ENSP_328_for_ArchiRes(kentika_doctype, record["214"]["c"], dates))


    # Leave if no 101
    if not (record["101"]):
        ERR_MAN.trigger_error(record_index, kentika_nb, Errors.NO_101, "No 101 was found in the record", "")
        LOG.error_in_record_loop(record_index, kentika_nb, Errors.NO_101.name)
        continue
    # Leave if no 101$a
    if not (record["101"]["a"]):
        ERR_MAN.trigger_error(record_index, kentika_nb, Errors.NO_101_A, "No $a was found in the first 101 found in the record", record["101"])
        LOG.error_in_record_loop(record_index, kentika_nb, Errors.NO_101_A.name)
        continue
    # Fix 101 with unknown code
    marc_utils.edit_specific_repeatable_subfield_content_with_regexp(record["101"], ["a", "c"], r"^\s*([a-z]{3})\s*$", r"\1")
    marc_utils.edit_specific_repeatable_subfield_content_with_regexp(record["101"], ["a", "c"], r"^jap$", r"jpn") # jap -> jpn
    marc_utils.replace_specific_repeatable_subfield_content_not_matching_regexp(record["101"], ["a", "c"], r"^[a-z]{3}$", "und")
    
    # Fix 101 indicators
    marc_utils.force_indicators(record, "101", ["0", " "])

    # Merge all 181
    marc_utils.merge_all_fields_by_tag(record, "181", ["6", "*", "2"])

    # Add $6 & $2 to 182
    # Merge all 182 just in case
    marc_utils.merge_all_fields_by_tag(record, "182")
    marc_utils.add_missing_subfield_to_field(record, "182", "6", "z01", 0)
    marc_utils.add_missing_subfield_to_field(record, "182", "2", "rdamedia")

    # Merge all 183
    marc_utils.merge_all_fields_by_tag(record, "183", ["6", "*", "2"])

    # Merge all 200 just in case
    marc_utils.merge_all_fields_by_tag(record, "200")
    
    # Delete whitespace only 200$e
    # We replace by nothing so it can be deleted at the end
    marc_utils.edit_specific_repeatable_subfield_content_with_regexp(record["200"], ["e"], r"^\s+$", "")

    # Delete whitespace only 205 & 214$a
    # We replace by nothing so it can be deleted at the end
    for field in record.get_fields("205", "214"):
        marc_utils.edit_specific_repeatable_subfield_content_with_regexp(field, ["a"], r"^\s+$", "")

    # Delete 210/4$d with 0 as value
    # We replace by nothing so it can be deleted at the end
    for field in record.get_fields("210", "214"):
        marc_utils.edit_specific_repeatable_subfield_content_with_regexp(field, ["d"], r"^\s*0\s*$", "")

    # Delete 225 with empty data
    marc_utils.delete_field_if_all_subfields_match_regexp(record, "225", "a", r"^\s+$", keep_if_no_subf=False)
    
    # Delete 330 with empty data
    marc_utils.delete_field_if_all_subfields_match_regexp(record, "330", "a", r"^\s+$", keep_if_no_subf=False)

    # Delete 410 with empty data
    marc_utils.delete_field_if_all_subfields_match_regexp(record, "410", "t", r"^\s+$", keep_if_no_subf=False)

    # Merge all 463 & split if multiple $t
    marc_utils.merge_all_fields_by_tag(record, "463")
    marc_utils.split_tags_if_multiple_specific_subfield(record, "463", "t")
    marc_utils.sort_subfields_for_tag(record, "463", ["t"])

    # Delete 615 without $a
    marc_utils.delete_field_if_all_subfields_match_regexp(record, "615", "a", r"^$", keep_if_no_subf=False)

    # Adds missing $2 to 615 with $a
    marc_utils.add_missing_subfield_to_field(record, "615", "2", "ENSP")

    # Sort 615 subfields
    marc_utils.sort_subfields_for_tag(record, "615", ["a", "*", "2"])

    # 7XX : Delete multiple $4, add missing $4, split if multiple $a, sort subfields for 7XX
    ENSP_edit_7XX(record, "700")
    ENSP_edit_7XX(record, "701")
    ENSP_edit_7XX(record, "702")
    ENSP_edit_7XX(record, "710")
    ENSP_edit_7XX(record, "711")
    ENSP_edit_7XX(record, "712")

    # Checks if they are multiple 7X0 and keeps the first one only as a 7X0
    # if 700 & 710, keep the 700
    all_7X0 = record.get_fields("700", "710")
    if len(all_7X0) > 1:
        LOG.debug("Multiple 7X0, keeping first 700 as 7X0 and moving the other as 7X1")
        has_700 = len(record.get_fields("700")) > 0
        first_occ = True
        for field in all_7X0:
            # i know I can nest things, but i like this better 
            if first_occ:
                if field.tag == "710" and has_700:
                    field.tag = "711"
                elif field.tag == "700":
                    first_occ = False
            else:
                field.tag = field.tag[:2] + "1"

    # Checks if there's a 7X0 if 7X1 are in the record
    if len(record.get_fields("700", "710")) == 0 and len(record.get_fields("701", "711", "702", "712")) > 0:
        for tag in ["701", "711", "702", "712"]:
            if len(record.get_fields(tag)) > 0:
                record.get_fields(tag)[0].tag = record.get_fields(tag)[0].tag[:2] + "0"
                break

    # Splits 856 if they are multiple $u
    marc_utils.split_tags_if_multiple_specific_subfield(record, "856", "u")

    # Delete 972 with empty data
    marc_utils.delete_field_if_all_subfields_match_regexp(record, "972", "a", r"^\s+$", keep_if_no_subf=False)

    # Split 995 if multiple items are in one
    marc_utils.split_merged_tags(record, "995")
    marc_utils.force_indicators(record, "995")
    # Why the fuck did I put ind2 = 0 for items in the first script ???? A garbage copy paste ???????


    # Delete empty subfields then empty fields (again)
    marc_utils.delete_empty_subfields(record)
    marc_utils.delete_empty_fields(record)

    # Sort the record fields
    marc_utils.sort_fields_by_tag(record)

    LOG.info("Record fully processed")

    # Writes the record
    MARC_WRITER.write(record.as_marc())

# Close in and out files
MARC_READER.close()
MARC_WRITER.close()
SKIPPED_MARC_WRITER.close()
ERR_MAN.close()

LOG.info("<(^-^)> <(^-^)> Script fully executed without errors <(^-^)> <(^-^)>")