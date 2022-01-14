import threading
import time
import os
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from requests import get, post
from catalog.models import Products, Offers
from . import serializer
from catalog import apps
from datetime import datetime


def updater_job():
    while True:
        time.sleep(60)
        offer_updater()


updater = threading.Thread(target=updater_job, daemon=True, )


def thread_starter():
    if updater.is_alive():
        return
    updater.start()


class ProductsAPI(ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = serializer.ProductsSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        post_data = {'id': serializer.data["id"], 'name': serializer.data["name"],
                     'description': serializer.data["description"]}
        r = post(url=str(os.getenv('API_OFFERS_URL')) + "/products/register", headers=apps.OFFER_API_HEADER,
                 data=post_data)
        if r.status_code.__str__() != '201':
            Products.objects.get(id=serializer.data["id"]).delete()
            r.raise_for_status()
            return Response(r.json())
        else:
            offers_response = load_offers_data(serializer.data["id"])
            if offers_response.status_code != 200:
                return Response({"status": False,
                                 "message:": "Problem loading offers",
                                 "offer_response": offers_response})
            thread_starter()
            headers = self.get_success_headers(serializer.data)
            return Response({"status": True,
                             "message": "Product added and offers loaded!",
                             "data": serializer.data,
                             "registration_response": r.json(),
                             "offers_response": offers_response.json()},
                            status=status.HTTP_201_CREATED, headers=headers)


class ProductsRetrieveAPI(ListAPIView):
    def get(self, request, *args, **kwargs):
        thread_starter()
        return Response({"status": True, "products": Products.objects.all().values()}, status=status.HTTP_200_OK)


class ProductsRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.ProductsSerializer

    def get_queryset(self):
        thread_starter()
        return Products.objects.filter(id=self.kwargs.get('pk', None))

    def update(self, request, *args, **kwargs):
        thread_starter()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"status": True,
                         "message": "Product updated!",
                         "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        thread_starter()
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"status": True,
                         "message": "Product deleted!"}, status=status.HTTP_204_NO_CONTENT)


class ProductsOfferGetAPI(ListAPIView):
    serializer_class = serializer.ProductsSerializer

    def get(self, request, *args, **kwargs):
        thread_starter()
        if Products.objects.filter(id=self.kwargs.get("pk")).exists():
            return Response({"status": True, "product": Products.objects.filter(id=self.kwargs.get("pk")).values()[0],
                             "offers": Offers.objects.filter(product=self.kwargs.get("pk")).values()}
                            )
        else:
            return Response({"status": False, "message:": "Product not found!",
                             }, status=status.HTTP_404_NOT_FOUND)


def load_offers_data(product_id):
    post_data = {'id': product_id}
    r = get(url=str(os.getenv('API_OFFERS_URL')) + "/products/" + str(product_id) + "/offers",
            headers=apps.OFFER_API_HEADER,
            data=post_data)
    if r.status_code != 200:
        return r
    received_offers = r.json()
    Offers.objects.filter(product=product_id).delete()
    for i in received_offers:
        created = Offers.objects.update_or_create(product=Products.objects.get(id=product_id), offer_id=i["id"],
                                                  price=i["price"], items_in_stock=i["items_in_stock"])
    return r


def offer_updater():
    ret = 0
    for product in Products.objects.all():
        load_offers_data(product.id)
        ret += 1
    print(datetime.now(), " Offers updated, # of products:", ret)
    return ret
