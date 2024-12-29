from django import forms
from .models import Supplier, Order, Prescription, AuditLog, Sale, Patient, Discount, StockAlert


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'expected_delivery_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    # Override the default initialization to set the format
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.expected_delivery_date:
            self.fields['expected_delivery_date'].initial = self.instance.expected_delivery_date.strftime('%Y-%m-%dT%H:%M')

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['drug', 'prescribed_to', 'dosage', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class AuditLogForm(forms.ModelForm):
    class Meta:
        model = AuditLog
        fields = '__all__'
        
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'

class StockAlertForm(forms.ModelForm):
    class Meta:
        model = StockAlert
        fields = '__all__'