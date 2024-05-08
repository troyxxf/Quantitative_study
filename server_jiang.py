import requests
from private_param import server_jiang_token
def server_jiang_send_message(text):
    api_url='https://sctapi.ftqq.com/{}.send'.format(server_jiang_token)
    data={
        'title':'股票信息',
        'desp':text
    }
    response = requests.post(api_url, data=data)
    return response.text

# server_jiang_send_message("test message")