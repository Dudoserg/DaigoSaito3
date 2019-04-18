from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='asdf'),

    path('product', views.product, name='product'),


    path('product/<int:idparam>/edit', views.productEdit, name='productEdit'),

    path('product/<int:id>/', views.productPage, name='productPage'),

    path('product/<int:idparam>/editajax', views.productEditajax, name='productEditajax'),


    path('product/<int:idparam>/addMaterial', views.productAddMaterial, name='productAddMaterial'),


    path('product/<int:idparam>/editPosition', views.productEditPosition, name='productEditPosition'),


    path('zlp/<int:pk>/', views.post_list, name='asdf'),

    path('product/place_search', views.get_queryset, name='place_search')

]

# urlpatterns = patterns(
# '',
# url(r'^place_search/$', PlaceListView.as_view, name='place_search'),)
