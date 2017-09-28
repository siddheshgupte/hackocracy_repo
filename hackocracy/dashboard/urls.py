from django.conf.urls import url
from .views import register, edit, dashboard, Transaction_history, custom_logout, send_blockchain, all_transaction
from django.contrib.auth import views as auth_views

urlpatterns = [
    # url(r'^login/$', user_login, name='login')

#     Default login/logout views
    url(r'^login/$',
        auth_views.login,
        name='login'),
    url(r'^logout/$',
        custom_logout,
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
    url(r'^all_transaction/$',
        all_transaction,
        name='all_transaction'),
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
    url(r'^edit/$',
        edit, name='edit'),
    url(r'^send_blockchain/$',
        send_blockchain,
        name='send_blockchain'),


]
