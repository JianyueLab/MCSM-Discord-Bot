import os
import requests

URL = os.getenv('URL')
APIKEY = os.getenv('APIKEY')

def status_judge(status_data):
    if status_data == -1:
        status = '未知'
    elif status_data == 0:
        status = '关闭'
    elif status_data == 1:
        status = '正在关闭'
    elif status_data == 2:
        status = '正在启动'
    elif status_data == 3:
        status = '启动'
    else:
        status = '状态错误'

    return status

def request_judge(result_status):
    try:
        if result_status == 200:
            judge_result = True
        elif result_status == 400:
            judge_result = '请求函数错误'

        elif result_status == 403:
            judge_result = '权限不足'

        elif result_status == 500:
            judge_result = '服务器内部问题'

        else:
            judge_result = '请求错误'
    
    except requests.exceptions.RequestException as e:
        judge_result = '请求错误，检查日志予以获取帮助'

    return judge_result

def update():
    global instance_nodes
    # 获取json
    response = requests.get(URL + '/api/service/remote_services?apikey=' + APIKEY)
    # 分析json
    original = response.json()
    # 重置词典
    instance_nodes = {}

    result_status = original['status']
    
    # 调用函数判断返回
    result_judge = request_judge(result_status)
    
    if result_judge == True:
        for data in original['data']:
            instances = data['instances']
            for instance in instances:
                nickname = instance['config']['nickname']
                instance_uuid = instance['instanceUuid']
                
                status_data = instance['status']
                
                # 调用函数判断状态
                status = status_judge(status_data)
                    
                daemon_uuid = data['uuid']
                # 存入字典
                instance_nodes[nickname] = {'uuid': instance_uuid, 'daemonId': daemon_uuid, 'status': status}

                result = '成功获取实例列表'
            
    else:
        result = result_judge
        
    return result

def list_all():
    # 获取json
    response = requests.get(URL + '/api/service/remote_services?apikey=' + APIKEY)
    # 分析json
    original = response.json()
    # 重置词典
    instance_nodes = {}
    
    final = []

    try:
        if original["status"] == 200:
            for data in original['data']:
                instances = data['instances']
                for instance in instances:
                    nickname = instance['config']['nickname']
                    instance_uuid = instance['instanceUuid']
                    
                    status_data = instance['status']
                    
                    status = status_judge(status_data)
                        
                    daemon_uuid = data['uuid']
                    # 存入字典
                    instance_nodes[nickname] = {'uuid': instance_uuid, 'daemonId': daemon_uuid, 'status': status}
                    # 将昵称添加到 final 列表中
                    final.append(f'**实例: ** {nickname}\n- **状态: ** {status}')

                    result = '\n-------------------\n'.join(final)
            
        elif original["status"] == 400:
            result = '请求函数错误'

        elif original["status"] == 403:
            result = '权限不足'

        elif original["status"] == 500:
            result = '服务器内部问题'

        else:
            result = '请求错误'
    
    except requests.exceptions.RequestException as e:
        result = '请求错误，检查日志予以获取帮助'
        
    return result

def instance_control(action, instance_name):
    action_value = action.value
    action_name = action.name

    target_name = instance_name
    
    try: 
        target_data = instance_nodes[target_name]
        daemonid = target_data['daemonId']
        instanceid = target_data['uuid']
        
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
            result = f'正常 {action_name} **| 实例：** {target_name}'
            
        elif data['status'] == 400:
            result = '请求参数不正确'
            
        elif data['status'] == 403:
            result = '无权限'
            
        else:
            result = '返回错误'
            
    except:
        result = '命令错误'

    return result