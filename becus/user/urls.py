from django.urls import path
from .views import *
urlpatterns = [
    path('naver/login', NaverLoginAPIView.as_view()),
    path('naver/callback', NaverCallbackAPIView.as_view()),
    path('naver/login/success', NaverLoginView.as_view()),
    path('kakao/login', KakaoLoginAPIView.as_view()),
    path('kakao/callback',KakaoCallbackAPIView.as_view()),
    path('kakao/login/success', KakaoLoginView.as_view())
]
