from django.db import models
from adaptor.model import CsvModel
from adaptor.fields import CharField, IntegerField, BooleanField, FloatField

# Create your models here.

class Reddit(models.Model):
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
    Frequency = models.IntegerField(max_length = 20)

class RedditCsvModel(CsvModel):
    Term = CharField(match = "Term")
    Company_Name =CharField(match = "Company_Name")
    Last_Sale = IntegerField(match = "Last Sale")
    Net_Change = IntegerField(match = "Net Change")
    Percent_Change = IntegerField(match = "% Change")
    Market_Cap = IntegerField(match = "Market Cap")
    Country = CharField(match = "Country")
    IPO_Year = IntegerField(match = "IPO Year")
    Volume = IntegerField(match = "Volume")
    Sector = CharField(match = "Sector")
    Industry = CharField(match = "Industry")
    Frequency = IntegerField(match = "Frequency")

    class Meta:
        delimiter = ","
        dbModel = Reddit





