from werkzeug.wrappers import Request, Response

class Middleware():
    def __init__(self,app) :
        self.app = app 
        self.username ='usuario'
        self.password = 'password'

def __call__ (self, environ, start,response):
    Request= Request(environ)
    username= request.authorrizantion ['usuario']
    password= request.authorrizantion ['password']
    
    if username == self.username and password == self.password:
       environ['usuario'] = {
           'name' : 'usuario'
       }
       return self.app (environ, start_response)
    res = response