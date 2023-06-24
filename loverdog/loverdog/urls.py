from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dogbreed.views import predict_dog_breed, breed_prediction

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chkDogImg/', include('chkDogImg.urls')),
    path('', include('single_page.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
    path('blog/', include('blog.urls')),
    path('predict/', predict_dog_breed, name='predict_breed'),
    path('predictions/', breed_prediction, name='breed_prediction'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
