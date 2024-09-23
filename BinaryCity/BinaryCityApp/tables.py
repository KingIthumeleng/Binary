import django_tables2 as tables
from .models import *

class ClientTable(tables.Table):

    number_of_clients_column = tables.Column(verbose_name='Number of Clients', accessor='num_clients_int')
    view_link = tables.LinkColumn('client_link', args=[tables.A('client_code')], text='Link Clients', verbose_name='Link Contact')


    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap.html"  # Using Bootstrap table style
        fields = ('client_code', 'name')  # Define the fields to display in the table
        order_by = 'name'  # Default ordering by name

class ContactTable(tables.Table):

    view_link = tables.LinkColumn('client_unlink', args=[tables.A('id')], text='Unlink', verbose_name='Unlink Contact')


    class Meta:
        model = Contact
        template_name = "django_tables2/bootstrap.html"  # Use bootstrap for styling (or change as needed)
        fields = ("contact_name", "phone_number", "email", "address", "date_added", "client")  # Fields to display in the table
        