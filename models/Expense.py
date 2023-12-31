from datetime import datetime
from typing import List

class Expense:
    def __init__(
            self,
            date:datetime,
            amount,
            reason,
            category,
            source,
            task,
            ):
        self.date = date
        self.amount = int(amount)
        self.reason = str(reason).upper()
        self.category = str(category).upper()
        self.source = str(source).upper()
        self.task = task

    def short_print(self):
        return f"""DATE_TIME:{self.date}|AMOUNT:{self.amount}|{str(self.category).upper()}|{self.reason}|{self.source}"""

    def __str__(self) -> str:
        return self.short_print(self)

    def to_values(self) -> List[str]:
        return [self.date.strftime("%d/%m/%Y,%H:%M:%S"), self.reason, self.category, self.source, self.amount]