from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models
from .mangers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    # Custom Field
    email = models.EmailField(max_length=30, unique=True)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)

    # 역할 관련
    ROLE_CHOICES = [
        ('USER', '회원'),
        ('NON-USER', '비회원'),
        ('ADMIN', '관리자')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # 승인 여부 관련
    APPROVAL_CHOICES = [
        ('ACCEPT', '요청 승인'),
        ('WAITING', '요청 대기'),
        ('REJECT', '요청 거부')
    ]
    approval = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default=None,
        blank=True,
        null=True
    )
    
    is_auth_email = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Necessary Field
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    # User 모델 식별을 위한 필드 설정
    USERNAME_FIELD = 'email'
    # 필수 작성 필드
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email