from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Reddit

admin.site.register(Reddit)

class RedditAdmin(ImportExportModelAdmin):
    #list_display = ('ticker_name', 'created_at', 'title','text', 'score', 'sentiment', 'subjectivity')
    pass
