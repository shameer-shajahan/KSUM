from django.shortcuts import render, redirect
from .models import YipForm, AdminModel
from .forms import YipFormForm
from django.contrib import messages
from .models import AdminModel
from .forms import AdminLoginForm
from django.contrib.auth import logout as auth_logout 
import razorpay
from django.conf import settings


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))

def yipform_create(request):
    if request.method == 'POST':
        form = YipFormForm(request.POST, request.FILES)
        if form.is_valid():
          
            yipform = form.save(commit=False)
            yipform.status = 'Pending' 
            
       
            order_amount = 50 * 100  # ₹50 = 5000 paise
            order_currency = 'INR'

            payment_order = client.order.create(dict(
                amount=order_amount,
                currency=order_currency,
                payment_capture=1
            ))
            
            yipform.razorpay_order_id = payment_order['id'] 
            yipform.save()  
            
            context = {
                'form': form,
                'yipform': yipform,
                'order_id': payment_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': order_amount,
            }
            return render(request, 'yipform_payment.html', context)
    else:
        form = YipFormForm()
    return render(request, 'yipform_create.html', {'form': form})

    

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')

    # Update the form status to "Pending Review" after successful payment
    try:
        yipform = YipForm.objects.get(razorpay_order_id=order_id)
        yipform.status = 'Pending'  # ready for admin review
        yipform.save()
        message = "Payment successful! Form submitted for review."
    except YipForm.DoesNotExist:
        message = "Payment received, but form not found."

    return render(request, 'yipform_submitted.html', {'message': message})


def yipform_list(request):
    yipforms = YipForm.objects.all()
    return render(request, 'yipform_list.html', {'yipforms': yipforms})


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                admin = AdminModel.objects.get(email=email, password=password)
                # Set session
                request.session['admin_id'] = admin.id
                request.session['admin_name'] = admin.full_name
                return redirect('admin_dashboard')  
            except AdminModel.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})


def admin_logout(request):
    auth_logout(request)  
    request.session.flush()  
    return redirect('admin_login')


def admin_dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
    return render(request, 'admin_dashboard.html', {'admin_name': request.session.get('admin_name')})



