from django.urls import path
from . import views

urlpatterns = [
    path('create', views.ProductsAPI.as_view()),
    path('<int:pk>', views.ProductsRetrieveUpdateDestroyAPI.as_view()),
    path('<int:pk>/offers', views.ProductsOfferGetAPI.as_view())
]
