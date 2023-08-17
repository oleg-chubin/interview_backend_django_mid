
from django.urls import path, re_path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, DeactivateOrderView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    re_path(r'^(?P<pk>\d+)/$', DeactivateOrderView.as_view(), name='order-deactivate'),
]
