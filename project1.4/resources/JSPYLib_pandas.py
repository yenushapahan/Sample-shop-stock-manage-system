import pandas as pd
import json
import os

class DATABASE:
    def __init__(self, fileName):
        self.fileName = f"{fileName}.json"
        self._initialize_file()

    def _initialize_file(self):
        """Ensure the JSON file exists and has a valid structure"""
        if not os.path.exists(self.fileName):
            with open(self.fileName, "w") as f:
                json.dump([], f, indent=4)

    def readData(self):
        """Read JSON file into a Pandas DataFrame"""
        try:
            return pd.read_json(self.fileName)
        except ValueError:
            print("Error: Invalid JSON format.")
            return pd.DataFrame()

    def insertData(self, content):
        """Add new entry to JSON file"""
        df = self.readData()
        df = df.append(content, ignore_index=True)  # Append new data
        df.to_json(self.fileName, orient="records", indent=4)

    def updateData(self, indexId, updatedContent):
        """Update entry based on index ID"""
        df = self.readData()
        if 0 <= indexId - 1 < len(df):
            df.iloc[indexId - 1] = updatedContent  # Update row directly
            df.to_json(self.fileName, orient="records", indent=4)
            print(f"Updated record at index {indexId}.")
        else:
            print("Error: Invalid index.")

    def deleteData(self, indexId):
        """Delete entry based on index ID"""
        df = self.readData()
        if 0 <= indexId - 1 < len(df):
            df.drop(indexId - 1, inplace=True)  # Remove row
            df.to_json(self.fileName, orient="records", indent=4)
            print(f"Deleted record at index {indexId}.")
        else:
            print("Error: Invalid index.")

    def searchData(self, keyOfDict, valueOfDict):
        """Search for entries matching a specific key-value pair"""
        df = self.readData()
        results = df[df[keyOfDict] == valueOfDict].to_dict(orient="records")
        return results

    def gettingIndex(self):
        """Return the next available index for new entries"""
        df = self.readData()
        return len(df) + 1

    def findUniqItems(self, keyOfDict):
        """Find unique values in a given key"""
        df = self.readData()
        return set(df[keyOfDict].astype(str).str.lower())  # Ensure case insensitivity

    def selectItems(self, keyOfDict, keyOfValue, condition):
        """Select items based on a condition (safe filtering)"""
        df = self.readData()
        try:
            return df.query(f"{keyOfValue} {condition}")[keyOfDict].tolist()
        except Exception:
            print("Error: Invalid condition format.")
            return []