from django.urls import path

from django.contrib.auth.views import LogoutView, LoginView

app_name = 'accounts'

urlpatterns = [
    path('', LoginView.as_view(template_name="login_page.html", redirect_authenticated_user=True), name="login", ),
    path('logout/', LogoutView.as_view(), name='logout'),
]
