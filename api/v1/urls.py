from django.urls import path, include


urlpatterns = [
    path('products/', include('api.v1.products.urls')),
]
