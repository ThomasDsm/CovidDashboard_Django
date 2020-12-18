from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('prov', views.prov, name='prov'),
	path('reg', views.reg, name='reg'),
]
