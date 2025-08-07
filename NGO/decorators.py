from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import redirect

def jwt_required(view_func):
    def wrapper(request, *args, **kwargs): 
        token = request.COOKIES.get('access_token')
        if not token: 
            return redirect('/ngo/login/')
        try: 
            access_token = AccessToken(token)
            # now we can access user_email and his/her password using access_token['user_email'] syntax
            request.jwt_payload = access_token ## attaching to jwt_payload for use in views 
            return view_func(request, *args, **kwargs)
        except Exception as e: 
            print("JWT error: ")
            print(e) 
            return redirect('/ngo/login')
    
    return wrapper