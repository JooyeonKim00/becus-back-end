from .views import *
from django.urls import path
urlpatterns = [
    # client API
    path('', ListRepairView.as_view()),
    path('<int:pk>', OneRepairView.as_view()),
    # admin API
]