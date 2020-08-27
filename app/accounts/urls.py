from django.conf.urls import url

from .views import custom_login, register, profile, logout_view, settings

app_name = 'accounts'
urlpatterns = [
    # /login
    url(
        r'^login/$',
        custom_login,
        name='login',
    ),

    # /logout
    url(
        r'^logout/$',
        logout_view.as_view(),
        name='logout',
    ),

    # /register
    url(
        r'^register/$',
        register,
        name='register',
    ),

    # /profile
    url(
        r'^profile/$',
        profile,
        name='profile',
    ),

    # /profile
    url(
        r'^settings/$',
        settings,
        name='settings',
    ),
]
