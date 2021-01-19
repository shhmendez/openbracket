
from clastic.middleware.cookie import SignedCookieMiddleware
from clastic import Response, Middleware
import os
import json

def render_raw(context):
    res = Response(context)
    return res
def render_raw_json(context):
    res = Response(json.dumps(context))
    return res
class RenderRawJson(Middleware):
    def request(self,next):
        # res = next()
        return Response()

class Unpack(Middleware):
    def __init__(self,*params):
        self.params = params
        self.provides = tuple(self.params)
    def request(self,next,request):
        data = json.loads(request.data.decode("utf-8"))
        #add check for correct data shape
        res = next(**data)
        return res



class Cors(Middleware):
    def request(self, next, request):
        res = next()
        if(type(res) != Response):
            try:
                res = json.dumps(res)
            except:
                pass
            res = Response(res)
        

        #find more specific implementation 
        base_url = request.origin
        res.headers['Access-Control-Allow-Origin'] = base_url
        res.headers['Access-Control-Allow-Headers'] = "content-type"
        res.headers['Access-Control-Allow-Credentials'] = 'true'
        return res

#A cache here could help 
class Uncookie(Middleware):
    def __init__(self,cookie_name):
        pass
    def request(self):
        pass
class UserSession(Middleware):
    provides = ('user',)
    def request(self,next, user_model,request, cookie,username=None): 
        print(f'cookies in request {cookie}')
        if not username:
            username = cookie['username']
        #perform validation on usersession here
        #cookie is a map containing {username} 
        #it's safety is up to question
        #assuming a trustable cookie
        # username can be used to generate a `User` database object
         
        response = next({"user": user_model.objects(username=username)})
        # for (k,v) in cookie.items():
        #     response.set_cookie(k,v)
        
        # print("who: {}".format(cook))
        return response

class BoardProvider(Middleware):
    provides = ('board',)
    def request(self,next,board_model,board_id):
        board = board_model.objects(_id=board_id) 
        response = next(board=board)
        print(response)
        return response


class GameListProvider(Middleware):
    provides = ('gameList',)
    def __init__(self, Board,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Board = Board
    def request(self,next,user):
        bl = self.Board.object(_id__in=user.game_id_list)
        response = next(gameList=bl)
        return response

