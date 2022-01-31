from urllib import request
from django.shortcuts import render,redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import User, Friends, Requests, UserInterest, Interest
from posts.models import Post
from .forms import RegistrationForm, InterestForm
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,  logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q

class RegisterView(CreateView):
    model = User
    form_class=RegistrationForm
    template_name = 'register.html'
    def form_valid(self, form):
        form.save()
        return redirect('profiles:login')

class LoginView(View):
    def get(self,request):
        form=AuthenticationForm()
        return render(request=request,template_name='login.html',context={"form":form})
    def post(self,request):
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print (user)
                return redirect('profiles:home')
            else:
               print("Invalid username or password.")
        else:
            print("Invalid username or password.")

class HomeView(LoginRequiredMixin,View):
    login_url='profiles:login'
    def get(self,request):
        print(request.user)
        posts=Post.objects.filter(user=request.user)
        interests=UserInterest.objects.filter(u=request.user)
        form=InterestForm()
        return render(request=request,template_name='home.html', context={"posts" : posts, "form":form, "in":interests})

class UpdateView(LoginRequiredMixin, UpdateView):

    def get_object(self):
        return self.request.user
    model=User
    fields=["username","photo","dob","bio"]
    template_name='updateprofile.html'
    success_url=reverse_lazy('profiles:home')

class DeleteView( LoginRequiredMixin, DeleteView):
    def get_object(self):
        return self.request.user
    model=User
    template_name='deleteprofile.html'
    success_url=reverse_lazy('profiles:logout')


class ProfileView(LoginRequiredMixin, View):
    login_url='profiles:login'
    def get(self, request, un):
        user=User.objects.get(username=un)
        posts=Post.objects.filter(user__username=un, private=False)
        interests=UserInterest.objects.filter(u=user)
        reqe=False
        fr=False
        reqr=False
        if Requests.objects.filter(requestee=request.user, requester=user).exists():
            reqe=True
        elif Requests.objects.filter(requestee=user, requester=request.user).exists():
            reqr=True
        elif Friends.objects.filter(friend1=request.user, friend2=user).exists():
            fr=True
        elif Friends.objects.filter(friend2=request.user, friend1=user).exists():
            fr=True
        return render(request, 'profile.html', {"us":user, "fr": fr, "reqe": reqe, "reqr": reqr, "posts":posts, "in":interests})


class FriendsView(LoginRequiredMixin, ListView):
    login_url='profiles:login'
    model=Friends
    template_name="friends.html"
    context_object_name="friends"
    ordering = ["-date_added"]
    def get_queryset(self):
        res=[]
        q=Friends.objects.filter(friend1=self.request.user).values('friend2__username', 'friend2__photo', 'friend2__bio')
        for f in q:
            res.append({'us': f['friend2__username'], 'pic': f['friend2__photo'], 'bio': f['friend2__bio']})
        q=Friends.objects.filter(friend2=self.request.user).values('friend1__username', 'friend1__photo', 'friend1__bio')
        for f in q:
            res.append({'us': f['friend1__username'], 'pic': f['friend1__photo'], 'bio': f['friend1__bio']})
        print(res)
        return res

class RequestView(LoginRequiredMixin, View):
    login_url='profiles:login'
    def get(self, request, sent=None):
        if sent:
            requests=Requests.objects.filter(requester=self.request.user).order_by("-date_added")
            return render(request, "requests_list.html", {'requests': [], 'sent': requests, 'sen':True})
        else:
            requests=Requests.objects.filter(requestee=self.request.user).order_by("-date_added")
            return render(request, "requests_list.html", {'requests': requests, 'sent':[], 'sen':False})

class SendRequestView(LoginRequiredMixin,View):
    login_url='profiles:login'
    def get(self, request, u=None):
        if not Requests.objects.filter(requester=request.user, requestee=User.objects.get(username=u)).exists():
            req=Requests.objects.create(requester=request.user, requestee=User.objects.get(username=u))
            req.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AcceptRequestView(LoginRequiredMixin,View):
    login_url='profiles:login'
    def get(self, request, u=None):
        ureq=User.objects.get(username=u)
        if Requests.objects.filter(requester=ureq, requestee=request.user).exists():
            fr=Friends.objects.create(friend1=request.user, friend2=ureq)
            Requests.objects.get(requester=ureq, requestee=request.user).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class WithdrawRequestView(LoginRequiredMixin,View):
    login_url='profiles:login'
    def get(self, request, u=None):
        ureq=User.objects.get(username=u)
        if Requests.objects.filter(requestee=ureq, requester=request.user).exists():
            Requests.objects.get(requestee=ureq, requester=request.user).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UnfriendView(LoginRequiredMixin,View):
    login_url='profiles:login'
    def get(self, request, u=None):
        ureq=User.objects.get(username=u)
        if Friends.objects.filter(friend1=ureq, friend2=request.user).exists():
            Friends.objects.get(friend1=ureq, friend2=request.user).delete()
        elif Friends.objects.filter(friend2=ureq, friend1=request.user).exists():
            Friends.objects.get(friend2=ureq, friend1=request.user).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class InterestView(LoginRequiredMixin, View):
    login_url='profiles:login'
    def post(self, request):
        form=InterestForm(request.POST)
        if form.is_valid():
            temp = form.cleaned_data.get("field")
            for t in temp:
               ui= UserInterest.objects.create(interest=Interest.objects.get(pk=int(t)), u=request.user)
               ui.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class LogoutView(LoginRequiredMixin,View):
    login_url='profiles:login'
    def get(self,request):
        logout(request)
        return redirect('profiles:login')

