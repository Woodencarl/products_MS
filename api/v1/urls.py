from django.urls import path, include


urlpatterns = [
    path('products/', include('api.v1.products.urls')),
    #path('productoffers/', include('api.v1.productoffers.urls')),
]
