from django.shortcuts import render
from .models import Drug, Cart, Type
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views.generic import ListView, CreateView, UpdateView
from .models import Supplier, Order, Prescription, AuditLog, Sale, Patient, Discount, StockAlert
from .forms import SupplierForm, OrderForm, PrescriptionForm, AuditLogForm, SaleForm, PatientForm, DiscountForm, StockAlertForm


def home(request):
    cart_count = 0
    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(user_id=request.user).first()
        cart_count = user_cart.drugs.count() if user_cart else 0
    
    drug_types = Type.objects.exclude(id__isnull=True)  # Fetch all Type objects

    context = {
        'posts': Drug.objects.all(),
        'cart_count': cart_count,  # Pass the cart count to the template
        'drug_types': drug_types,
    }
    return render(request, 'pharmacy/home.html', context)


def drugs_by_type(request, type_id):
    type_obj = get_object_or_404(Type, id=type_id)
    drugs = Drug.objects.filter(type=type_obj)
    context = {
        'type': type_obj,
        'drugs': drugs,
    }
    return render(request, 'pharmacy/drugs_by_type.html', context)

def drug_expiry_analysis(request):
    today = now()
    five_days_later = today + timedelta(days=5)

    expired_drugs = Drug.objects.filter(expiry__lt=today).count()
    expiring_soon = Drug.objects.filter(expiry__range=(today, five_days_later)).count()
    valid_drugs = Drug.objects.filter(expiry__gt=five_days_later).count()

    chart_data = {
        'labels': ['Expired', 'Expiring in 5 days', 'Valid (5+ days to expiry)'],
        'values': [expired_drugs, expiring_soon, valid_drugs],
    }

    return render(request, 'pharmacy/drug_expiry_analysis.html', {'chart_data': chart_data})




def about(request):
    return render(request, 'pharmacy/about.html', {'title': 'About'})



@login_required(login_url='login')
def add_to_cart(request, drug_id):
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"Login URL: {request.build_absolute_uri('/login/')}")
    drug = get_object_or_404(Drug, id=drug_id)
    user_cart, created = Cart.objects.get_or_create(user_id=request.user)

    # Avoid adding duplicates
    if drug.cart == user_cart:
        message = f"{drug.name} is already in your cart."
    else:
        drug.cart = user_cart
        drug.save()
        message = f"{drug.name} added to your cart."

    # Get the updated cart count
    cart_count = user_cart.drugs.count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': message, 'cart_count': cart_count})

    messages.success(request, message)
    return redirect('pharmacy-home')


def cart_page(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to view your cart.")
        return redirect('login')

    user_cart = Cart.objects.filter(user_id=request.user).first()
    drugs = user_cart.drugs.all() if user_cart else []

    # Calculate the total price
    total_price = sum(drug.price for drug in drugs) if drugs else 0

    context = {
        'drugs': drugs,
        'cart_count': user_cart.drugs.count() if user_cart else 0,  # Pass the cart count
        'total_price': total_price,  # Pass the total price to the template
    }
    return render(request, 'pharmacy/cart.html', context)


def remove_from_cart(request, drug_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to modify your cart.")
        return redirect('login')

    drug = get_object_or_404(Drug, id=drug_id)
    if drug.cart and drug.cart.user_id == request.user:
        drug.cart = None
        drug.save()
        messages.success(request, f"{drug.name} removed from your cart.")
    else:
        messages.error(request, "This item is not in your cart.")

    return redirect('cart-page')

@login_required(login_url='login')
def pay_now(request):
    # Placeholder logic for payment
    return render(request, 'pharmacy/pay_now.html', {'title': 'Checkout'})


# Generic create, update, delete views
def create_instance(request, model_form, template_name, success_url):
    if request.method == 'POST':
        form = model_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = model_form()
    return render(request, template_name, {'form': form})

def update_instance(request, instance, model_form, template_name, success_url):
    if request.method == 'POST':
        form = model_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = model_form(instance=instance)
    return render(request, template_name, {'form': form})

def delete_instance(request, instance, success_url):
    if request.method == 'POST':
        instance.delete()
        return redirect(success_url)
    return render(request, 'pharmacy/confirm_delete.html', {'object': instance})

# Model-specific views
def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'pharmacy/supplier_list.html', {'suppliers': suppliers})

def create_supplier(request):
    return create_instance(request, SupplierForm, 'pharmacy/supplier_form.html', 'supplier_list')

def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return update_instance(request, supplier, SupplierForm, 'pharmacy/supplier_form.html', 'supplier_list')

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return delete_instance(request, supplier, 'supplier_list')



# List View for Orders
class OrderListView(ListView):
    model = Order
    template_name = "pharmacy/order_list.html"
    context_object_name = "orders"

# Create View for a New Order
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "pharmacy/order_form.html"
    success_url = reverse_lazy("order-list")

# Update View for an Existing Order
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "pharmacy/order_form.html"
    success_url = reverse_lazy("order-list")




# List all prescriptions
class PrescriptionListView(ListView):
    model = Prescription
    template_name = "pharmacy/prescription_list.html"
    context_object_name = "prescriptions"

# View details of a prescription
class PrescriptionDetailView(DetailView):
    model = Prescription
    template_name = "pharmacy/prescription_detail.html"
    context_object_name = "prescription"

# Create a new prescription
class PrescriptionCreateView(CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "pharmacy/prescription_form.html"
    success_url = reverse_lazy("user-prescription-list")

# Update an existing prescription
class PrescriptionUpdateView(UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "pharmacy/prescription_form.html"
    success_url = reverse_lazy("user-prescription-list")

# Delete a prescription
class PrescriptionDeleteView(DeleteView):
    model = Prescription
    template_name = "pharmacy/prescription_confirm_delete.html"
    success_url = reverse_lazy("user-prescription-list")


class UserPrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = "pharmacy/user_prescriptions.html"
    context_object_name = "prescriptions"

    def get_queryset(self):
        return Prescription.objects.filter(prescribed_to=self.request.user)

class PrescriptionCreateView(LoginRequiredMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "pharmacy/prescription_form.html"
    success_url = reverse_lazy("user-prescription-list")
