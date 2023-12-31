import gspread
from models.Expense import Expense
from gspread.worksheet import Worksheet
from gspread.exceptions import WorksheetNotFound
from typing import List
from todoist_api_python.api import TodoistAPI
import os

def add_expenses_to_sheet(expenses:List[Expense], sheet_url:str, api:TodoistAPI):
    # Get the absolute path to the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to service_account.json
    service_account_path = os.path.join(script_directory, 'service_account.json')
    service_account = gspread.service_account(filename=service_account_path)
    sheet = service_account.open_by_url(sheet_url)
    # row format:
    # DATE	REASON	CATEGORY	SOURCE	AMOUNT
    for expense in expenses:
        values = expense.to_values()
        MONTH_SHEET = f"{expense.date.strftime('%Y-%B').upper()}"
        mastersheet = None
        month_sheet = None
        try:
            month_sheet = sheet.worksheet(MONTH_SHEET)
        except WorksheetNotFound:
            month_sheet:Worksheet = sheet.add_worksheet(MONTH_SHEET,0,0)
            month_sheet.append_row(
                ["DATE","REASON","CATEGORY","SOURCE","AMOUNT"]
            )
        try:
            mastersheet = sheet.worksheet("MASTERSHEET")
        except WorksheetNotFound:
            month_sheet:Worksheet = sheet.add_worksheet("MASTERSHEET",0,0)
            month_sheet.append_row(
                ["DATE","REASON","CATEGORY","SOURCE","AMOUNT"]
            )
        mastersheet.append_row(values=values)
        month_sheet.append_row(values=values)
        if api.close_task(expense.task.id):
            print("Successfully closed expense ",expense.short_print())