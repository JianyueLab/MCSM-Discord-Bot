import os
import requests

# 获取站点地址
URL = os.getenv('URL')
# 获取 MCSM APIKEY
APIKEY = os.getenv('APIKEY')

# 判断访问请求
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
        print({e})
        judge_result = '请求错误，检查日志予以获取帮助'

    return judge_result

# 判断实例状态
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

# 更新
def update():
    global instance_nodes
    # 获取json
    response = requests.get(URL + '/api/service/remote_services?apikey=' + APIKEY)
    # 分析json
    original = response.json()
    # 重置词典
    instance_nodes = {}

    # 调用函数判断返回
    result_judge = request_judge(original['status'])
    
    if result_judge is True:
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

                result = '成功获取实例信息'
            
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
    
    # 调用函数判断返回
    result_judge = request_judge(original['status'])
    
    if result_judge is True:
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
    
    else:
        result = result_judge

    return result

def instance_control(action, instance_name):
    action_value = action.value
    action_name = action.name
    
    try: 
        target_data = instance_nodes[instance_name]
        daemonid = target_data['daemonId']
        instanceid = target_data['uuid']
        
        if action_value == 'start':
            response = requests.get(URL + '/api/protected_instance/open?apikey=' + APIKEY + '&uuid=' + instanceid + '&daemonId=' + daemonid)
            original = response.json()
        
        if action_value == 'restart':
            response = requests.get(URL + '/api/protected_instance/restart?apikey=' + APIKEY + '&uuid=' + instanceid + '&daemonId=' + daemonid)
            original = response.json()

        if action_value == 'stop':
            response = requests.get(URL + '/api/protected_instance/kill?apikey=' + APIKEY + '&uuid=' + instanceid + '&daemonId=' + daemonid)
            original = response.json()
        
        # 调用函数判断返回
        result_judge = request_judge(original['status'])
        
        if result_judge is True:
            result = f'已 {action_name} **| 实例：** {instance_name}'
        
        else:
            result = result_judge
            
    except:
        result = '命令错误'

    return result

def check_instance(instance_name):
    result_update = update()
    
    try:
        if result_update == '成功获取实例信息':
            target_data = instance_nodes[instance_name]
            instance_status = target_data['status']
            instance_uuid = target_data['uuid']

            result = f'**实例：** {instance_name}\n- **uuid: ** {instance_uuid}\n- **状态: ** {instance_status}'
            
        else:
            result = result_update
      
    except:
        result = '命令错误'
        
    return result