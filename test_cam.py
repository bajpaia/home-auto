import io
import socketio
import struct
import time
import picamera


SERVER = 'http://192.168.0.201:5000'
connected = False



while not connected:
    try:
        sio.connect(SERVER)
    except Exception as e:
        print('error')
        print(e)
    else:
        connected = True
        print('connected')
        sio.emit('connection_ack', {"name":"camera"})


try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        time.sleep(2)
        stream = io.BytesIO()
        # Use the video-port for captures...

        for frame in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())

            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
