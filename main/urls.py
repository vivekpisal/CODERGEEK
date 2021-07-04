from django.urls import path,include
from django.conf import settings
from django.contrib.auth.views import *
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
    path('addjob',addjob,name="addjob"),
    path('courses',courses,name="courses"),
    path('login/',login_view,name="login"),
    path("password-reset/", 
        PasswordResetView.as_view(template_name='registration/password_reset.html'),
        name="password_reset"),

    path("password-reset/done/", 
        PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/", 
        PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
        name="password_reset_confirm"),

    path("password-reset-complete/", 
        PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
        name="password_reset_complete"),

    path('resendOTP', resend_otp),
    path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)