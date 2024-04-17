# -*- coding: utf-8 -*- 

# external imports
from enum import Enum
import csv

class Error_File_Headers(Enum):
        INDEX = "index"
        ID = "id"
        ERROR = "error"
        TXT = "error_message"
        DATA = "data"

class Errors(Enum):
    CHUNK_ERROR = 0
    NO_RECORD_ID = 1
    
    # Add biblionumber & barcodes to records
    ALREADY_MAPPED = 100
    MATCHED_ID_NOT_A_INT = 101
    TOO_MUCH_BARCODES = 102

    # Fix records (10000 → 19999)
    TOO_MUCH_099 = 10000
    DUPLICATE_SUBFIELD_099 = 10001
    NO_ARCHIRES_DOCTYPE = 10030
    NO_971 = 10050
    NO_ORIGIN_DB_DOCTYPE = 10051
    NO_100 = 10100
    NO_100_A = 10101
    INVALID_LENGTH_100_A = 10102
    NO_101 = 10200
    NO_101_A = 10201
    NO_102 = 10210
    NO_102_A = 10211
    NO_102_C = 10212


class Errors_Manager(object):
    def __init__(self, file_path:str) -> None:
        self.file = open(file_path, "w", newline="", encoding='utf-8')
        self.headers = []
        for member in Error_File_Headers:
            self.headers.append(member.value)
        self.writer = csv.DictWriter(self.file, extrasaction="ignore", fieldnames=self.headers, delimiter=";")
        self.writer.writeheader()

    def close(self):
        self.file.close()

    def trigger_error(self, index:int, id:str, error:Errors, txt:str, data:str):
        """Trigger an error.
        Takes as argument :
            - index {int} : record index, negative value means skipped
            - id {str} : record ID
            - error {Errors} : Error type
            - txt {str} : Error message
            - data {str} : additionnal information (ex : data that trigger the error)"""
        if index < 0:
            index = "Ø"
        self.writer.writerow(
            {
                Error_File_Headers.INDEX.value:index,
                Error_File_Headers.ID.value:id,
                Error_File_Headers.ERROR.value:error.name,
                Error_File_Headers.TXT.value:txt,
                Error_File_Headers.DATA.value:data
            }
        )
