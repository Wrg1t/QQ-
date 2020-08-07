from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from json import loads, dumps
from abaGEN import aba

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/api/messages')
def server(ws):
    while not ws.closed:
        data = loads(ws.receive())
        if data:
            message = data.get('raw_message')
            if data.get('type') == 'GroupMessage' and '阿巴' in message:
                sendGMsg(ws, data.get('group_id'), aba())
            elif data.get('type') == 'PrivateMessage' and '阿巴' in message:
                sendPMsg(ws, data.get('user_id'), aba())
    return data

def sendGMsg(ws, group_id, msg):
    msg = {
        'action': 'send_group_msg',
        'params': {
            'group_id': group_id,
            'message': msg
        }
    }
    print(msg)
    ws.send(dumps(msg))

def sendPMsg(ws, user_id, msg):
    msg = {
        "action": "send_private_msg",
        "params": {
            "user_id": user_id,
            "message": msg
        }
    }
    print(msg)
    ws.send(dumps(msg))

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5701), application=app, handler_class=WebSocketHandler)
    print('Server Started')
    server.serve_forever()
