from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DeleteView, CreateView
from django.shortcuts import redirect, get_object_or_404
from webapp.models import Product, Cart, Order, OrderProduct
from webapp.forms import OrderForm
from django.contrib.sessions.models import Session


class AddItemToCart(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        if not request.session.get('cart'):
            request.session['cart'] = list()
        else:
            request.session['cart'] = list(request.session['cart'])

        app_data = {
            'product_id': product.pk,
            'qty' : request.POST.get('qty'),
        }

        request.session['cart'].append(app_data)

        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('webapp:index')


class CartList(ListView):
    model = Cart
    template_name = 'cart/index.html'
    context_object_name = "carts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['total'] = Cart.get_total()
        context['form'] = OrderForm
        cart = self.request.session.get('cart', {})
        for products in cart:
            qty = products['qty']
            for values in products.values():
                product = Product.objects.get(pk=values)
        if cart:
            cart = Cart.objects.create(product=product, qty=qty)
        else:
            pass
        return context


class CartDelete(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart_index')

    def get(self, request, *args, **kwargs):
        print(Cart.product_id)
        cart = self.request.session.get('cart', {})
        for prod in request.session['cart']:
            if prod['product_id'] == Cart.product_id:
                prod.clear()
        return self.delete(request, *args, **kwargs)


class CartDeleteOne(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart_index')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.qty -= 1
        if self.object.qty < 1:
            self.object.delete()
        else:
            self.object.save()
        return redirect(success_url)


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            order = form.save(commit=False)
            order.user = self.request.user
            order.save()
        else:
            order = form.save()

        for item in Cart.objects.all():
            OrderProduct.objects.create(product=item.product, qty=item.qty, order=order)
            item.product.balance -= item.qty
            item.product.save()
            item.delete()

        return redirect(self.success_url)
