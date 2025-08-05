# this file will contain some functions 
import jwt 


SECRET_KEY = 'django-insecure-m)isy)vlw86%+lr#oc*sv*5)rt%ba9m$q$!f!hq53*v7h*=z+3'

def findCurrentUser(request):
    token = request.COOKIES.get('access_token')

    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as e: 
        print("Error in findCurrentUser() " + e)
        return None 
    
    user_id = payload.get('user_id')
    return str(user_id)