from utils.api import (
    get_tasks
)
from models.Expense import Expense
from datetime import datetime
from todoist_api_python.api import TodoistAPI
from custom_logger import get_logger
DEFAULT_CATEGORY = "want"
from typing import List

SRC_MAP = {
    4:"Credit Card",
    3:"Debit Card",
    2:"UPI",
    1:"Cash"
}

logger = get_logger(__name__)

def get_expenses(api:TodoistAPI, project_id):
    logger.debug("Getting expenses")
    expense_tasks = get_tasks(api, project_id)
    expenses:List[Expense] = []
    for task in expense_tasks:
        amount = task.content.split(' ')[0]
        reason = task.content[len(amount)+1:]
        category = ""
        if 'want' in task.labels:
            category = "want"
        if 'need' in task.labels:
            category = "need"
        if category == "":
            category = DEFAULT_CATEGORY
        date=task.due.datetime
        if not date:
            datetime_object = datetime.strptime(task.due.date, '%Y-%m-%d')
            date = datetime_object
        source = SRC_MAP.get(task.priority)
        expense = Expense(
            date=date,
            amount = amount,
            reason=reason,
            category=category,
            source=source,
            task=task
            )
        expenses.append(expense)
    logger.debug([exp.short_print() for exp in expenses])
    return expenses