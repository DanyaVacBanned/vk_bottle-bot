import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("api_key")
group_id = int(os.getenv("group_id"))
first_admin_id = int(os.getenv("first_admin_id"))
second_admin_id = int(os.getenv("second_admin_id"))
developer_id = int(os.getenv("developer_id"))