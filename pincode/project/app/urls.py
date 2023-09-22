from django.urls import path
from .views import pincode

urlpatterns = [
    path('pincode/',pincode, name='pincode'),
    ]