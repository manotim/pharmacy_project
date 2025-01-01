from django.urls import path 
from . import views 
from .views import (
    OrderListView,
    OrderCreateView, 
    OrderUpdateView,
    PrescriptionListView, 
    PrescriptionDetailView, 
    PrescriptionCreateView, 
    PrescriptionUpdateView, 
    PrescriptionDeleteView,
    AuditLogListView,
    SaleListView,
    SaleCreateView
)

urlpatterns = [
    path('', views.home, name='pharmacy-home'),
    path('type/<uuid:type_id>/', views.drugs_by_type, name='drugs-by-type'),
    path('analysis/', views.drug_expiry_analysis, name='drug-expiry-analysis'),
    path('about/', views.about, name='pharmacy-about'),
    path('add-to-cart/<uuid:drug_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_page, name='cart-page'),
    path('remove-from-cart/<uuid:drug_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('pay-now/', views.pay_now, name='pay-now'),
    #Add URL patterns for suppliers,
    path('suppliers/', views.list_suppliers, name='supplier_list'),
    path('suppliers/create/', views.create_supplier, name='supplier_create'),
    path('suppliers/update/<uuid:pk>/', views.update_supplier, name='supplier_update'),
    path('suppliers/delete/<uuid:pk>/', views.delete_supplier, name='supplier_delete'),
    # Add URL patterns for Order,
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/new/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<uuid:pk>/edit/", OrderUpdateView.as_view(), name="order-update"),
    # Add URL for AddPrescription,
     path('prescriptions/', PrescriptionListView.as_view(), name='user-prescription-list'),
    path('prescriptions/<uuid:pk>/', PrescriptionDetailView.as_view(), name='prescription-detail'),
    path('prescriptions/add/', PrescriptionCreateView.as_view(), name='prescription-create'),
    path('prescriptions/<uuid:pk>/edit/', PrescriptionUpdateView.as_view(), name='prescription-update'),
    path('prescriptions/<uuid:pk>/delete/', PrescriptionDeleteView.as_view(), name='prescription-delete'),
    #uditLog, 
     path("audit-logs/", AuditLogListView.as_view(), name="audit-log-list"),
    #  Sale, Patient, Discount, StockAlert
     path("sales/", SaleListView.as_view(), name="sale-list"),
    path("sales/create/", SaleCreateView.as_view(), name="sale-create"),
]
