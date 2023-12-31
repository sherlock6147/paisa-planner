# 1. Get payment logs from todoist
# 2. Move them into categories based on the task tags
# 3. Update them to google sheets
# 4. Move the updated tasks to completed and history section
import os
from dotenv import load_dotenv
from expenses.runner import (
    manage_expenses
)
from utils.sheets import (
    status_update
)
from todoist_api_python.api import TodoistAPI

# load env variables
load_dotenv()

API_KEY = os.getenv("TODOIST_API_TOKEN","")

api = TodoistAPI(API_KEY)

manage_expenses(api)
status_update(os.getenv("EXPENSES_SHEET_URL"))