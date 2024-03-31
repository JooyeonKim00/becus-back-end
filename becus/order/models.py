from django.db import models


# Create your models here.
class Order(models.Model):
    o_name = models.CharField(max_length=20)
    o_email = models.EmailField()
    o_phone = models.CharField(max_length=13)
    o_product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    o_amount = models.IntegerField()
    o_address = models.CharField(max_length=50)
    o_content = models.TextField()

    # 주문 상태 관련
    O_STATUS_CHOICES = [
        ('Request', '요청 대기'),
        ('Accepted', '요청 수락'),
        ('Completed', '처리 완료')
    ]
    o_status = models.CharField(
        max_length=10,
        choices=O_STATUS_CHOICES,
        default='Request'
    )

    o_author = models.ForeignKey("user.User", on_delete=models.CASCADE)
