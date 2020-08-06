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
            content = ''.join(i for i in aba())
            if data.get('type') == 'GroupMessage' and '阿巴' in message:
                msg = {
                    'action': 'send_group_msg',
                    'params': {
                        'group_id': data.get('group_id'),
                        'message': content
                    }
                }
                print(msg)
                ws.send(dumps(msg))
            elif data.get('type') == 'PrivateMessage' and '阿巴' in message:
                msg = {
                    "action": "send_private_msg",
                    "params": {
                        "user_id": data.get('user_id'),
                        "message": content
                    }
                }
                print(msg)
                ws.send(dumps(msg))

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5701), application=app, handler_class=WebSocketHandler)
    print('server started')
    server.serve_forever()
