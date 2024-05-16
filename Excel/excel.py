import pandas as pd
import datetime as dt
from openpyxl import load_workbook, Workbook


class Excel:
    def __init__(self) -> None:
        self.data_path = "Data"

    def export_to_excel(
        self,
        df: pd.DataFrame,
        file_name: str,
        folder: str,
        if_sheet_exists: str = "error",
    ) -> None:
        """

        df: Dataframe to export.
        file_name: File name to save.
        folder: Folder to save file in.
        if_sheet_exists: How to handle a sheet existing.
                         error: raise a ValueError.
                         new: Create a new sheet, with a name determined by the engine.
                         replace: Delete the contents of the sheet before writing to it.
                         overlay: Write contents to the existing sheet without first removing, but possibly over top of, the existing contents.

        """

        date = dt.datetime.now().date()
        date_str = date.strftime("%Y-%m-%d")
        file_name = f"{file_name}.xlsx"
        path = f"{self.data_path}\\{folder}\\Excel\\{file_name}"

        try:
            with pd.ExcelWriter(
                path, mode="a", engine="openpyxl", if_sheet_exists=if_sheet_exists
            ) as writer:
                try:
                    df.to_excel(writer, sheet_name=date_str)
                except ValueError:
                    print(f"[Excel Exists]: Sheet '{date_str} already exists.")
        except FileNotFoundError:
            with pd.ExcelWriter(path, mode="w", engine="openpyxl") as writer:
                try:
                    df.to_excel(writer, sheet_name=date_str)
                except ValueError:
                    print(f"[Excel Exists]: Sheet '{date_str} already exists.")

    def export_to_csv(self, df: pd.DataFrame, file_name: str, folder: str):
        date = dt.datetime.now().date()
        date_str = date.strftime("%Y-%m-%d")
        file_name = f"{file_name}_{date_str}.csv"
        path = f"{self.data_path}\\{folder}\\CSV\\{file_name}"

        try:
            df = pd.read_csv(path)
            print(f"[CSV Exist] {file_name}")
        except FileNotFoundError:
            df.to_csv(path)
