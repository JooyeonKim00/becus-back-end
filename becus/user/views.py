from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from json import JSONDecodeError
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.naver import views as naver_views
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView

from .models import User
from .serializers import GetUserSerializer

# python package
import requests
# Create your views here.

class NaverLoginAPIView(APIView):
    # 로그인을 위한 창은 누구든 접속이 가능해야 하기 때문에 permission을 AllowAny로 설정
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        client_id = settings.SOCIAL_AUTH_NAVER_CLIENT_ID
        response_type = "code"
        uri = settings.SOCIAL_AUTH_NAVER_REDIRECT_URI
        state = settings.STATE
        url = "https://nid.naver.com/oauth2.0/authorize"
        return redirect(
            f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={uri}&state={state}'
        )


class NaverCallbackAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # setting naevr login parameters
            grant_type = 'authorization_code'
            client_id = settings.SOCIAL_AUTH_NAVER_CLIENT_ID
            client_secret = settings.SOCIAL_AUTH_NAVER_SECRET
            code = request.GET.get('code')
            state = request.GET.get('state')
            parameters = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"

            # request access_token for getting user_info
            token_request = requests.get(
                f"https://nid.naver.com/oauth2.0/token?{parameters}"
            )
            token_response_json = token_request.json()
            error = token_response_json.get('error', None)
            # access token call error
            if error is not None:
                raise JSONDecodeError(error)
            access_token = token_response_json.get('access_token')
            
            # get user info
            user_info_request = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization":f"Bearer {access_token}"}
            )
            if user_info_request.status_code != 200:
                return JsonResponse({
                    "error": "failed to naver login"
                }, status=status.HTTP_400_BAD_REQUEST)
            user_info = user_info_request.json().get("response")
            email = user_info["email"]
            if email is None:
                return JsonResponse({
                    "error": "Can't Get Email Information from Naver"
                }, status=status.HTTP_400_BAD_REQUEST)
            name = user_info.get('name', None)
            phone = user_info.get('mobile', None)
            # try login & register
            try:
                user = User.objects.get(email=email)
                social_user = SocialAccount.objects.get(user=user)
                data = {'access_token': access_token, 'code': code}
                authentication = requests.post(
                    settings.SOCIAL_AUTH_NAVER_LOGIN_URI, data=data
                )
                if authentication.status_code != 200:
                    return JsonResponse({"error": "Failed to SignIn"}, status=status.HTTP_200_OK)
                authentication_json = authentication.json()

                # refresh token parsing
                access_token = authentication_json['access']
                refresh_token = authentication_json['refresh']
                cookie_max_age = 3600 * 24 * 2
                response = JsonResponse(authentication_json, status=status.HTTP_200_OK)
                response.set_cookie('access-token', access_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
                response.set_cookie('refresh-token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
                return response
            except User.DoesNotExist:
                data = {'access_token': access_token, 'code': code}
                authentication = requests.post(
                    settings.SOCIAL_AUTH_NAVER_LOGIN_URI, data=data
                )
                if authentication.status_code != 200:
                    return JsonResponse({"error": "Failed to SignIn"}, status=status.HTTP_200_OK)
                authentication_json = authentication.json()
                user = User.objects.get(email=email)
                user.name = name
                user.phone = phone
                user.is_auth_email = True
                user.role = 'USER'
                user.save()
                # refresh token parsing
                access_token = authentication_json['access']
                refresh_token = authentication_json['refresh']
                cookie_max_age = 3600 * 24 * 2
                response = JsonResponse(authentication_json, status=status.HTTP_200_OK)
                response.set_cookie('access-token', access_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
                response.set_cookie('refresh-token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
                return response
            except SocialAccount.DoesNotExist:
                return JsonResponse({'error': 'email already exists but not social account'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({
                "error": "Failed to request naver login"
            }, status=status.HTTP_400_BAD_REQUEST)

class NaverLoginView(SocialLoginView):
    adapter_class = naver_views.NaverOAuth2Adapter
    client_class = OAuth2Client

# kakao login
class KakaoLoginAPIView(APIView):
    # 로그인을 위한 창은 누구든 접속이 가능해야 하기 때문에 permission을 AllowAny로 설정
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        client_id = settings.SOCIAL_AUTH_KAKAO_CLIENT_ID
        redirect_uri = settings.SOCIAL_AUTH_KAKAO_REDIRECT_URI
        response_type = 'code'
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}&scope=profile_image,profile_nickname"
        )
    
class KakaoCallbackAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # setting kakao login parameters
            grant_type = 'authorization_code'
            client_id = settings.SOCIAL_AUTH_KAKAO_CLIENT_ID
            redirect_uri = settings.SOCIAL_AUTH_KAKAO_REDIRECT_URI
            code = request.GET.get('code')
            # request access token
            url = "https://kauth.kakao.com/oauth/token"
            headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
            datas = {
                "grant_type" : grant_type,
                "client_id" : client_id,
                "redirect_uri" : redirect_uri,
                "code" : code
            }
            # Response python 객체 반환
            token_request = requests.post(url, data=datas, headers=headers)
            token_response_json = token_request.json()
            # 에러 여부 체크
            error = token_response_json.get("error", None)
            if error is not None:
                raise json.JSONDecodeError(error)
            
            # access token
            access_token = token_response_json.get("access_token")
            url = "https://kapi.kakao.com/v2/user/me"
            headers = {"Authorization" : f"Bearer {access_token}"}
            # information request
            profile_request = requests.post(url, headers=headers)
            profile_response_json = profile_request.json()
            
            kakao_account = profile_response_json.get('kakao_account')
            profile = kakao_account.get('profile')
            nickname = profile.get('nickname')
            profile_image = profile.get('thumbnail_image_url')
            print(nickname, profile_image)
            # try login & register
            try:
                user = User.objects.get(name=nickname)
                social_user = SocialAccount.objects.get(user=user)
                # not kakao social account
                if social_user.provider != 'kakao':
                    return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
                
                data = {'access_token': access_token, 'code': code}
                authentication = requests.post(
                    settings.SOCIAL_AUTH_KAKAO_LOGIN_URI, data=data
                )
                if authentication.status_code != 200:
                    return JsonResponse({"error": "Failed to SignIn"}, status=status.HTTP_200_OK)
                authentication_json = authentication.json()
                print(authentication_json)
                # refresh token parsing
                access_token = authentication_json['access']
                refresh_token = authentication_json['refresh']
                cookie_max_age = 3600 * 24 * 2
                response = JsonResponse(authentication_json, status=status.HTTP_200_OK)
                response.set_cookie('access-token', access_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
                response.set_cookie('refresh-token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
                return response
            except User.DoesNotExist:
                data = {'access_token': access_token, 'code': code}
                authentication = requests.post(
                    settings.SOCIAL_AUTH_KAKAO_LOGIN_URI, data=data
                )
                if authentication.status_code != 200:
                    return JsonResponse({"error": "Failed to SignIn"}, status=status.HTTP_200_OK)
                authentication_json = authentication.json()
                user = User.objects.get(name=nickname)
                user.name = nickname
                user.role = 'USER'
                user.save()
                # refresh token parsing
                access_token = authentication_json['access']
                refresh_token = authentication_json['refresh']
                cookie_max_age = 3600 * 24 * 2
                response = JsonResponse(authentication_json, status=status.HTTP_200_OK)
                response.set_cookie('access-token', access_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
                response.set_cookie('refresh-token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
                return response
            except SocialAccount.DoesNotExist:
                return JsonResponse({'error': 'email already exists but not social account'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({
                "error": "Failed to request kakao login"
            }, status=status.HTTP_400_BAD_REQUEST)

class KakaoLoginView(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    callback_url = settings.SOCIAL_AUTH_KAKAO_REDIRECT_URI
    client_class = OAuth2Client