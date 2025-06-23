from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from weasyprint import HTML
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required

from store.models import Order
@login_required
def generate_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    template = get_template('pdf/receipt.html')
    html_string = template.render({'order': order})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}_receipt.pdf"'
    return response
