from django.urls import path,include
from core.views import vendor_list_view
from core import views
app_name="core"

urlpatterns=[
    path("", views.index,name="index"),
    path("book/", views.booking_view,name="bookingform"),
    path("feedback/", views.feedbackform_view,name="feedbackform"),
    path('payment-callback/', views.handle_payment_callback, name='payment_callback'),
    path('book/invoice/', views.invoice_view, name='invoice'),

    ##path("mpesa/", views.mpesa,name="mpesa"),
    #path('mpesa_payment/', views.mpesa_payment, name='mpesa_payment'),
    #path("mpesa_payment/daraja/stk_push", views.stk_push_callback,name="stk_push_callback"),
    
    
   path("vendor/", views.vendor_list_view,name="vendor"),
]