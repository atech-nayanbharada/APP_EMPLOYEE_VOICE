from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('review:employee_review')
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['email']
        pwd = request.POST['password']
        user = authenticate(email=email, password=pwd)
        if user.is_active:
            login(request, user)
            messages.success(request, "login success")
            return redirect('review:employee_review')
        else:
            messages.error(request, "invalid credentials")
        return render(request, self.template_name)
        # print(email+"= email ,"+pwd+" = password")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('user:login')


class DemoView(View):
    template_name = "demo.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginOneView(View):
    template_name = "user/login/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user:dashboard')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        pwd = request.POST['password']
        user = authenticate(email=email, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, "login success")
            return redirect('user:dashboard')
        else:
            messages.error(request, "invalid credentials")
        return render(request, self.template_name)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "user/dashboard.html"
