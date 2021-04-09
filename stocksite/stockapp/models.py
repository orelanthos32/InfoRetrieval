from django.db import models

# Create your models here.
'''
class RedditStonks(models.Model):
    Term = models.CharField(max_length = 100)
    Company_Name = models.CharField(max_length = 100)
    Last_Sale = models.IntegerField(max_length = 20)
    Net_Change = models.IntegerField(max_length = 20)
    Percent_Change = models.IntegerField(max_length = 20)
    Market_Cap = models.IntegerField(max_length = 20)
    Country = models.CharField(max_length = 100)
    IPO_Year = models.IntegerField(max_length = 20)
    Volume = models.IntegerField(max_length = 20)
    Sector = models.CharField(max_length = 100)
    Industry = models.CharField(max_length = 100)
    '''

class Reddit(models.Model):
    ticker_name = models.CharField(max_length = 20)
    created_at = models.CharField(max_length = 20)
    title  = models.CharField(max_length = 100)
    text = models.CharField(max_length = 100)
    score = models.IntegerField(max_length = 2)
    sentiment = models.IntegerField(max_length = 2)
    subjectivity = models.IntegerField(max_length = 2)

    '''

class Twitter(models.Model):
    # remove datetime, twweetid
    query = models.CharField(max_length = 10)
    text = models.CharField(max_length = 100)
    username = models.CharField(max_length = 20)
    rt = models.CharField(max_length = 2)
    rtCount = models.IntegerField(max_length = 4)
    favCount = models.IntegerField(max_length = 4)
    sentiment = models.IntegerField(max_length = 2)
    subjectivity = models.IntegerField(max_length = 2)
    '''



