from django.db import models


# Create your models here.
class Pconsult(models.Model):
    pc_name = models.CharField(max_length=20)
    pc_email = models.EmailField()
    pc_phone = models.CharField(max_length=13)
    pc_product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    pc_content = models.TextField()
    pc_created_at = models.DateTimeField(auto_now_add=True)

    # 문의 상태 관련
    PC_STATUS_CHOICES = [
        ('Request', '요청 대기'),
        ('Accepted', '요청 수락'),
        ('Completed', '처리 완료')
    ]
    pc_status = models.CharField(
        max_length=10,
        choices=PC_STATUS_CHOICES,
        default='Request'
    )

    pc_author = models.ForeignKey("user.User", on_delete=models.CASCADE)

class Gconsult(models.Model):
    gc_name = models.CharField(max_length=20)
    gc_email = models.EmailField()
    gc_phone = models.CharField(max_length=13)

    # 문의 유형
    GC_TYPE_CHOICES = [
        ('Order', '주문'),
        ('AS', 'AS 요청'),
        ('Consult', '상담')
    ]
    gc_type = models.CharField(
        max_length=10,
        choices=GC_TYPE_CHOICES,
        default='Order'
    )

    #gc_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    gc_content = models.TextField()
    gc_created_at = models.DateTimeField(auto_now_add=True)

    # 문의 상태 관련
    GC_STATUS_CHOICES = [
        ('Request', '요청 대기'),
        ('Accepted', '요청 수락'),
        ('Completed', '처리 완료')
    ]
    gc_status = models.CharField(
        max_length=10,
        choices=GC_STATUS_CHOICES,
        default='Request'
    )

    gc_author = models.ForeignKey("user.User", on_delete=models.CASCADE)