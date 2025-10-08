from django.db import models

# Create your models here

    

class CustomerModel(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.full_name




class YipForm(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    short_bio = models.TextField()
    resume_upload = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending Review'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    
 
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_name
