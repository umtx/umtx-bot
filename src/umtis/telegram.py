import requests
import logging
from .storage import DEFAULT_PATH
import os
logger = logging.getLogger()
TELEGRAM_SEND_MESSAGE = "https://api.telegram.org/bot{token}/sendMessage"


def get_credentials():
    from . import utils

    from .storage import local as local_storage
    if not local_storage.check_file_exist(
            f"{DEFAULT_PATH}/credentials/telegram.json"):
        logger.error("Credentials for Telegram is not found. Create empty one!")
        utils.write_json_file(f"{DEFAULT_PATH}/credentials/telegram.json", {})

    credentials = utils.load_json_file(
        f"{DEFAULT_PATH}/credentials/telegram.json")
    if ('token' not in credentials.keys()) or (not credentials['token']):
        raise Exception("Token Telegram not found")
    else:
        return credentials


def get_token(credentials=get_credentials()):
    return credentials['token']


def get_main_group(credentials=get_credentials()):
    return credentials['main_group_id']


def get_group_id_default(credentials=get_credentials()):
    return credentials['group_id']


def o_send_message(message, chat_id=get_group_id_default(), token=get_token()):
    from . import utils
    payloads = {
        'text': message,
        'chat_id': chat_id
    }
    response = requests.post(TELEGRAM_SEND_MESSAGE.format(token=token),
                             json=payloads)
    return utils.get_response(response)['ok']


def send_message(message, chat_id=get_group_id_default(), token=get_token()):
    if os.getenv("TELEGRAM_DEV") == "1" or os.getenv("TELEGRAM_DEV") == 1:
        return
    from . import utils
    payloads = {
        'text': message,
        'chat_id': chat_id
    }
    response = requests.post(TELEGRAM_SEND_MESSAGE.format(token=token),
                             json=payloads)
    # print(response.text)
    if 'ok' in utils.get_response(response):
        return utils.get_response(response)['ok']
    else:
        return False
