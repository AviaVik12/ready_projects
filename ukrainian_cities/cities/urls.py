from django.urls import path
from cities import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users_list, name='user-list'),
    path('usersview/', views.UserListView.as_view(), name="user-list"),
    path('cities/', views.CitiesListView.as_view(), name='city-list'),
    path('cities/<name>/', views.CitiesDetailView.as_view(), name='city-detail'),
    path('cities/<name>/delete/', views.CitiesDeleteView.as_view(), name='city-delete'),
    path('citizens/', views.citizens_list, name='citizen-list'),
    # path('people/', views.people_list, name='human-list'),
    path('500-error/', views.server_death, name='server_death'),
    path('400-error/', views.bad_request, name='bad-request'),
    path('403-error/', views.permission_denied, name='permission-denied')
]


