# -*- coding: utf-8 -*- 

# external imports
import os
import re
import dotenv

# internal imports
import api.koha.Koha_SRU as Koha_SRU
import archires_coding_convention_resources as accr

dotenv.load_dotenv()

KOHA_URL = accr.erase_trailing_slash(os.getenv("KOHA_ARCHIRES_SRU"))
FILE_PATH = os.getenv("PPN_IN_KOHA_FILE_IN")
OUTPUT_PATH = os.path.dirname(FILE_PATH) + "/PPN_in_ArchiRes.csv"

with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
    f_out.write("PPN;nb_match;bibnb\n")
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for row in f.readlines():
            # Normalize PPN
            ppn = re.sub(r"[^\dX]", "", row)
            while len(ppn) < 9:
                ppn = "0" + ppn
            print(ppn)

            output = [str(ppn)]
            if ppn != "NULL":
                res = Koha_SRU.Koha_SRU(f"dc.identifier all {ppn}", KOHA_URL, version="2.0")
                
                output.append(str(res.get_nb_results()))
                if output[1] == "0":
                    output.append("")
                else:
                    output.append(str(res.get_records_id())[1:-1])

            else:
                output.append("SKIPPED")
                output.append("")

            f_out.write(";".join(output) + "\n")
