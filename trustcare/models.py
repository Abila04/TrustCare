from django.db import models
class tbl_admin(models.Model):
    email = models.EmailField() 
    password = models.CharField(max_length=100) 


from django.db import models

class tbl_volunteer(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

 
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    service_type = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],default="pending")
    availability = models.BooleanField(default=True)
    place = models.CharField(max_length=255)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    aadhaar_pic = models.ImageField(upload_to='aadhaar_pics/')
    profile_pic = models.ImageField(upload_to='profile_pics/')
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=10)
    resume = models.FileField(upload_to='resume/')  # Ensure this field is defined


    def __str__(self):
        return f"{self.name} ({self.email})"

    
    
class tbl_user(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()  # Shorter email length
    password = models.CharField(max_length=100) 
    address = models.TextField(max_length=100)
    DOB = models.DateField(max_length=100)
    Phone = models.CharField(max_length=100)



class tbl_service(models.Model):
    SERVICE_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable')
    ]

    service_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='services/images/')
    status = models.CharField(max_length=20, choices=SERVICE_STATUS_CHOICES, default='Available')

    def __str__(self):
        return self.service_name

    
from django.db import models


class Allocation(models.Model):
    appointment = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name="allocations")
    volunteer = models.ForeignKey(tbl_volunteer, on_delete=models.CASCADE, related_name="allocations")
    allocated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending') 

    def __str__(self):
        return f"Allocation: {self.appointment} -> {self.volunteer}"
    
    
    
class Booking(models.Model):
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)  # Assuming the user is logged in and using Django's default User model
    service = models.ForeignKey(tbl_service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Booking for {self.service.service_name} by {self.name}"



from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Payment(models.Model):
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], default='PENDING')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
