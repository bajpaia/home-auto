from flask import *
from flask_socketio import *
import  flask_socketio



app = Flask(__name__)
socket = SocketIO(app)

rooms = dict()
print(rooms)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register_user():
    return render_template('sign_up.html')

@app.route('/test')
def test():
    return render_template('test.html', rooms = rooms)


@app.route('/<sid>/controls')
def controls(sid):
    return render_template('room.html', room=rooms[sid])


@socket.on('connection_ack')
def acknoledge(data):
    room_name = data['name']
    socket.emit('update_home', data)
    data['code'] = request.sid
    rooms[request.sid] = data



@socket.on('process_request')
def process_request(data):
    print(data)
    socket.emit('execute_request', data,room = data['code'])


@socket.on('disconnect')
def disconnection_event():
    disconnected_client = request.sid
    print('Client disconnected {0}'.format(disconnected_client))
    if disconnected_client in rooms:
        del rooms[request.sid]
    else:
        print(rooms)
    socket.emit('update_home', {'text':'{0} disconnected'.format(request.sid)})


if __name__ == '__main__':
    socket.run(app,host='0.0.0.0')