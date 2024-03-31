from .views import *
from django.urls import path
urlpatterns = [
    # client API
    path('global', ListGlobalConsultView.as_view()),
    path('global/<int:pk>', OneGlobalConsultView.as_view()),
    path('product', ListProductConsultView.as_view()),
    path('product/<int:pk>', OneProductConsultView.as_view())
    # admin API
]