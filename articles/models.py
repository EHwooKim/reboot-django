from django.db import models

# Reporter(1) - Aricle(N)
# reporter - name
class Reporter(models.Model):
    name = models.CharField(max_length=5)

# Create your models here.
# 내가 Article.objects 같은 정의하지 않을 것들을 쓰잖아. 상속받은게 있기 때문이고, Model은 CamelCase인걸 보니 클래스구나 
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField()
    # auto_now_add : 더해지는 그 순간... create되는 순간에만!
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now : 변경될 때 항상 찍어주는거!
    updated_at = models.DateTimeField(auto_now=True)
    # reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

# Article(1) - Comment(N)
# comment - content
class Comment(models.Model):
    content = models.CharField(max_length=140)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
