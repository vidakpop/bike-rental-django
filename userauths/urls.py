from django.urls import path
from userauths import views

app_name="userauths"

urlpatterns=[
    path("signup/",views.register_view, name="signup"),
    path("",views.login_view, name="login"),
    path("logout/",views.logout_view, name="logout"),


]
