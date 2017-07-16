import json
import os

def load_token(file_path='token.json'):
    with open(file_path, 'r') as file:
        token = json.load(file)
    return token.get('token')

TELEGRAM_BOT_KEY  = load_token()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "logs/logs.log")