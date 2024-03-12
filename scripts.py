import requests
from settings import URL, APIKEY

def getAll():
    response = requests.get(str(URL) + '/api/service/remote_services?apikey=' + str(APIKEY))
    data = response.json()
    
    pre = []
    
    try:
        if data["status"] == 200:
            for item in data['data']:
                uuid = item.get('uuid')
                remarks = item.get('remarks')
                if uuid and remarks:
                    pre.append(f'**UUID:** {uuid}, **昵称:** {remarks}')
                    result = '\n'.join(pre)
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