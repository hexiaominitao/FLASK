from gevent.pywsgi import WSGIServer
from app import create_app

app = create_app('app.config.ProConfig')

server = WSGIServer(('0.0.0.0',5000),app)
server.serve_forever()