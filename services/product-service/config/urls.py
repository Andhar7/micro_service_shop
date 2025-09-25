from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'product-service'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('api/', include('apps.products.urls')),
]
