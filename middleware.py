# from werkzeug.wrappers import Request, Response

# class Middleware():
#     def __init__(self,app) :
#         self.app = app 
#         self.username ='usuario'
#         self.password = 'password'

# def __call__ (self, environ, start,response):
#     Request= Request(environ)
#     username= request.authorrizantion ['usuario']
#     password= request.authorrizantion ['password']
    
#     if username == self.username and password == self.password:
#        environ['usuario'] = {
#            'name' : 'usuario'
#        }
#        return self.app (environ, start_response)
#     res = response


from werkzeug.wrappers import Request, Response

class Middleware:
    def __init__(self, app):
        self.app = app
        self.username = 'usuario'
        self.password = 'password'

    def __call__(self, environ, start_response):
        request = Request(environ)
        auth = request.authorization
        
        if auth and auth.username == self.username and auth.password == self.password:
            environ['usuario'] = {
                'name': 'usuario'
            }
            return self.app(environ, start_response)
        
        res = Response('Unauthorized', status=401)
        return res(environ, start_response)
