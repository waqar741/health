from . import views
from django.urls import path

urlpatterns = [
    path('',views.memo_list,name='memo_list'),
    path('create/',views.memo_create,name='memo_create'),
    path('<int:memo_id>/delete/',views.memo_delete,name='memo_delete'),
    path('<int:memo_id>/edit/',views.memo_edit,name='memo_edit'),
    path('register/',views.register,name='register'),
]
