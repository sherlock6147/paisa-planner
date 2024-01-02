from todoist_api_python.api import TodoistAPI
from expenses.api import (
    get_expenses
)
from utils.api import (
    choose_project,
)
from expenses.sheets import (
    add_expenses_to_sheet,
)
from custom_logger import get_logger
import os

logger = get_logger(__name__)

def manage_expenses(api:TodoistAPI):
    project_id = os.getenv("EXP_PROJECT_ID")
    EXPENSES_SHEET_URL = os.getenv('EXPENSES_SHEET_URL')
    logger.debug("google sheet url: "+EXPENSES_SHEET_URL)
    if not project_id:
        logger.info("No project id specified.")
        project = choose_project(api)
    else:
        project = api.get_project(project_id)
    logger.debug(project_id)
    if project:
        expenses = get_expenses(api, project_id)
        # add expenses to sheet
        add_expenses_to_sheet(expenses, sheet_url=EXPENSES_SHEET_URL, api=api)