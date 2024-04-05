# -*- coding: utf-8 -*- 

# external imports
import os
from dotenv import load_dotenv
import csv
import pandas as pd
from enum import Enum

load_dotenv()

# Based on AR436 short single exec

# ----------------- Class def -----------------
class Output_Headers(Enum):
    ORIGIN_ID = "origin_db_id"
    TARGET_ID = "target_db_id"

class Output_File(object):
    def __init__(self, file_path:str) -> None:
        self.file = open(file_path, "w", newline="", encoding='utf-8')
        self.headers = [Output_Headers.ORIGIN_ID.value, Output_Headers.TARGET_ID.value]
        self.writer = csv.DictWriter(self.file, extrasaction="ignore", fieldnames=self.headers, delimiter=";")
        self.writer.writeheader()

    def write(self, content:dict):
        self.writer.writerow(content)

    def close(self):
        self.file.close()

class Matched_ids(object):
    def __init__(self, origin_id:str, target_id:str) -> None:
        self.origin_id = origin_id
        self.target_id = target_id
    
    def to_dict(self) -> dict:
        return {
            Output_Headers.ORIGIN_ID.value:self.origin_id,
            Output_Headers.TARGET_ID.value:self.target_id
        }

# ----------------- Func def -----------------

# ----------------- Init -----------------
FILE_FOLDER = os.getenv("EXTRACT_ID_FCR_FILES_FOLDER")
OUTPUT_FILE = Output_File(os.getenv("EXTRACT_ID_FCR_OUTPUT_FILE"))
COL_ORIGIN_ID = os.getenv("EXTRACT_ID_FCR_COLUMN_NAME_ORIGIN_ID")
COL_TARGET_ID = os.getenv("EXTRACT_ID_FCR_COLUMN_NAME_TARGET_ID")
COL_ACTION = os.getenv("EXTRACT_ID_FCR_COLUMN_NAME_ACTION")
ACTION = os.getenv("EXTRACT_ID_FCR_ACTION")

# For each file
file_list = os.listdir(FILE_FOLDER)
for file in file_list:
    # IL FAUT FAIRE UN FOR EACH SHEET
    sheets_dict = pd.read_excel(f"{os.path.abspath(FILE_FOLDER)}/{file}", sheet_name=None)
    for sheet_name, df in sheets_dict.items():
        missing_cols = []
        for col in [COL_ACTION, COL_ORIGIN_ID, COL_TARGET_ID]:
            if not col in df:
                missing_cols.append(col)
        if missing_cols == []:
            for index, row in df[df[COL_ACTION].astype(str).str.contains(ACTION, case=False, na=False)].iterrows():
                OUTPUT_FILE.write(Matched_ids(row[COL_ORIGIN_ID], row[COL_TARGET_ID]).to_dict())
        else:
            print(f"{file} - \"{sheet_name}\" does not have columns : {', '.join(missing_cols)}")

OUTPUT_FILE.close()