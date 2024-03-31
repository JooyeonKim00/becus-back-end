from django.urls import path
from .views import *

urlpatterns = [
    path('', ListProductView.as_view()),
    path('<int:pk>', OneProductView.as_view())
]
