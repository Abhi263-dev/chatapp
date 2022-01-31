from urllib import request
from django.shortcuts import render, redirect

from profiles.models import User
from .models import Post
from profiles.models import Friends
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
from django.db.models import Q


class PostCreate(LoginRequiredMixin, CreateView):
    login_url='profiles:login'
    model= Post
    fields = ["picture", "caption", "private"]
    template_name = "createpost.html"
    success_url=reverse_lazy('profiles:home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class Postlist(LoginRequiredMixin, View):
    login_url='profiles:login'
    def get(self, request):
        query=request.GET.get("query")
        msg=""
        if query and User.objects.filter(username=query).exists():
            if query==request.user.username:
                return redirect('profiles:home')
            return redirect('profiles:profile', un=query)
        elif query:
            msg="Cannot find anyone named "+query
        users = User.objects.all()
        res= Post.objects.filter(
            Q(user__in=Friends.objects.filter(friend1=self.request.user.pk).values('friend2')) |
            Q(user__in=Friends.objects.filter(friend2=self.request.user.pk).values('friend1'))
        ).order_by("-date_added")
        return render(request,'listpost.html',{"users":users, "msg":msg, "posts":res})

