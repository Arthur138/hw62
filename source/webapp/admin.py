from django.contrib import admin
from webapp.models import Product , Order , OrderProduct , Cart


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'balance', 'price']
    list_filter = ['category']
    search_fields = ['name', 'description']
    exclude = []


admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)
# Register your models here.
