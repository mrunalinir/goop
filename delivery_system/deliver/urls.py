
from django.contrib import admin
from django.urls import path, include, re_path
from users import views as userviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('order/', include('order.urls', namespace='order')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('feedback/',include('feedback.urls', namespace='feedback')),
    path('', include('shop.urls', namespace='shop')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)