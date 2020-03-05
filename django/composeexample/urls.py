"""composeexample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from django.conf.urls.static import static
from django.conf import settings

from course.urls import router as course_router
from classroom.urls import router as classroom_router
from main.urls import router as main_router
from mail.urls import router as mail_router

# router = routers.DefaultRouter()
# router.extend(course_router)
# router.extend(classroom_router)
# router.extend(main_router)
# router.extend(mail_router)

urlpatterns = [
    re_path('^api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    # path("api/", include("main.urls")),
    # path("api/", include(router.urls)),
    path("api/", include("course.urls")),
    # path("api/", include("mail.urls")),
    # path("")

]



# if the static files isn't AWS S3
if (not settings.USE_S3) and (not settings.USE_AWS_FOR_OFFLINE_USAGE):
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
