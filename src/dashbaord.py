import requests
from shared import *


def get_panel_overview():
    try:
        response = requests.get(f'{ADDRESS}/api/overview', headers=headers).json()["data"]

        return {
            "cpu": round(response["system"]["cpu"]),
            "freemem": bytes_gigabytes(response["system"]["freemem"]),
            "totalmem": bytes_gigabytes(response["system"]["totalmem"]),
            "availableRemote": response["system"]["remoteCount"]["available"],
            "totalRemote": response["system"]["remoteCount"]["total"],
            "version": response["version"],
            "logined": response["record"]["logined"],
            "illegalAccess": response["record"]["illegalAccess"],
            "banips": response["record"]["banips"],
            "loginFailed": response["record"]["loginFailed"],
            "totalInstance": response["chart"]["request"][0]["totalInstance"],
            "runningInstance": response["chart"]["request"][0]["runningInstance"],
        }
    except Exception as e:
        print(e)
        return


def get_daemon_overview(number):
    if number is None:
        number = 0

    try:
        response = requests.get(f'{ADDRESS}/api/overview').json()["data"]["remote"][number]

        return {
            "version": response["version"],
            "cpu": round(response["system"]["cpu"]),
            "freemem": bytes_gigabytes(response["system"]["freemem"]),
            "totalmem": bytes_gigabytes(response["system"]["totalmem"]),
            "totalInstance": response["instance"]["total"],
            "runningInstance": response["instance"]["running"],
            "uuid": response["uuid"],
            "ip": response["ip"],
            "port": response["port"],
            "available": true_false_tran(response["available"]),
            "remark": response["remark"],
        }
    except Exception as e:
        print(e)
        return False
