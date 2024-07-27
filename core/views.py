from django.shortcuts import render,redirect
from django.http import HttpResponse
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,wishlist,ProductReview,Address
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404



# Create your views here.
@login_required(login_url='userauths:login')
def index(request):
    #products=Product.objects.all().order_by("-id")
    products=Product.objects.filter(product_status="published",featured=True).order_by("-id")
    ##reviews
    #product=Product.objects.get(pid=pid)
   # review=ProductReview.objects.filter(product=product)

    context={
        "products":products,
        #"review":review,

    }
    return render(request,'core/index.html',context)
@login_required
def booking_view(request):
    products = Product.objects.all().order_by("-id")
    product_id = request.GET.get('product_id')  # Get product_id from URL parameter

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Retrieve amount from form data and convert it to an integer
        amount_str = request.POST.get('amount', '0')  # Default to '0' if amount is not provided
        try:
            amount = int(amount_str)
        except ValueError:
            return render(request, 'core/error.html', {'message': 'Invalid amount. Please provide a valid integer amount.'})

        account_reference = 'Bikechapchap'
        transaction_desc = 'Rent a bike'
        callback_url = 'https://vidakpop.github.io/stk-push/'

        # Perform STK Push with the provided details
        cl = MpesaClient()
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        print(response.__dict__)

        # Check the response and handle accordingly
        if response.response_code == '0':
            # Transaction is successful, generate and save an invoice
            product = Product.objects.get(id=product_id)
            total_amount = amount
            invoice = CartOrder.objects.create(
                
                user=request.user,
                #product = Product.objects.get(id=product_id),
                phone_number=phone_number,
                price=total_amount
            )
            cart_order_products=CartOrderItems.objects.create(
                order=invoice,
                invoice_no="INVOICE_NO-"+str(invoice),
                item=product.title,
                image=product.image,
                price=amount,
                total=amount,
                
            )

            # Render success page with invoice details
            return render(request, 'core/success.html', {'message': 'Payment request initiated successfully!', 'invoice': invoice,'product':product,'cart_order_products':cart_order_products})
        else:
            return render(request, 'core/error.html', {'message': 'Failed to initiate payment request. Please try again.'})
    else: 
        if product_id:
            product = Product.objects.get(id=product_id)
            context = {"product": product}
            # Handle GET requests (e.g., show the form)
            return render(request, 'core/bookingform.html', context)

    return render(request, "core/bookingform.html", context)


def category_list_view(request):
    categories=Category.objects.all()
    context={
        "categories":categories
    }
    return render(request,'core/index.html',context)

def vendor_list_view(request):
    vendor=Vendor.objects.all()
    context={
        "vendor":vendor,
    }
    return render(request,"core/vendor.html",context)                

@login_required
def invoice_view(request):
    # Retrieve the invoice and related items from the database
    products = Product.objects.all().order_by("-id")
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    invoice = get_object_or_404(CartOrder, id=product_id)
    items = CartOrderItems.objects.filter(order=invoice)

    context = {
        'invoice': invoice,
        'items': items,
        'product':product,
    }

    return render(request, 'core/invoice.html', context)


def feedbackform_view(request):

    return render(request,'core/feedbackform.html')


       

@csrf_exempt  # Disable CSRF protection for this view as some payment gateways may not send the CSRF token
def handle_payment_callback(request):
    # Extract relevant information from the request
    products = Product.objects.all().order_by("-id")
    order_id = request.GET.get('product_id')  # Assuming your payment gateway sends the product_id parameter
    callback_path = request.GET.get('callback_path') # Get product_id from URL parameter # Assuming your payment gateway sends the order_id parameter
    # ... extract other details ...

    # Validate the authenticity of the callback (Check the documentation of your payment gateway)
    # For M-Pesa Daraja, you might need to verify the Lipa Na M-Pesa online payment status
    # Refer to the M-Pesa Daraja API documentation for details on verifying the callback

    # Example verification for M-Pesa Daraja (This is just a simplified example, follow the API documentation)
    # You should replace these lines with actual verification logic
    is_verified = True  # Replace this with your actual verification logic

    if is_verified:
        # Retrieve the corresponding order from your database
        
        order = get_object_or_404(CartOrder, id=order_id)

        # Update the order status or perform other necessary actions
        order.status = 'paid'
        order.save()

        # Return a response to the payment gateway
    else:
        # Handle failed verification
        return HttpResponse('Callback verification failed. Do not update the order.')

# Note: Depending on your payment gateway, you may need to implement more sophisticated verification logic.
