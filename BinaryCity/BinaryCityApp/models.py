from django.db import models
from django.core.exceptions import ValidationError
import re

class Client(models.Model):
    client_code = models.CharField(max_length=100, primary_key=True)  # client_code as the primary key
    name = models.CharField(max_length=255)  # name field

    def __str__(self):
        return self.name

    # Validation method for name
    def clean(self):
        # Ensure the name only contains letters and spaces (for simplicity)
        if not re.match(r'^[A-Za-z\s]+$', self.name):
            raise ValidationError("Name can only contain letters and spaces.")
        
        # Ensure the name is not blank
        if self.name.strip() == '':
            raise ValidationError("Name cannot be empty.")

    class Meta:
        ordering = ['name']  # Optional: order clients by name


class Contact(models.Model):
    contact_name = models.CharField(max_length=255)  # Full name of the contact
    contact_surname = models.CharField(max_length=255, default="Surname")  # Surname of the contact
    phone_number = models.CharField(max_length=15, unique=True)  # Phone number, assuming it needs to be unique
    email = models.EmailField(unique=True)  # Email address, unique to avoid duplicates
    address = models.TextField()  # Address as a text field to accommodate longer addresses
    date_added = models.DateTimeField(auto_now_add=True)  # Timestamp for when the contact was added
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts', default='NON')  # ForeignKey to Client

    def __str__(self):
        return f"{self.contact_name} ({self.email})"
