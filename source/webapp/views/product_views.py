from django.contrib.auth.mixins import PermissionRequiredMixin
from webapp.forms import SearchForm, ProductForm
from webapp.models import Product
from webapp.views.base_views import SearchView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy


class ProductList(SearchView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    search_form_class = SearchForm
    search_fields = ['name__icontains']
    paginate_by = 5
    ordering = ['category', 'name']

    def get_queryset(self):
        return self.model.objects.filter(balance__gt=0)


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_view.html'


class ProductCreate(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    permission_required = 'webapp.add_product'

    def has_permission(self):
        return super().has_permission()

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk })


class ProductUpdate(PermissionRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'
    permission_required = 'webapp.change_product'

    def has_permission(self):
        return super().has_permission()

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk })


class ProductDelete(PermissionRequiredMixin,DeleteView):
    model = Product
    template_name = "product/product_delete.html"
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'

    def has_permission(self):
        return super().has_permission()