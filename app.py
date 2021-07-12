from flask import *
from flask_socketio import *
import  flask_socketio
import cv2

app = Flask(__name__)
socket = SocketIO(app, async_mode='threading')
rooms = dict()





def gen_frames():  
    camera = cv2.VideoCapture("tcp://192.168.0.174:8554")
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/register')
def register_user():
    return render_template('sign_up.html')


@app.route('/home')
def home():
    return render_template('home.html', rooms = rooms)


@app.route('/<sid>/controls')
def controls(sid):
    if request.method == 'GET':
        if sid in rooms:
            return render_template('room.html', room=rooms[sid])
        return redirect(url_for('test'))


@app.route('/security')
def security():
    return render_template('camera.html')


@socket.on('connection_ack')
def acknoledge(data):
    print(data)
    room_name = data['name']
    socket.emit('update_home', data)
    data['code'] = request.sid
    rooms[request.sid] = data


@socket.on('toggle_sensors')
def activate_sensor(data):
    print('starting room sensors')
    socket.emit('toggle_room_sensors',room=data['code'])


@socket.on('process_sensor_data')
def process_sensor_data(data):
    data['code']= request.sid
    print(data)
    socket.emit('update_sensor', data)


@socket.on('process_request')
def process_request(data):
    print(data)
    socket.emit('execute_request', data,room = data['code'])

@socket.on("toggle_camera")
def toggle_camera(data):
    print("Toggle camera")
    socket.emit("start_camera", data, broadcast= True)



@socket.on('disconnect')
def disconnection_event():
    disconnected_client = request.sid
    print('Client disconnected {0}'.format(disconnected_client))
    if disconnected_client in rooms:
        del rooms[request.sid]
        socket.emit('update_home', {'text':'{0} disconnected'.format(request.sid)})
    else:
        print(rooms)
    


@socket.on('camera_stream')
def get_stream(data):
    socket.emit('cv-data', data)


@socket.on('to_camera')
def send_to_camera(data):
    socket.emit("move_camera", data)






if __name__ == '__main__':
    socket.run(app,host='0.0.0.0')