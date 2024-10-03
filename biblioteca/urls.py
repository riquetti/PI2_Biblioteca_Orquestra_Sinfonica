from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path('', lambda request: redirect('auth/login/')),
    path('admin/', admin.site.urls),
    path('livro/', include('livro.urls')),
    path('auth/', include('usuarios.urls'))
]
