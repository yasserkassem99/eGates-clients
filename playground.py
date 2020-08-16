import eventlet
from socketio import Client,Server,WSGIApp
from Messages.ConfigMessage import ConfigMessage
import threading
import random
cio = Client()
sio = Server(cors_allowed_origins='*',always_connect=True)
app = WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

#######################################################################################
#events handlers for the connection where this device work as client for another server
######################################################################################
@cio.event
def connect():
    print('connection as client established ')
    

@cio.event
def disconnect():
    print('disconnect from server as client ')
    
    
@cio.event
def my_response(data):
    print(data,'my_event')
    print('hereeeeeeeeeeeeeeeeeeee')
    sio.emit('my_message',data)




#################################################################################
#event handlers for the connection where this device work as server for a client
#################################################################################
@sio.event
def connect(sid, environ):
    print('connect ', sid)
    

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def my_message(sid,data):
    print(data)
    cio.emit('my_event',data)


def emit_message(message,sid):
    sio.emit(event_name,message)


#start socket connection
if __name__ == '__main__':
    cio_thread = threading.Thread(target=cio.connect,args=['http://0.0.0.0:8080'])
    cio_thread.start()
    eventlet.wsgi.server(eventlet.listen(('192.168.1.10', 5000)), app)
    