from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(embargo_date__gte=start_date)
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(embargo_date__lte=end_date)
        return queryset
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
