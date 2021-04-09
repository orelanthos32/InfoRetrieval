from import_export import resources
from .models import Reddit

class RedditResource(resources.ModelResource):
    class meta:
        model = Reddit