from abaGEN import aba
from flask import Flask,request
from json import loads
import requests

bot_server = Flask(__name__)

@bot_server.route('/api/messages',methods = ['POST'])

def server():
    data = request.get_data().decode('utf-8')
    data = loads(data)
    print(data)
    message = data['message'] #由于不同版本，返回的数据类型不相类似，根据实际情况自行更改
    if data['type'] == 'GroupMessage' and '阿巴' in message:
        group = data['group_id']
        abaGPost(group)
        print(group)
    elif data['type'] == 'PrivateMessage' and '阿巴' in message:
        user = data['user_id']
        abaPPost(user)
        print(user)
    return ''#必须有返回值，否则报错

def abaGPost(group):
    content = ''.join(i for i in aba())
    data = {"group_id": group, "message": content}
    requests.post('http://localhost:5700/ws/send_group_msg', data)

def abaPPost(user):
    content = ''.join(i for i in aba())
    data = {"user_id": user, "message": content}
    requests.post('http://localhost:5700/ws/send_private_msg', data)

if __name__ == "__main__":
    bot_server.run(port=5701)
