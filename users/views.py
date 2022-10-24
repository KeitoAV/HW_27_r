import json

from django.contrib import postgres
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.baseconv import base64
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from HW_27_r.settings import TOTAL_ON_PAGE
from users.models import User, Location


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        users = self.object_list.order_by('username')
        # pagination
        paginator = Paginator(users, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        response = {
            "items": [
                {
                    'id': user.pk,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'age': user.age,
                    'locations': list(map(str, user.location.all())),
                    'total_ads': user.ads.filter(is_published=True).count()
                } for user in obj],
            "total": paginator.count,
            "per_page": paginator.num_pages
        }

        return JsonResponse(response,
                            safe=False,
                            json_dumps_params={"ensure_ascii": False})


class UserDetailView(DetailView):
    model = User

    def get(self, *args, **kwargs):
        user = self.get_object()

        response = {
            'id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.location.all())),
            'total_ads': user.ads.filter(is_published=True).count()
        }

        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'first_name' in data:
            self.object.first_name = data['first_name']
        if 'last_name' in data:
            self.object.last_name = data['last_name']
        if 'age' in data:
            self.object.age = data['age']
        if 'role' in data:
            self.object.role = data['role']

        if 'locations' in data:
            for loc_name in data['locations']:
                loc, created = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        self.object.save()

        response = {
            'id': self.object.pk,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'role': self.object.role,
            'age': self.object.age,
            'locations': list(map(str, self.object.location.all())),
            'total_ads': self.object.ads.filter(is_published=True).count()
        }

        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'},
                            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        user = User.objects.create(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            password=data['password'],
            age=data['age']
        )

        # if 'password' in data:
        #     for password in data['password']:
        #         user.set_password(password)
        #         user.save()

        if 'locations' in data:
            for loc_name in data['locations']:
                loc, created = Location.objects.get_or_create(name=loc_name)
                user.location.add(loc)

        user.save()

        response = {
            'id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.location.all())),
            'total_ads': user.ads.filter(is_published=True).count()
        }

        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False})
