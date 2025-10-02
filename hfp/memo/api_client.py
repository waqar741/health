import requests
from django.conf import settings

API_BASE = settings.API_BASE_URL.rstrip("/") + "/"

TOKEN_URL = API_BASE + "api/token/"
REFRESH_URL = API_BASE + "api/token/refresh/"

def obtain_token(username: str, password: str):
    r = requests.post(TOKEN_URL, data={"username": username, "password": password})
    if r.ok:
        return r.json() 
    return None

def refresh_access_token(refresh_token: str):
    r = requests.post(REFRESH_URL, data={"refresh": refresh_token})
    if r.ok:
        return r.json()  
    return None

def get_auth_header(request):
    access = request.session.get("access")
    if access:
        return {"Authorization": f"Bearer {access}"}
    return {}

def api_request(request, method, path, data=None, params=None, files=None, json=None, stream=False):
    url = API_BASE + path.lstrip("/")
    headers = get_auth_header(request)  


    r = requests.request(method, url, headers=headers, data=data, params=params, files=files, json=json, stream=stream)

    
    if r.status_code in (401, 403):
        refresh = request.session.get("refresh")
        if refresh:
            new = refresh_access_token(refresh)
            if new and "access" in new:
                request.session["access"] = new["access"]
                headers = get_auth_header(request)
                r = requests.request(method, url, headers=headers, data=data, params=params, files=files, json=json, stream=stream)

    return r
