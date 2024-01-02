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
from custom_logger import get_logger

# load env variables
load_dotenv()
logger = get_logger(__name__)
API_KEY = os.getenv("TODOIST_API_TOKEN","")

try:
    api = TodoistAPI(API_KEY)
    projects = api.get_projects()
    logger.info('API object creation successfull.')
except Exception as e:
    logger.critical('API object creation failed. Check API_KEY and environment variables.\n'+str(e))
manage_expenses(api)
status_update(os.getenv("EXPENSES_SHEET_URL"))