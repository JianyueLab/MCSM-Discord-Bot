import os
import requests

URL = os.getenv('URL')
APIKEY = os.getenv('APIKEY')

pre = []

def getAll(index):
    response = requests.get(URL + '/api/service/remote_services?apikey=' + APIKEY)
    data = response.json()

    try:
        if data["status"] == 200:
            daemon_data = data['data'][index]
            daemon_id = daemon_data['uuid']
            daemon_nickname = daemon_data['remarks']
            instance_data = daemon_data['instances']
            for instance in instance_data:
                instance_uuid = instance['instanceUuid']
                instance_nickname = instance['config']['nickname']
                if daemon_id and daemon_nickname:
                    daemon_result = (f'**节点: ** {daemon_nickname}, **节点ID: ** {daemon_id} \n-----------------------------\n')
                    pre.append(f'**实例：** {instance_nickname}, **实例ID: ** {instance_uuid}')
                    result = daemon_result + '\n-----------------------------\n'.join(pre)
            return result
                
        elif data["status"] == 400:
            result = '请求函数错误'
            return result
        elif data["status"] == 403:
            result = '权限不足'
            return result
        elif data["status"] == 500:
            result = '服务器内部问题'
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f'发生错误：{e}')
        return None
