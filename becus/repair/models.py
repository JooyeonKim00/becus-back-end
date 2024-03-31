from django.db import models


# Create your models here.
class Repair(models.Model):
    r_name = models.CharField(max_length=20)
    r_email = models.EmailField()
    r_phone = models.CharField(max_length=13)
    r_product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    # 수리 유형 관련
    R_TYPE_CHOICES = [
        ('RT1', 'RT1'),
        ('RT2', 'RT2')
    ]
    r_type = models.CharField(
        max_length=10,
        choices=R_TYPE_CHOICES,
        default='RT1'
    )

    r_content = models.TextField()
    r_created_at = models.DateTimeField(auto_now_add=True)

    # AS 상태 관련
    R_STATUS_CHOICES = [
        ('Request', '요청 대기'),
        ('Accepted', '요청 수락'),
        ('Completed', '처리 완료')
    ]
    r_status = models.CharField(
        max_length=10,
        choices=R_STATUS_CHOICES,
        default='Request'
    )


class Maintenance(models.Model):
    m_product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    # 수리 유형 관련
    M_TYPE_CHOICES = [
        ('RT1', 'RT1'),
        ('RT2', 'RT2')
    ]
    m_type = models.CharField(
        max_length=10,
        choices=M_TYPE_CHOICES,
        default='RT1'
    )

    m_title = models.CharField(max_length=20)
    m_content = models.TextField()

    M_CONTENT_TYPE_CHOICES = [
        ('Video', '비디오'),
        ('Text', '텍스트')
    ]
    m_content_type = models.CharField(max_length=10, choices=M_CONTENT_TYPE_CHOICES)

    r_author = models.ForeignKey("user.User", on_delete=models.CASCADE)