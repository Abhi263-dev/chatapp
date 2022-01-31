from django.urls import path
from . import views
from django.conf.urls import url

app_name = "profiles"


urlpatterns = [
	path('register/', views.RegisterView.as_view(), name="register"),
	path('login/', views.LoginView.as_view(), name="login"),
	path('home/', views.HomeView.as_view(), name="home"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
	path('update/', views.UpdateView.as_view(), name="update"),
	path('delete/', views.DeleteView.as_view(), name="delete"),
	path('requests/', views.RequestView.as_view(), name="request"),
	path('requests/<int:sent>', views.RequestView.as_view(), name="request"),
	path('friends/', views.FriendsView.as_view(), name="friends"),
	path('request/<str:u>', views.SendRequestView.as_view(), name="request"),
	path('accept/<str:u>', views.AcceptRequestView.as_view(), name="accept"),
	path('unfriend/<str:u>', views.UnfriendView.as_view(), name="unfriend"),
	path('withdraw/<str:u>', views.WithdrawRequestView.as_view(), name="withdraw"),
	path('profile/<str:un>', views.ProfileView.as_view(), name="profile"),
	path('interest/', views.InterestView.as_view(), name="interest"),
]
