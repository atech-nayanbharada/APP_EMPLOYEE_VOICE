from django.contrib import admin
from django.urls import path,include
from user import views

app_name = 'user'

urlpatterns = [
 path('', views.LoginView.as_view(), name='login'),
 path('logout', views.LogoutView.as_view(), name='logout'),

 # new designs
 # path("login_one", views.LoginOneView.as_view(), name="login_one"),
 # path('demo', views.DemoView.as_view(), name='demo'),
 # path('dashboard', views.DashboardView.as_view(), name='dashboard')

]
