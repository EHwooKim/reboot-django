from django.db import models

# Create your models here.
# 내가 Article.objects 같은 정의하지 않을 것들을 쓰잖아. 상속받은게 있기 때문이고, Model은 CamelCase인걸 보니 클래스구나 
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
