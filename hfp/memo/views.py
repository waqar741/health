from django.shortcuts import render
from .models import Memo
from .forms import MemoForm
from django.shortcuts import get_object_or_404,redirect
# Create your views here.
def index(request):
    return render(request, 'index.html')

def memo_list(request):
    memory =Memo.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'memory':memory})

def memo_create(request):
    if request.method== "POST":
      MemoForm(request.POST,request.FILES)
      if form.is_valid():
          memo= form.save(commit=False)
          memo.user =request.user
          memo.save()
          return redirect('memo_list')
    else:
        form =MemoForm()
    return render(request,'tweet_form.html',{'form':form})

def memo_edit(request,memo_id):
    memo=get_object_or_404(Memo,pk=memo_id,user = request.user)
    if request.method == 'POST':
        MemoForm(request.POST,request.FILES,instance=memo)
        if form.is_valid():
            memo= form.save(commit=False)
            memo.user = request.user
            memo.save()
            return redirect('memo_list')
    else:
        form =MemoForm(instance=memo)
    return render(request,'tweet_form.html',{'form':form})