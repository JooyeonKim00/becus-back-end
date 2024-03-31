from .views import *
from django.urls import path
urlpatterns = [
    # client API
    path('', ListOrderView.as_view()),
    path('<int:pk>', OneOrderView.as_view()),
    # admin API
]