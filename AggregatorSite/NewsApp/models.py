from django.db import models

#Source -> E.g. BBC,CNN,etc.
class Source(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True,null=True)
    #0 - 7 Bias Classification
    class Bias(models.IntegerChoices):
        Unknown = 0
        Far_Left = 1
        Left = 2
        Centre_Left = 3
        Centre = 4
        Centre_Right = 5
        Right = 6
        Far_Right = 7
    bias = models.IntegerField(choices=Bias)

class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=30)
    author = models.CharField(max_length=30,blank=True,null=True)
    title = models.CharField(max_length=500)
    processed_title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    url = models.URLField(unique=True)
    urlToImage = models.URLField(unique=True)
    publishedAt = models.DateTimeField()
    content = models.TextField(blank=True)

