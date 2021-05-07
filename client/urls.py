from django.urls import path

from client.views import ClientActionView, ClientListView, ClientDetailView, ClientUpdateView, \
    RegionListView, RegionUpdateView, ClientTypeListView, ClientTypeUpdateView

urlpatterns = [
    path('client-list/', ClientListView.as_view(), name='client-list'),
    path('client-detail/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client-update/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('region-list/', RegionListView.as_view(), name='region-list'),
    path('region-update/<int:pk>/', RegionUpdateView.as_view(), name='region-update'),
    path('client-type-list/', ClientTypeListView.as_view(), name='client-type-list'),
    path('client-type-update/<int:pk>/', ClientTypeUpdateView.as_view(), name='client-type-update'),
    path('client/action/', ClientActionView.as_view(), name='client_action'),
]
