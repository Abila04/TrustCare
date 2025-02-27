from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
import re
from .models import*

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'volunteer/about.html')

def user_reg(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address = request.POST['address']
        dob = request.POST['dob']  # Retrieve Date of Birth
        phone = request.POST['phone']

        # Password Confirmation Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif tbl_user.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        elif tbl_user.objects.filter(name=name).exists():
            messages.error(request, "Username already exists.")  # Ensure you are checking the right field
        else:
            # Save the user
            user = tbl_user.objects.create(
                name=name,
                email=email,
                password=password,  
                address=address,
                DOB=dob,
                Phone=phone
            )
            user.save()
            messages.success(request, "User registered successfully! Please log in.")
            return redirect('login')  # Adjust 'login' if necessary
    return render(request, 'user_reg.html')




def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Query to check credentials
        admin_var = tbl_admin.objects.filter(email=email, password=password).first()
        user_var = tbl_user.objects.filter(email=email, password=password).first()
        volunteer_var = tbl_volunteer.objects.filter(email=email, password=password).first()

        # Check admin login
        if admin_var:
            request.session['id'] = admin_var.id
            return render(request, 'admin/admin_index.html')

        # Check user login
        elif user_var:
            request.session['id'] = user_var.id
            return render(request, 'user/user_index.html')

        # Check volunteer login
        elif volunteer_var:
            if volunteer_var.status == 'approved':  
                request.session['id'] = volunteer_var.id
                return render(request, 'volunteer/vol_index.html')
            elif volunteer_var.status == 'pending':  
                return HttpResponse(
                    "<script>alert('Your registration is still pending approval.');window.location='/';</script>"
                )

        # Invalid credentials
        else:
            return HttpResponse(
                "<script>alert('Invalid email or password! Please try again.');window.location='/login/';</script>"
            )

    return render(request,'login.html')


def volunteer_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        qualification = request.POST.get('qualification')
        service_type = request.POST.get('service_type')
        place = request.POST.get('place')
        aadhaar_number = request.POST.get('aadhaar_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Handle file uploads
        aadhaar_pic = request.FILES.get('aadhaar_pic')
        profile_pic = request.FILES.get('profile_pic')
        resume = request.FILES.get('resume')

        # Validate form inputs
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('volunteer_register')

        if tbl_volunteer.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('volunteer_register')

        if tbl_volunteer.objects.filter(aadhaar_number=aadhaar_number).exists():
            messages.error(request, "Aadhaar number already registered!")
            return redirect('volunteer_register')

        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):  # type: ignore
            messages.error(request, "Please enter a valid email address.")
            return redirect('volunteer_register')

        # Validate phone number format (10 digits)
        phone_pattern = r'^\d{10}$'
        if not re.match(phone_pattern, phone):  # type: ignore
            messages.error(request, "Please enter a valid phone number (10 digits).")
            return redirect('volunteer_register')

        # Validate file uploads (optional)
        if aadhaar_pic and not aadhaar_pic.name.lower().endswith(('jpg', 'jpeg', 'png')):
            messages.error(request, "Aadhaar picture must be an image file (JPG, JPEG, PNG).")
            return redirect('volunteer_register')

        if profile_pic and not profile_pic.name.lower().endswith(('jpg', 'jpeg', 'png')):
            messages.error(request, "Profile picture must be an image file (JPG, JPEG, PNG).")
            return redirect('volunteer_register')

        if resume and not resume.name.lower().endswith(('pdf', 'doc', 'docx')):
            messages.error(request, "Resume must be a file of type PDF, DOC, or DOCX.JPG,PNG,JPEJ")
            return redirect('volunteer_register')

        # Save the volunteer
        volunteer = tbl_volunteer(
            name=name,
            email=email,
            password=password,  # Save the plain text password
            qualification=qualification,
            service_type=service_type,
            place=place,
            aadhaar_number=aadhaar_number,
            aadhaar_pic=aadhaar_pic,
            profile_pic=profile_pic,
            gender=gender,
            dob=dob,
            address=address,
            phone=phone,
            resume=resume,  # Save the uploaded resume file
        )
        volunteer.save()

        messages.success(request, "Registration successful!")
        return redirect('login')  # Redirect to the login page

    return render(request, 'volunteer_register.html')



def admin_index(request):
    return render(request, 'admin/admin_index.html')

def admin_view_vol(request):
    data = tbl_volunteer.objects.filter(status='pending')  
    return render(request, 'admin/admin_view_vol.html', {'data': data})


def admin_approve_vol(request):
    id=request.GET['id']
    tbl_volunteer.objects.filter(id=id).update(status='approved') 
    return redirect('admin_view_vol')



def admin_view_approved_vol(request):
    data=tbl_volunteer.objects.all().filter(status='approved')
    return render(request,'admin/admin_view_approved_vol.html',{'data':data})



from django.shortcuts import get_object_or_404, redirect


def admin_reject_vol(request):
    volunteer_id = request.GET.get('id')
    if volunteer_id:
        volunteer = get_object_or_404(tbl_volunteer, id=volunteer_id)
        volunteer.status = 'rejected'  # Make sure to have a status field for rejection
        volunteer.save()
    return render(request, 'admin/admin_view_rejected_vol.html') # Redirect to the rejected volunteers page



def admin_view_rejected_vol(request):
    rejected_volunteers = tbl_volunteer.objects.filter(status='rejected')
    return render(request, 'admin/admin_view_rejected_vol.html', {'data': rejected_volunteers})


def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return render(request,'index.html')


def admin_view_user(request):
    data = tbl_user.objects.defer('password')  # Exclude the 'password' field from the query
    return render(request, 'admin/admin_view_user.html', {'data': data})


def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return render(request,'index.html')



def adm_addserv(request):
    if request.method == 'POST':
        service_name = request.POST['service_name']
        description = request.POST['description']
        status = request.POST['status']
        image = request.FILES.get('image')

        # Create the service object without category
        tbl_service.objects.create(
            service_name=service_name,
            description=description,
            status=status,
            image=image
        )
        return redirect('service_list')  # Redirect to a service listing page or another relevant page

    return render(request, 'admin/adm_addserv.html')  # No need to pass categories anymore


def service_list(request):
    """
    Displays a list of all available services.
    """
    services = tbl_service.objects.all()  # Fetch all services from the database
    return render(request, 'admin/service_list.html', {'services': services})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def delete_service(request, service_id):
    """
    Deletes a specific service based on the provided service ID.
    """
    service = get_object_or_404(tbl_service, id=service_id)  # Fetch the service or return a 404 error
    service.delete()  # Delete the service
    messages.success(request, "Service deleted successfully.")  # Optional: Add a success message
    return redirect('service_list')  # Redirect to the service listing page




def user_view_service(request):
    services = tbl_service.objects.all()  # type: ignore # Get all services to display
    return render(request, 'user/user_serv.html', {'services': services})


def admin_view_appointments(request):
    # Fetch all appointments for the admin
    appointments = Booking.objects.all().order_by('appointment_date')  # Order by date or as needed
    
    return render(request, 'admin/admin_view_appointments.html', {'appointments': appointments})

from django.contrib import messages
from django.shortcuts import render
# from .models import Appointment




def user_view_booking(request):
    # Get the user ID from the session
    user_id = request.session.get('id')

    # Check if the user is logged in (if no ID in session, redirect to login)
    if not user_id:
        messages.error(request, "You need to log in to view your bookings.")
        return redirect('login')  # Adjust this to your login URL
    
    # Fetch the bookings for the logged-in user using the ID from session
    bookings = Booking.objects.filter(user_id=user_id)

    # Pass the bookings to the template for rendering
    return render(request, 'user/user_view_booking.html', {'booking': bookings})


def cancel_booking(request, booking_id):
    user_id = request.session.get('id')
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.success(request, "Your booking has been canceled successfully.")

    return redirect('user_view_booking') 

def admin_view_booking(request):
    """
    View for admin to view all user booking.
    """
    bookings = Booking.objects.filter(status="pending")

    return render(request, 'admin/admin_view_booking.html', {'booking': bookings}) # type: ignore

def admin_view_allocated_booking(request):
    """
    View for admin to view all user booking.
    """
    bookings = Allocation.objects.all()

    return render(request, 'admin/admin_view_allocated_booking.html', {'booking': bookings}) # type: ignore

def allocate_volunteer(request, booking_id):
    # Fetch the booking record
    booking = get_object_or_404(Booking, id=booking_id)

    # Filter volunteers based on service type, approval status, and availability
    volunteers = tbl_volunteer.objects.filter(
        service_type__icontains=booking.service,  
        status="approved",                       
        availability=True  # Boolean check
    )

    if request.method == 'POST':
        # Get volunteer_id from the form
        volunteer_id = request.POST.get('volunteer_id')

        if not volunteer_id:
            messages.error(request, "Please select a volunteer.")
            return redirect('allocate_volunteer', booking_id=booking_id)

        volunteer = get_object_or_404(tbl_volunteer, id=volunteer_id)

        # Create an allocation record
        Allocation.objects.create(
            appointment=booking,
            volunteer=volunteer
        )

        # Update booking status and volunteer availability
        booking.status = "allocated"
        booking.save()

        volunteer.availability = False  # Correct Boolean value
        volunteer.save()

        messages.success(request, f"Volunteer {volunteer.name} has been allocated to the booking.")
        return redirect('admin_view_booking')

    return render(request, 'admin/allocate_volunteer.html', {
        'booking': booking,
        'volunteers': volunteers,
    })

    

def vol_view_assigned_tasks(request):
    # Get the logged-in volunteer (assuming they are authenticated)
    volunteer_id = request.session.get('id')  # Assumes the user is a volunteer and logged in

    # Fetch tasks assigned to the logged-in volunteer
    vol_view_assigned_tasks= Allocation.objects.filter(volunteer=volunteer_id)

    # Render the template and pass the assigned tasks
    return render(request, 'volunteer/vol_view_assigned_tasks.html', {
        'vol_view_assigned_tasks': vol_view_assigned_tasks
    })
    
def volunteer_availability(request, volunteer_id):
    try:
        volunteer = get_object_or_404(tbl_volunteer, id=volunteer_id)
        volunteer.status = 'Unavailable' if volunteer.status == 'Available' else 'Available'
        volunteer.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except tbl_volunteer.DoesNotExist:
        return HttpResponse("Volunteer not found", status=404)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import tbl_service, tbl_user, Booking

def book_service(request, service_id):
    service = get_object_or_404(tbl_service, pk=service_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
    else:
        # Try to get the user from the session
        user_id = request.session.get('id')  # Using 'id' based on your login logic
        if user_id:
            user = get_object_or_404(tbl_user, pk=user_id)
        else:
            # If the user is neither authenticated nor in session, don't force redirect
            # instead, you can display a message or handle accordingly.
            messages.error(request, "You must be logged in to book a service.")
            return redirect('login')  # You can redirect to login or show a message as per your flow.

    if request.method == 'POST':
        # Retrieve the form data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        # Create and save the booking
        booking = Booking(
            user=user,  # This will be either the logged-in user or user from session
            service=service,
            name=name,
            email=email,
            address=address,
            phone=phone,
            message=message,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )
        booking.save()

        # Pass the booking and service data to the payment page
        return redirect('payment_page', booking_id=booking.id)  # Pass booking_id to the payment page

    return render(request, 'user/book_service.html', {'service': service})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking, Payment, tbl_user

def payment_page(request, booking_id):
    # Fetch the booking object
    booking = get_object_or_404(Booking, id=booking_id)
    fixed_amount = 500.00  # Fixed amount for payment

    # Fetch the user from the session
    user_id = request.session.get('id')  # Retrieve user ID from session
    if not user_id:
        messages.error(request, "You must be logged in to make a payment.")
        return redirect('login')  # Redirect to login if user not logged in

    user = get_object_or_404(tbl_user, id=user_id)  # Get user object

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Basic validation for card details
        if not (card_number and expiry_date and cvv):
            messages.error(request, "Please fill in all card details.")
            return render(request, 'user/payment_page.html', {'booking': booking, 'price': fixed_amount})

        # Simulate payment processing
        payment_status = 'SUCCESS'  # Simulate a successful payment
        transaction_id = 'TXN' + str(booking_id)  # Simulated transaction ID

        # Create the payment record
        payment = Payment.objects.create(
            user=user,
            booking=booking,
            amount=fixed_amount,
            status=payment_status,
            transaction_id=transaction_id
        )

        if payment.status == 'SUCCESS':
            messages.success(request, "Payment successful!")
            return redirect('success_page', payment_id=payment.id)
        else:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('payment_page', booking_id=booking_id)

    return render(request, 'user/payment_page.html', {'booking': booking, 'price': fixed_amount})
def success_page(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'user/success_page.html', {'payment': payment})
