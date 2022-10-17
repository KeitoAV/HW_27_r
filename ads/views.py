import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ad, Category


def root(request):
    return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        ads = Ad.objects.all()
        response = []
        for ad in ads:
            response.append({
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price
            })
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        ad_data = json.loads(request.body)
        ad = Ad.objects.create(**ad_data)
        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published

        }, safe=False, json_dumps_params={'ensure_ascii': False})


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        response = []
        for cat in categories:
            response.append({
                "id": cat.pk,
                "name": cat.name
            })
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        cat_data = json.loads(request.body)
        cat = Category.objects.create(**cat_data)

        return JsonResponse({
            "id": cat.pk,
            "name": cat.name
        }, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({
            "id": cat.pk,
            "name": cat.name,
        },
            safe=False, json_dumps_params={'ensure_ascii': False}
        )
