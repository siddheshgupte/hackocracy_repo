from django.conf.urls import url
from .views import register
from django.contrib.auth import views as auth_views
from .views import dashboard,Transaction_history

urlpatterns = [
    # url(r'^login/$', user_login, name='login')

#     Default login/logout views
    url(r'^login/$',
        auth_views.login,
        name='login'),
    url(r'^logout/$',
        auth_views.logout,
        name='logout'),
    url(r'^logout-then-login/$',
        auth_views.logout_then_login,
        name='logout_then_login'),
    url(r'^$',
        dashboard,
        name='dashboard'),
    url(r'^Transaction_history/$',
        Transaction_history,
        name='Transaction_history'),
    url(r'^password-change/$',
        auth_views.password_change,
        name='password_change'),
    url(r'^password-change-done/$',
        auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password-reset/$',
        auth_views.password_reset,
        name='password_reset'),
    url(r'^password-reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password_reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^register/$',
        register,
        name='register'),

]