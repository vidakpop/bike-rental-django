

# Bike Rental System

A comprehensive Bike Rental system built using Django, with integrated payment capabilities via M-Pesa STK (Sim Tool Kit).

## Features

- User registration and authentication
- Browse and search for available bikes
- Book and rent bikes
- Integrated M-Pesa STK payment for bike rentals
- Admin panel to manage bikes, rentals, and users

## Prerequisites

- Python 3.x
- Django 3.x or later
- SQLite (default) or any other preferred database
- M-Pesa credentials for payment integration

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bike-rental-system.git
   cd bike-rental-system
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup the database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000` in your browser to see the app in action.

## M-Pesa STK Integration

1. **Install the required package for M-Pesa integration**
   ```bash
   pip install django-daraja
   ```

2. **Configure M-Pesa settings**

   Add the following settings to your `settings.py`:
   ```python
   MPESA_ENVIRONMENT = 'sandbox'  # or 'production'
   MPESA_CONSUMER_KEY = 'your_consumer_key'
   MPESA_CONSUMER_SECRET = 'your_consumer_secret'
   MPESA_SHORTCODE = 'your_shortcode'
   MPESA_PASSKEY = 'your_lipa_na_mpesa_online_passkey'
   ```

3. **Update your `urls.py` to include M-Pesa endpoints**
   ```python
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('mpesa/', include('daraja.urls')),
       # Other paths...
   ]
   ```

4. **Create payment views**

   In your `views.py`, add the logic to handle M-Pesa payments:
   ```python
   from django_daraja.mpesa.core import MpesaClient
   from django.conf import settings
   from django.http import JsonResponse

   mpesa_client = MpesaClient()
   lipa_na_mpesa_online_url = 'your_callback_url'

   def mpesa_payment(request):
       phone_number = request.POST.get('phone')
       amount = request.POST.get('amount')
       account_reference = 'BikeRental'
       transaction_desc = 'Bike rental payment'
       callback_url = lipa_na_mpesa_online_url

       response = mpesa_client.lipa_na_mpesa_online(
           phone_number, 
           amount, 
           account_reference, 
           transaction_desc, 
           callback_url
       )
       return JsonResponse(response)
   ```

5. **Update your booking process to include the M-Pesa payment**

   Modify your booking view to handle payments:
   ```python
   from django.shortcuts import render, redirect
   from django.http import HttpResponse
   from .models import Bike, Rental
   from .forms import BookingForm
   from .views import mpesa_payment

   def book_bike(request, bike_id):
       bike = Bike.objects.get(id=bike_id)
       if request.method == 'POST':
           form = BookingForm(request.POST)
           if form.is_valid():
               rental = form.save(commit=False)
               rental.bike = bike
               rental.user = request.user
               rental.save()
               return redirect(mpesa_payment)
       else:
           form = BookingForm()
       return render(request, 'book_bike.html', {'form': form, 'bike': bike})
   ```

## Usage

1. **Register an account**: Users can register for an account to start renting bikes.

2. **Browse available bikes**: Users can browse and search for available bikes.

3. **Book a bike**: Once a bike is selected, users can book the bike by providing necessary details.

4. **Make a payment**: Users will be redirected to make a payment via M-Pesa STK.

5. **Manage rentals**: Users can view their rental history and manage ongoing rentals.

6. **Admin panel**: Admins can manage bikes, rentals, and users through the Django admin panel.

## Contributing

We welcome contributions! Please fork the repository and create a pull request.

