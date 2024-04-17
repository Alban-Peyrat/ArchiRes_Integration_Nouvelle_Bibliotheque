# -*- coding: utf-8 -*- 

# external imports
import os
import re
import dotenv
import csv
from enum import Enum

# internal imports
import api.koha.Koha_SRU as ksru
import utils.fcr_func as fcf

dotenv.load_dotenv()

KOHA_URL = os.getenv("PPN_IN_KOHA_KOHA_SRU")
sru = ksru.Koha_SRU(KOHA_URL, ksru.SRU_Version.V1_1)
FILE_PATH = os.getenv("PPN_IN_KOHA_FILE_IN")
OUTPUT_PATH = os.getenv("PPN_IN_KOHA_OUTPUT_FILE")

class Output_Headers(Enum):
    PPN = "ppn"
    NB_MATCH = "nb_match"
    BIBNB = "bibnb"

with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f_out:
    WRITER = csv.DictWriter(f_out, extrasaction="ignore", fieldnames=[elem.value for elem in Output_Headers], delimiter=";")
    WRITER.writeheader()
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for row in f.readlines():
            # Normalize PPN
            ppn = re.sub(r"[^\dX]", "", row)
            while len(ppn) < 9:
                ppn = "0" + ppn

            output = {
                Output_Headers.PPN.value:str(ppn),
                Output_Headers.NB_MATCH.value:"",
                Output_Headers.BIBNB.value:""
            }

            # If PPN == NULL, leave
            if ppn == "NULL":
                output[Output_Headers.BIBNB.value] = "SKIPPED_PPN"
                WRITER.writerow(output)
                continue

            # If PPN would end up making an empty request, leave
            ppn = fcf.delete_for_sudoc(ppn).strip()
            if ppn == "":
                output[Output_Headers.BIBNB.value] = "EMPTY_PPN"
                WRITER.writerow(output)
                continue

            # Queries the SRU
            sru_request = [ksru.Part_Of_Query(ksru.SRU_Indexes.DC_IDENTIFIER,ksru.SRU_Relations.EQUALS, ppn)]
            res = sru.search(
                sru.generate_query(sru_request),
                record_schema=ksru.SRU_Record_Schemas.MARCXML,
                start_record=1,
                maximum_records=10
            )
            # SRU Error
            if (res.status == "Error"):
                output[Output_Headers.BIBNB.value] = "SRU_ERROR"
                WRITER.writerow(output)
                continue
            
            # SRU Success
            output[Output_Headers.NB_MATCH.value] = len(res.get_records_id())
            output[Output_Headers.BIBNB.value] = ", ".join(res.get_records_id())
            WRITER.writerow(output)
