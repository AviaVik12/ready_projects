from django import forms
from django.contrib.auth import get_user_model, login
from django.core.exceptions import BadRequest, PermissionDenied, ValidationError
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView
from django.views.generic.edit import FormView

from cities.models import Citizen, City

"""---Homepage-----------------------------------"""

User = get_user_model()


def index(request):
    context = {}
    return render(request, 'cities/index.html', context=context)


"""---Cities-------------------------------------"""


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', 'population', 'photo')
        widgets = {'name': forms.TextInput(),}
        
        
class CityDetailForm(CityForm):
    name = forms.CharField(disabled=True)


@require_http_methods(['GET', 'POST'])
def cities_list(request):
    cities = City.objects.order_by('-population', 'name')
    form = CityForm
    context = {
        'cities': cities,
        'form': form
    }
    
    if request.method == 'GET':
        return render(request, 'cities/cities.html', context=context)

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            City.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(request.path)

    context['form'] = form
    return render(request, 'cities/cities.html', context=context)


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    
    def get_success_url(self) -> str:
        created_city = self.get_context_data()['city']
        return reverse('city-datail', args=[created_city.name])


class CitiesListView(ListView, FormView):
    model = City
    form_class = CityForm
    ordering = ['-population', 'name']
    template_name = 'cities/cities.html'
    context_object_name = 'cities'

    def post(self, request, *args, **kwargs):
        cities = super().get_queryset()
        view = CityCreateView.as_view(
            extra_context={'cities': cities},
            template_name=self.template_name
        )
        return view(request, *args, **kwargs)


class CitiesDetailView(DetailView, UpdateView):
    model = City
    form_class = CityDetailForm
    template_name = 'cities/city_detail.html'
    context_object_name = 'city'
    pk_url_kwarg = 'name'


class CitiesDeleteView(DeleteView):
    model = City
    pk_url_kwarg = 'name'

    def get_success_url(self):
        return reverse('city-list')


"""---Administrative Divisions-------------------"""


def citizens_list(request):
    citizens = Citizen.objects.all()
    context = {'citizens': citizens}
    return render(request, 'cities/citizens.html', context=context)


"""---Users-------------------------------------"""


def users_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'cities/people.html', context=context)


class UserListView(ListView):
    model = User
    template_name = 'cities/people.html'
    context_object_name = 'users'
    
    
class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {'password': forms.PasswordInput()}
        
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 3:
            raise ValidationError('Password is too short!')
        else:
            return password
        
        
class CreateUserView(FormView):
    form_class = CreateUserForm
    template_name = 'cities/create_user.html'
    
    @property
    def success_path(self):
        return reverse('index')
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_path)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect(self.success_path)
        return render(request, self.template_name, {'form': form})

"""---Errors-------------------------------------"""


def server_death(request):
    raise Exception


def bad_request(request):
    raise BadRequest


def permission_denied(request):
    raise PermissionDenied
