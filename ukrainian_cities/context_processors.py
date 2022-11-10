from django.urls import reverse


def routers(request):
    return {
        'routers': {
            'index': reverse('index'),
            'cities': reverse('city-list'),
            'citizens': reverse('citizen-list'),
            # 'people': reverse('human-list'),
            'users': reverse('user-list')
        },
        'path': request.path
    }


