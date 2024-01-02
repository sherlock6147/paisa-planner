from datetime import datetime
from typing import List
from todoist_api_python.models import Task

class Expense:
    def __init__(
            self,
            date:datetime,
            amount,
            reason,
            category,
            source,
            task:Task,
            ):
        self.date = date
        self.amount = float(amount)
        self.reason = str(reason).upper()
        self.category = str(category).upper()
        self.source = str(source).upper()
        self.task = task
        self.description = task.description

    def short_print(self):
        return "DATE_TIME:"+self.date.strftime("%d/%m/%Y,%H:%M:%S")+"|AMOUNT:"+str(self.amount)+"|"+str(self.category).upper()+"|"+self.reason+"|"+self.source + "\ndescription: " + self.description

    def __str__(self) -> str:
        return self.short_print(self)

    def to_values(self) -> List[str]:
        return [self.date.strftime("%d/%m/%Y,%H:%M:%S"), self.reason,self.description, self.category, self.source, self.amount]