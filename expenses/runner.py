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
import os

def manage_expenses(api:TodoistAPI):
    project_id = os.getenv("EXP_PROJECT_ID")
    EXPENSES_SHEET_URL = os.getenv('EXPENSES_SHEET_URL')
    print(EXPENSES_SHEET_URL)
    if not project_id:
        project = choose_project(api)
    else:
        project = api.get_project(project_id)
    if project:
        expenses = get_expenses(api, project_id)
        # print("expenses:\n",expenses)
        # add expenses to sheet
        add_expenses_to_sheet(expenses, sheet_url=EXPENSES_SHEET_URL, api=api)