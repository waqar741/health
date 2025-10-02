from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from .forms import  MemoForm
import requests
# from django.contrib import messages

API_TOKEN_URL = "http://127.0.0.1:8001/api/token/"
API_REGISTER_URL = "http://127.0.0.1:8001/api/register/"
API_BASE = "http://127.0.0.1:8001/api/memos/"
API_USERS = "http://127.0.0.1:8001/api/users/"


def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = requests.post(API_TOKEN_URL, data={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access"]
            refresh_token = tokens["refresh"]
            response = redirect("memo_list")
            response.set_cookie("access_token", access_token, httponly=True, samesite="Strict")
            response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")
            return response
        else:
            error = "Invalid username or password"

        return render(request, "registration/login.html", {"error": error})

    return render(request, "registration/login.html")

def memo_list(request):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return redirect("login")
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(API_BASE, headers=headers)
    memos = []
    if res.ok:
        memos = res.json()
    else:
        messages.error(request, f"Could not fetch memos. API responded with status {res.status_code}.")
    return render(request, "memo_list.html", {"memos": memos})


def memo_create(request):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return redirect("login")
    
    if request.method == "POST":
        form = MemoForm(request.POST, request.FILES)
        if form.is_valid():
            headers = {"Authorization": f"Bearer {access_token}"}
            data = {
                "title": form.cleaned_data["title"],
                "content": form.cleaned_data["content"] or ""
            }
            files = {}
            if form.cleaned_data.get("photo"):
                photo = request.FILES["photo"]
                files = {"photo": (photo.name, photo.read(), photo.content_type)}
            res = requests.post(API_BASE, headers=headers, data=data, files=files)

            if res.status_code == 201:
                return redirect("memo_list")
            else:
                messages.error(request, f"API error: {res.status_code} {res.text}")
    else:
        form = MemoForm()
    return render(request, "memo_form.html", {"form": form, "action": "Create"})

def memo_update(request, pk):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{API_BASE}{pk}/"
    res = requests.get(url, headers=headers)
    if not res.ok:
        messages.error(request, "Could not fetch memo to edit.")
        return redirect("memo_list")
    memo = res.json()

    if request.method == "POST":
        form = MemoForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                "title": form.cleaned_data["title"],
                "content": form.cleaned_data["content"] or ""
            }
            files = None
            if form.cleaned_data.get("photo"):
                photo = request.FILES["photo"]
                files = {"photo": (photo.name, photo.read(), photo.content_type)}
            res2 = requests.put(url, headers=headers, data=data, files=files)
            if res2.ok:
                return redirect("memo_list")
            else:
                messages.error(request, f"API update error: {res2.status_code} {res2.text}")
    else:
        form = MemoForm(initial={"title": memo.get("title"), "content": memo.get("content")})
    
    return render(request, "memo_form.html", {"form": form, "action": "Update"})


def memo_delete(request, pk):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{API_BASE}{pk}/"

    if request.method == "POST":
        response = requests.delete(url, headers=headers)
        if response.status_code in [200, 204]:
            return redirect("memo_list")
        else:
            error = response.text
            return render(request, "memo_confirm_delete.html", {"error": error})

    return render(request, "memo_confirm_delete.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        response = requests.post(API_REGISTER_URL, data={
            "username": username,
            "password": password,
            "email": email
        })

        if response.status_code == 201:
            return redirect("memo:login")
        else:
            error = response.json().get("error", "Registration failed")
            return render(request, "registration/register.html", {"error": error})

    return render(request, "registration/register.html")


def logout_view(request):
    response = redirect("login")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token") 
    return response 