import os

import requests

from dotenv import load_dotenv

load_dotenv('.env')

# 获取站点地址
URL = os.getenv('URL')
# 获取 MCSM APIKEY
APIKEY = os.getenv('APIKEY')


# 判断访问请求
def request_judge(result_status):
    status_map = {
        200: True,
        400: '请求函数错误',
        403: '权限不足',
        500: '服务器内部错误'
    }

    try:
        if status_map[result_status] is None:
            return '请求错误'
        else:
            return status_map[result_status]

    except requests.exceptions.RequestException as e:
        print('发生错误: ', e)
        return '请求错误，请检查后台予以寻求帮助'


# 判断实例状态
def status_judge(status_data):
    status_map = {
        -1: '未知',
        0: '关闭',
        1: '正在关闭',
        2: '正在启动',
        3: '启动'
    }

    if status_map[status_data] is None:
        return '返回错误'
    else:
        return status_map[status_data]


def true_false_judge(data):
    data_map = {
        True: '是',
        False: '否'
    }

    if data_map[data] is None:
        return '返回错误'
    else:
        return data_map[data]


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
        daemon_id = target_data['daemonId']
        instance_id = target_data['uuid']

        if action_value == 'start':
            response = requests.get(
                URL + '/api/protected_instance/open?apikey=' + APIKEY + '&uuid=' + instance_id + '&daemonId=' + daemon_id
            )

        if action_value == 'restart':
            response = requests.get(
                URL + '/api/protected_instance/restart?apikey=' + APIKEY + '&uuid=' + instance_id + '&daemonId=' + daemon_id
            )

        if action_value == 'stop':
            response = requests.get(
                URL + '/api/protected_instance/kill?apikey=' + APIKEY + '&uuid=' + instance_id + '&daemonId=' + daemon_id
            )

        if action_value == 'kill':
            response = requests.get(
                URL + '/api/protected_instance/kill?apikey=' + APIKEY + '&uuid=' + instance_id + '&remote_uuid=' + daemon_id
            )

        original = response.json()

        # 调用函数判断返回
        result_judge = request_judge(original['status'])

        if result_judge is True:
            result = f'已 {action_name} **| 实例：** {instance_name}'

        else:
            result = result_judge

    except Exception as e:
        print('发生错误：', e)
        result = '发生错误，请检查控制台获取更多信息'

    return result


def check_instance(instance_name):
    update()

    try:
        target_data = instance_nodes[instance_name]
        instance_uuid = target_data['uuid']
        daemon_id = target_data['daemonId']

        response = requests.get(
            URL + '/api/instance?apikey=' + APIKEY + '&uuid=' + instance_uuid + '&daemonId=' + daemon_id
        )

        original = response.json()

        result_request = request_judge(original['status'])

        data = original['data']

        if result_request is True:
            nickname = data['config']['nickname']
            status = status_judge(data['status'])
            start_command = data['config']['startCommand']
            stop_command = data['config']['stopCommand']
            file_code = data['config']['fileCode']
            auto_start = true_false_judge(data['config']['eventTask']['autoStart'])
            auto_restart = true_false_judge(data['config']['eventTask']['autoRestart'])

            result = f"""
                ### 实例: {nickname}
                - **状态:** {status}
                - **启动命令:** `{start_command}`
                - **暂停命令:** `{stop_command}`
                - **文件编码:** `{file_code}`
                - **是否自动启动:** {auto_start}
                - **是否自动重启:** {auto_restart}
            """

        else:
            return result_request

    except Exception as e:
        print('发生错误: ', e)
        result = '发生错误，请检查控制台获取更多信息'

    return result


def getOutput(instance_name, size):
    update()

    instance_id = instance_nodes[instance_name]['uuid']
    daemon_id = instance_nodes[instance_name]['daemonId']

    try:
        response = requests.get(
            URL + '/api/protected_instance/outputlog?apikey=' + APIKEY + '&uuid=' + instance_id + '&daemonId=' + daemon_id + '&size=' + size
        )

        data = response.json()

        request_result = request_judge(data['status'])

        if request_result is True:
            result = f"""
            ```bash
            {data['data']}
            ```
            """
        else:
            return request_result

    except Exception as e:
        print('发生错误: ', e)
        result = '发生错误，请检查控制台获取更多信息'

    return result


def sendCommand(instance_name, command):
    update()

    instance_id = instance_nodes[instance_name]['uuid']
    daemon_id = instance_nodes[instance_name]['daemonId']

    try:
        response = requests.get(
            URL + '/api/protected_instance/command?apikey=' + APIKEY + '&uuid=' + instance_id + '&daemonId=' + daemon_id + '&commands' + command
        )

        data = response.json()

        request_result = request_judge(data['status'])

        if request_result is True:
            result = f'已发送 | {instance_name}'
        else:
            result = data['data']


    except Exception as e:
        print('发生错误', e)
        result = '发生错误，请检查控制台获取更多信息'

    return result