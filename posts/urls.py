from django.urls import path
from . import views
from django.conf.urls import url

app_name = "posts"


urlpatterns = [
	path('create/', views.PostCreate.as_view(), name="createpost"),
    path('explore/', views.Postlist.as_view(), name="listpost"),
]