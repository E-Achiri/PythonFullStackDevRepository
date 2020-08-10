from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.create_user),
    path('dashboard', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('trips/new', views.trip_page),
    path('create_trip', views.plan_trip),
    path('remove/<int:x>', views.destroy),
    path('trips/<int:x>/update', views.updateTrip),
    path('trips/edit/<int:x>', views.editTrip),
    path('trips/<int:x>', views.tripage),
    path('join/<int:x>', views.joinATrip),
    path('cancel/<int:x>', views.cancel)

]