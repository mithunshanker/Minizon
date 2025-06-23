from django.shortcuts import redirect, render
from store.forms import AddressForm
from store.models import Adress
from django.contrib.auth.decorators import login_required

@login_required
def address_view(request):
    try:
        address = Adress.objects.get(user=request.user)
    except Adress.DoesNotExist:
        address = None

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('place_order')
    else:
        form = AddressForm(instance=address)

    return render(request, 'address_form.html', {'form': form, 'page_name': 'Address'})