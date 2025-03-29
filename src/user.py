from shared import *


def get_user_list(username, role):
    try:
        response = requests.get(f'{ADDRESS}/api/auth/search?apikey={API_KEY}', headers=headers).json()["data"]

    except Exception as e:
        print(e)
        return False
