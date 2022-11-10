from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class City(models.Model):
    name = models.TextField(primary_key=True, verbose_name="name")
    population = models.PositiveIntegerField(verbose_name="population")
    photo = models.ImageField(upload_to='city_photos', null=True, blank=True)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def get_absolute_url(self):
        return reverse('city-detail', kwargs={'name':self.name})

    def __str__(self):
        return f'{self.name} city has {self.population} people'

    def __repr__(self):
        cls_name = type(self).__name__
        return (
            f'{cls_name}(name="{self.name}", '
            f'population={self.population})'
        )


class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cities = models.ManyToManyField(City, related_name='citizens')

    class Meta:
        verbose_name = 'citizen'
        verbose_name_plural = 'citizens'

    def __str__(self):
        return (
            f'{self.user} likes {self.cities}'
        )

    def __repr__(self):
        cls_name = type(self).__name__
        cities = [city for city in self.cities.all()]
        return (
            f'{cls_name}(city="{cities}", '
            f'user_id={self.user_id}'
        )

