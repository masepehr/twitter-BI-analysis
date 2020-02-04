from django.db import models

# Create your models here.
class Persons(models.Model):
    uname=models.CharField(max_length=255,null=False)
    followers=models.IntegerField(default=0)
    followings=models.IntegerField(default=0)
    pic=models.ImageField(upload_to='images/',null=True)
    def __str__(self):
        return self.uname


class Tweets(models.Model):
    author=models.ForeignKey(Persons,on_delete=models.CASCADE,related_name='tweets')
    text=models.TextField(max_length=500)
    date=models.DateTimeField()

    likes_count=models.PositiveIntegerField()
    hashtags=models.CharField(max_length=255)
    replies_count=models.PositiveIntegerField()
    retweets_count=models.PositiveIntegerField()
    class Meta:
        unique_together=(('author','text','date','likes_count','hashtags','replies_count','retweets_count'))

    def __str__(self):
        return self.text
