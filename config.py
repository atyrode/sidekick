import base64
import os

from dotenv import load_dotenv
from ollama import Client

load_dotenv()

MODEL = {
    "deepseek": {
        "1.5b": "deepseek-r1:1.5b",
        "7b": "deepseek-r1",
        "8b": "deepseek-r1:8b",
        "14b": "deepseek-r1:14b",
        "32b": "deepseek-r1:32b",
    }
}
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

# Create basic auth header
credentials = f"{USERNAME}:{PASSWORD}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
auth_header = f"Basic {encoded_credentials}"

ollama = Client(
    host=f'http://{HOST}:{str(PORT)}/',
    headers={
        'Authorization': auth_header,
    }
)