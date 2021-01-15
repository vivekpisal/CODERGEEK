from django.contrib import admin
from .models import *
# Register your models here.


admin.site.site_header="CODERGEEK"
admin.site.index_title="CODERGEEK"
admin.site.site_title="CODERGEEK"


admin.site.register(Info)
admin.site.register(Article)
admin.site.register(PublishedArticle)
admin.site.register(Jobs)
admin.site.register(Course)