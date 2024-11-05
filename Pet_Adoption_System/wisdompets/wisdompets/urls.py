from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from adoptions import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('delete_pet/<id>/',views.delete_pet,name="delete_pet"),
    path('update_pet/<id>/',views.update_pet,name="update_pet"),
    path('add_pet/',views.add_pet,name="add_pet"),
    path('all_pets/',views.pets,name="pets"),
    path('register/',views.register_page,name="register_page"),
    path('login/',views.login_page,name="login_page"),
    path('logout/',views.logout_page,name="logout_page"),
    path('adoptions/<int:pet_id>/', views.pet_detail, name='pet_detail'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
