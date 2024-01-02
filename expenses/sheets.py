import gspread
from models.Expense import Expense
from gspread.worksheet import Worksheet
from gspread.exceptions import WorksheetNotFound
from typing import List
from todoist_api_python.api import TodoistAPI
import os
from dotenv import load_dotenv
from custom_logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def add_expenses_to_sheet(expenses:List[Expense], sheet_url:str, api:TodoistAPI):
    # Get the absolute path to the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to service_account.json
    service_account_path = os.path.join(script_directory, 'service_account.json')
    service_account = gspread.service_account(filename=service_account_path)
    sheet = service_account.open_by_url(sheet_url)
    DEBUG = os.getenv('DEBUG',False)
    # row format:
    # DATE	REASON  DESCRIPTION CATEGORY	SOURCE	AMOUNT
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
                ["DATE","REASON","DESCRIPTION","CATEGORY","SOURCE","AMOUNT"]
            )
            logger.info("Created a month sheet "+MONTH_SHEET)
        try:
            mastersheet = sheet.worksheet("MASTERSHEET")
        except WorksheetNotFound:
            mastersheet:Worksheet = sheet.add_worksheet("MASTERSHEET",0,0)
            mastersheet.append_row(
                ["DATE","REASON","DESCRIPTION","CATEGORY","SOURCE","AMOUNT"]
            )
            logger.info("Created the master sheet")
        try:
            mastersheet.append_row(values=values)
            month_sheet.append_row(values=values)
            logger.info("Added to sheet:\n"+expense.short_print())
            if DEBUG == False:
                if api.close_task(expense.task.id):
                    logger.info("Successfully closed expense task",expense.short_print())
        except Exception as e:
            logger.error("Appending expenses to sheets failed.\n"+str(e))