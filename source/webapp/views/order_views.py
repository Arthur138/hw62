from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from webapp.models import Order , OrderProduct


class OrderList(LoginRequiredMixin , ListView):
    model = OrderProduct
    template_name = 'order/order_list.html'
    context_object_name = "orders"

    def get_queryset(self):
        return self.model.objects.filter(order__user = self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderList, self).get_context_data()
        return context