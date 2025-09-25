from django.shortcuts import render
from .models import Memo
from .forms import MemoForm ,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def memo_list(request):
    memos =Memo.objects.all().order_by('-created_at')
    return render(request,'memo_list.html',{'memos':memos})

@login_required
def memo_create(request):
    if request.method== "POST":
      form = MemoForm(request.POST,request.FILES)
      if form.is_valid():
          memo= form.save(commit=False)
          memo.user =request.user
          memo.save()
          return redirect('memo_list')
    else:
        form =MemoForm()
    return render(request,'memo_form.html',{'form':form})

@login_required
def memo_edit(request,memo_id):
    memo=get_object_or_404(Memo,pk=memo_id,user = request.user)
    if request.method == 'POST':
        form = MemoForm(request.POST,request.FILES,instance=memo)
        if form.is_valid():
            memo= form.save(commit=False)
            memo.user = request.user
            memo.save()
            return redirect('memo_list')
    else:
        form =MemoForm(instance=memo)
    return render(request,'memo_form.html',{'form':form})

@login_required
def memo_delete(request,memo_id):
    memo=get_object_or_404(Memo,pk=memo_id,user = request.user)
    if request.method == 'POST':
        memo.delete()
        return redirect('memo_list')
    return render(request,'memo_confirm_delete.html',{'memo':memo})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('memo_list')
    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')