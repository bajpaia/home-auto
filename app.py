from flask import *
from flask_socketio import *
import  flask_socketio
import cv2
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'home'
socket = SocketIO(app, async_mode='threading')

from db_models import *


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


def get_tasks():
    return Task.query.all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def gen_frames():  
    camera = cv2.VideoCapture("tcp://192.168.0.175:8554")
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    email = request.form.get("email")
    user = User.query.filter_by(email = email).first()
    if not user:
        flash('This email is not registered')
        return redirect(url_for('index'))  
    if not check_password_hash(user.password_hash, request.form.get('password')):
        flash('Please check login details')
        return redirect(url_for('index'))
    login_user(user)
    return redirect(url_for('home'))

@login_required
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == "GET":
        return render_template('sign_up.html')
    
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user: 
        return redirect(url_for('index'))
    new_user = User(email=email, name=name, password_hash=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('home'))


@login_required
@app.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    print(current_user.name)
    return render_template('home.html', rooms = rooms, tasks=get_tasks())



@login_required
@app.route('/edit_home', methods=['GET', 'POST'])
def edit_home():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('edit_home.html', rooms = rooms)
    if request.method == 'POST':
        print('Posting')
    for room in rooms:
        name = request.form.get(room)
        if len(name) >0:
            socket.emit("change_room_name", {"name":name}, room=room)
    return redirect(url_for('home'))

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/to-do', methods=['POST'])
def to_do():
    if len(request.form.get('todo'))>0:
        task = Task(text=request.form.get('todo'))
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('home'))


@login_required
@app.route('/delete-to-do', methods=['POST'])
def del_to_do():
    print("delete {}".format(request.form.get('todoId')))
    Task.query.filter_by(id=request.form.get('todoId')).delete()
    db.session.commit()
    return redirect(url_for('home'))


@login_required
@app.route('/<sid>/edit_room', methods=['GET', 'POST'])
def edit_room(sid):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        if sid in rooms:
            return render_template('edit_room.html', room = rooms[sid])
        else:
            return redirect(url_for('home'))
    room = rooms[sid]
    for relay in room['relays']:
        name = request.form.get(str(relay['pin']))
        if name:
            print(name)
            socket.emit("change_relay_names", {"name":name, "relay": int(relay['pin'])}, room=sid)
    return redirect(url_for('controls', sid=sid))

@login_required
@app.route('/<sid>/controls')
def controls(sid):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        if sid in rooms:
            return render_template('room.html', room=rooms[sid])
        return redirect(url_for('home'))

@login_required
@app.route('/security')
def security():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('camera.html')



@app.route('/guide')
def guide():
    return render_template('guide.html')


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