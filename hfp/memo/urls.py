from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.memo_list, name="memo_list"),
    path("create/", views.memo_create, name="memo_create"),
    path("edit/<int:pk>/", views.memo_update, name="memo_update"),
    path("delete/<int:pk>/", views.memo_delete, name="memo_delete"),
]
