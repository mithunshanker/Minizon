from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import Product, Order, Order_item
from django.db.models import Sum, Count
import plotly.graph_objs as go
import plotly.offline as opy
from .models import *


class CustomAdminSite(admin.AdminSite):
    site_header = '🛒 E-Commerce Admin'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view))
        ]
        return my_urls + urls

    def dashboard_view(self, request):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(order_status="Placed").aggregate(Sum("total_price"))['total_price__sum'] or 0
        total_products = Product.objects.count()

        top_products = (
            Order_item.objects
            .values('product__name')
            .annotate(quantity=Sum('quantity'))
            .order_by('-quantity')[:5]
        )

        product_names = [item['product__name'] for item in top_products]
        quantities = [item['quantity'] for item in top_products]

        bar_chart = go.Figure([go.Bar(x=product_names, y=quantities)])
        bar_chart.update_layout(title='Top 5 Selling Products')
        chart_div = opy.plot(bar_chart, auto_open=False, output_type='div')

        context = dict(
            self.each_context(request),
            total_orders=total_orders,
            total_revenue=total_revenue,
            total_products=total_products,
            chart=chart_div,
        )
        return TemplateResponse(request, "admin/custom_dashboard.html", context)


admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(Product)
admin_site.register(Categories)
admin_site.register(Order)
admin_site.register(Order_item)
admin_site.register(Cart)
admin_site.register(Cartitem)
admin_site.register(Adress)