import eventlet
from socketio import Client,Server,WSGIApp
from Messages.ConfigMessage import ConfigMessage
from clientSocket import ClientSocket
from Messages.message_types import *




# client to server socket
client = None
# socket as server
sio = Server(cors_allowed_origins='*')
app = WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})




#################################################################################
#event handlers for the connection where this device work as server for a client
#################################################################################
@sio.event
def connect(sid, environ):
    global client
    client = ClientSocket()
    print('connect ', sid)
    configMessage = ConfigMessage()
    configMessage.set_type(CLIENT_CONFIG_MESSAGE)
    client.send_msg(configMessage.json())
    

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    
    
@sio.event
def my_message(sid, environ):
    print('my_message ', sid)
    configMessage = ConfigMessage()
    configMessage.set_type(CLIENT_CONFIG_MESSAGE)
    client.send_msg(configMessage.json())
    



#start socket connection
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('192.168.1.10', 5001)), app)
