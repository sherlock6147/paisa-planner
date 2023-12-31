import datetime as dt
from gspread.exceptions import WorksheetNotFound
import gspread
import os

def status_update(sheet_url:str):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(script_directory, 'service_account.json')
    service_account = gspread.service_account(filename=service_account_path)
    sheet = service_account.open_by_url(sheet_url)
    status_sheet = None
    try:
        status_sheet = sheet.worksheet("STATUS")
    except WorksheetNotFound:
        status_sheet = sheet.add_worksheet("STATUS",0,0)
        status_sheet.append_row(['LAST UPDATE ON'])
    dt_India_aware = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30)))
    last_update_on = dt_India_aware
    last_update_str = f"{dt_India_aware:%d-%b-%y %H:%M:%S}"
    status_sheet.update_acell('B1',last_update_str)