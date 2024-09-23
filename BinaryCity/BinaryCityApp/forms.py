from django import forms
from .models import Client, Contact

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'client_code']
        widgets = {
            'client_code': forms.TextInput(attrs={'readonly': 'readonly'}),  # Make client_code read-only
        }

    def save(self, commit=True):
        # Auto-generate client_code based on name (e.g., first three letters of the name + a random number)
        client = super().save(commit=False)
        if not client.client_code:
            client.client_code = self.generate_client_code(client.name)
        if commit:
            client.save()
        return client

    def generate_client_code(self, name):
        # Example: Generate client_code by taking first three letters of name + random number
        import random
        prefix = ''.join(e for e in name if e.isalnum())[:3].upper()  # First 3 letters (alphanumeric)
        suffix = str(random.randint(100, 999))  # Random 3-digit number
        return prefix + suffix





class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_name', 'contact_surname', 'phone_number', 'email', 'address']  # Fields to be rendered in the form

    # Optionally, you can add widgets and custom labels for the fields
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter full name'}))
    contact_surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter surname'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter address'}))
