from flask import *
from flask_socketio import *
import  flask_socketio
import cv2


app = Flask(__name__)
socket = SocketIO(app, async_mode='threading')
rooms = dict()
camera_active = False

def cam_toggle():
    global camera_active
    if camera_active:
        camera_active = False
        print("off")
    else:
        camera_active = True
        print("on")


def gen_frames():  
    camera = cv2.VideoCapture("tcp://192.168.0.174:8554")
    while camera_active:
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



@app.route('/edit_home', methods=['GET', 'POST'])
def edit_home():
    if request.method == 'GET':
        return render_template('edit_home.html', rooms = rooms)
    for room in rooms:
        name = request.form.get(room)
        if len(name) >0:
            socket.emit("change_room_name", {"name":name}, room=room)
    return redirect(url_for('home'))


@app.route('/<sid>/edit_room', methods=['GET', 'POST'])
def edit_room(sid):
    if request.method == 'GET':
        return render_template('edit_room.html', room = rooms[sid])
    room = rooms[sid]
    for relay in room['relays']:
        name = request.form.get(str(relay['pin']))
        if name:
            print(name)
            socket.emit("change_relay_names", {"name":name, "relay": int(relay['pin'])}, room=sid)
    return redirect(url_for('controls', sid=sid))


@app.route('/<sid>/controls')
def controls(sid):
    if request.method == 'GET':
        if sid in rooms:
            return render_template('room.html', room=rooms[sid])
        return redirect(url_for('home'))


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
    print('sending request')
    socket.emit('execute_request', data,room = data['code'])

@socket.on("toggle_camera")
def toggle_camera(data):
    print("Toggle camera")
    cam_toggle()




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