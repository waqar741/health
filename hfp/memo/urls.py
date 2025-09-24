from . import views
from

urlpatterns = [
    path('/views',views.index,name='index'),
]
