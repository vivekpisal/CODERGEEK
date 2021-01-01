from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('',login,name='login'),
    path('writearticle',writearticle,name="writearticle"),
    path('reviewarticle',reviewarticle,name="reviewarticle"),
    path('review/<int:id>',review,name="review"),
    path('deletearticle/<int:id>',deletearticle,name="deletearticle"),
    path('allarticles',allarticles,name="allarticles"),
    path('editarticle/<int:id>',editarticle,name="editarticle"),
    path('filterarticle/<str:status>',filter_article,name="filterarticle"),
    path('article/<str:title>',showarticle,name="showarticle"),
    path('profile',profile,name="profile"),
    path('search',search,name="search"),
    path('save',save,name="save"),
    path('register',register,name="register"),
    path('jobs',jobs,name="jobs"),
    path('addjob',addjob,name="addjob")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)