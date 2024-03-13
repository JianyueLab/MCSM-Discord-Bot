import os
import requests

URL = os.getenv('URL')
APIKEY = os.getenv('APIKEY')

def getAll(index):
    response = requests.get(URL + '/api/service/remote_services?apikey=' + APIKEY)
    data = response.json()

    pre = []
    
    try:
        if data["status"] == 200:
            daemon_data = data['data'][index]
            daemon_id = daemon_data['uuid']
            daemon_nickname = daemon_data['remarks']
            if daemon_id and daemon_nickname:
                instance_data = daemon_data['instances']
                daemon_result = (f'- **节点: ** {daemon_nickname}\n- **节点ID: ** {daemon_id} \n-----------------------------\n')
                for instances in instance_data:
                    instance_uuid = instances['instanceUuid']
                    instance_nickname = instances['config']['nickname']
                    instance_status_data = instances['status']
                    if instance_status_data == -1:
                        instance_status = '未知'
                    elif instance_status_data == 0:
                        instance_status = '关闭'
                    elif instance_status_data == 1:
                        instance_status = '正在关闭'
                    elif instance_status_data == 2:
                        instance_status = '正在启动'
                    elif instance_status_data == 3:
                        instance_status = '启动'
                    else:
                        instance_status = '返回错误'
                    pre.append(f'- **实例：** {instance_nickname}\n- **实例ID: ** {instance_uuid}\n- **状态: ** {instance_status}')
                result = daemon_result + '\n-----------------------------\n'.join(pre)
                
            else: 
                result = '返回错误'
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

def instance_control(action, daemonid, instanceid):
    action_value = action.value
    action_name = action.name
    
    print(action_value)
    
    if action_value == 'start':
        response = requests.get(URL + '/api/protected_instance/open?apikey=' + APIKEY + '&uuid=' + instanceid + '&daemonId=' + daemonid)
        data = response.json()
    
    if action_value == 'restart':
        response = requests.get(URL + '/api/protected_instance/restart?apikey=' + APIKEY + '&uuid=' + instanceid + '&daemonId=' + daemonid)
        data = response.json()

    if action_value == 'stop':
        response = requests.get(URL + '/api/protected_instance/kill?apikey=' + APIKEY + '&uuid=' + instanceid + '&daemonId=' + daemonid)
        data = response.json()
    
    if data['status'] == 200:
        result = f'正常{action_name}'
        
    elif data['status'] == 400:
        result = '请求参数不正确'
        
    elif data['status'] == 403:
        result = '无权限'
        
    else:
        result = '返回错误'

    return result