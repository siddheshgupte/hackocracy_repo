from django.conf.urls import url
from .views import user_login
from django.contrib.auth import views as auth_views
from .views import dashboard

urlpatterns = [
    # url(r'^login/$', user_login, name='login')

#     Default login/logout views
    url(r'^login/$',
        auth_views.login,
        name='login'),
    url(r'^logout/$',
        auth_views.logout,
        name='logout'),
    url(r'logout-then-login',
        auth_views.logout_then_login,
        name='logout_then_login'),
    url(r'^$',
        dashboard,
        name='dashboard'),

]