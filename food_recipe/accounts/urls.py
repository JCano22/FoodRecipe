from django.urls import path
from .views import SignUpView
from . import views 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path("account_info/", views.account_info_view, name='account_info'),
    path('edit_account/', views.edit_account, name='edit_account'),

]