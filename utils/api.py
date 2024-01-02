from todoist_api_python.api import TodoistAPI
from custom_logger import get_logger

logger = get_logger(__name__)

def get_tasks(api:TodoistAPI, project_id, is_completed = False):
    tasks = api.get_tasks(project_id=project_id)
    return tasks

def get_projects(api:TodoistAPI):
    return api.get_projects()

def get_user_choice(options):
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def choose_project(api:TodoistAPI):
    projects = get_projects(api)
    for index, proj in enumerate(projects, 1):
        print(f"{index}|{proj.name}")
    project = get_user_choice(projects)
    logger.info("Choosen Project: ",project)
    return project