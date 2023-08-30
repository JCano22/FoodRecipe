from django.urls import path
from .views import SaveNextView

urlpatterns = [
    path('save_next/', SaveNextView.as_view(), name='save_next'),
]
