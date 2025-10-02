# memo/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, NoteForm
from . import api_client
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            tokens = api_client.obtain_token(form.cleaned_data["username"], form.cleaned_data["password"])
            if tokens and "access" in tokens:
                request.session["access"] = tokens["access"]
                request.session["refresh"] = tokens.get("refresh")
                return redirect("memo_list")
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    request.session.pop("access", None)
    request.session.pop("refresh", None)
    return redirect("login")

def memo_list(request):
    # ensure logged in
    if not request.session.get("access"):
        return redirect("login")
    res = api_client.api_request(request, "GET", "api/notes/")
    notes = res.json() if res.ok else []
    return render(request, "memo_list.html", {"notes": notes})

def memo_create(request):
    if not request.session.get("access"):
        return redirect("login")
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                "title": form.cleaned_data["title"],
                "content": form.cleaned_data["content"] or ""
            }
            files = None
            if form.cleaned_data.get("photo"):
                photo = request.FILES["photo"]
                # requests expects file tuple or file-like; we'll send tuple (filename, bytes, content_type)
                files = {"photo": (photo.name, photo.read(), photo.content_type)}
            res = api_client.api_request(request, "POST", "api/notes/", data=data, files=files)
            if res.status_code in (200, 201):
                return redirect("memo_list")
            else:
                # show server error
                messages.error(request, f"API error: {res.status_code} {res.text}")
    else:
        form = NoteForm()
    return render(request, "memo_form.html", {"form": form, "action": "Create"})

def memo_update(request, pk):
    if not request.session.get("access"):
        return redirect("login")
    # fetch note to prefill form
    res = api_client.api_request(request, "GET", f"api/notes/{pk}/")
    if not res.ok:
        messages.error(request, "Could not fetch note")
        return redirect("memo_list")
    note = res.json()
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                "title": form.cleaned_data["title"],
                "content": form.cleaned_data["content"] or ""
            }
            files = None
            if form.cleaned_data.get("photo"):
                photo = request.FILES["photo"]
                files = {"photo": (photo.name, photo.read(), photo.content_type)}
            res2 = api_client.api_request(request, "PUT", f"api/notes/{pk}/", data=data, files=files)
            if res2.ok:
                return redirect("memo_list")
            messages.error(request, f"API error: {res2.status_code} {res2.text}")
    else:
        form = NoteForm(initial={"title": note.get("title"), "content": note.get("content")})
    return render(request, "memo_form.html", {"form": form, "action": "Update"})

def memo_delete(request, pk):
    if not request.session.get("access"):
        return redirect("login")
    if request.method == "POST":
        res = api_client.api_request(request, "DELETE", f"api/notes/{pk}/")
        if res.status_code in (204, 200):
            messages.success(request, "Deleted")
        else:
            messages.error(request, f"Delete failed: {res.status_code}")
        return redirect("memo_list")
    # optional: show confirmation page
    res = api_client.api_request(request, "GET", f"api/notes/{pk}/")
    note = res.json() if res.ok else {}
    return render(request, "memo_confirm_delete.html", {"note": note})
