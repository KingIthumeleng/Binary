from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from .tables import *
from django.http import HttpResponse


def client_page_view(request):
    form = ClientForm()
    if request.method == 'POST':
        name = request.POST.get('name')

        # Check if the name contains more than one word
        name_parts = name.split()

        
        if len(name_parts) == 1:
            # Single-word name: take the first 3 letters or pad with 'A'
            client_code_letters = (name[:3].upper() if len(name) >= 3 else name.upper().ljust(3, 'A'))
        elif len(name_parts) == 2:
            # Two-word name: take the first letter of each word and pad with 'A'
            client_code_letters = ''.join([word[0] for word in name_parts if word]).upper().ljust(3, 'A')
        else:
            # More than two words: take the first letter of up to 3 words
            client_code_letters = ''.join([word[0] for word in name_parts[:3] if word]).upper()

        clients_with_code = Client.objects.filter(client_code__contains = client_code_letters)

        code_index = len(clients_with_code) + 1

        code_index = str(code_index).zfill(3)

        client_code = client_code_letters + str(code_index)

        # Save the Client object with the auto-generated client_code
        client = Client(name=name, client_code=client_code)
        client.save()

        # Redirect to a success page or handle further logic
        return redirect('success_contact_added')

    else:
        form = ClientForm()
        
        contacts = Contact.objects.filter(client__isnull=False)

        contacts_count = len(contacts)

        # Create a table instance with the fetched clients
        contactTable = ContactTable(contacts)

        print("The contact content: ", contacts)

        # Fetch all clients from the database
        clients = Client.objects.all()

        client_data_with_int = []

        # Loop through each client instance
        for clientInstance in clients:
            # Count the number of linked contacts for the current client
            linked_contact_count = Contact.objects.filter(client=clientInstance).count()
            
            # Print the number of linked contacts for debugging purposes
            print(f"Number of contacts linked to client {clientInstance.client_code}: {linked_contact_count}")
            
            # Append client data including contact count
            client_data_with_int.append({
                'name': clientInstance.name,  # Assuming 'name' field exists in Client model
                'client_code': clientInstance.client_code,
                'num_clients_int': linked_contact_count
            })


        client_count = len(client_data_with_int)

        # Create a table instance with the modified clients data
        clientTable = ClientTable(client_data_with_int)

        return render(request, 'clients_page.html', {'form': form, 'contactTable': contactTable, 'clientTableView': clientTable, 'client_count': client_count, 'contacts_count': contacts_count,})

def contact_page_view(request):
    form = ContactForm()
    if request.method == 'POST':
        contact_name = request.POST.get('contact_name')
        contact_surname = request.POST.get('contact_surname')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')


    
        # Check if a Contact with the same email already exists
        if Contact.objects.filter(email=email).exists() or Contact.objects.filter(phone_number=phone_number).exists():
            # Handle the case where the email is already taken
            return HttpResponse("A contact with this email or phone already exists.")
        
        # Create and save the contact object
        contact = Contact(contact_name=contact_name, contact_surname = contact_surname, phone_number=phone_number, email=email, address=address)
        contact.save()
        return redirect('success_contact_added')
    else:
        form = ContactForm()  # Display an empty form

        # Fetch all clients from the database
        clients = Client.objects.all()

        # Create a table instance with the fetched clients
        clientTable = ClientTableContactPage(clients)

        # Fetch all clients from the database
        contacts = Contact.objects.all()

        # Create a table instance with the modified clients data
        contactTablePage = ContactTablePage(contacts)

        print("Table created", contactTablePage)

        return render(request, 'contacts_page.html', {'form': form, 'clientTableView': clientTable, 'contactTable': contactTablePage})  # Pass the form to the template

def success_contact_added(request):
    return render(request, 'client_succesful.html')

def success_contact_linked(request,client_code):
    if request.method == 'POST':
        selected_contacts = request.POST.getlist('selected_contacts')
        # Logic to link the selected contacts to the client
        for contact_id in selected_contacts:
            # Assuming contact_id is provided
            contact = get_object_or_404(Contact, id=contact_id)

            # Assuming client_code is the new value provided and exists in the Client model
            client = get_object_or_404(Client, client_code=client_code)

            # Update the contact's client reference
            contact.client = client
            contact.save()

        return redirect('client_view')
    
    contacts = Contact.objects.filter(client__isnull=True)

    return render(request, 'client_linking.html', {
        'contacts': contacts,
    })

def success_client_link(request,contact_code):
    if request.method == 'POST':
        selected_client = request.POST.getList('selected_contacts')
        # Logic to link the selected contacts to the client
        # Assuming contact_id is provided
        contact = get_object_or_404(Contact, id=contact_code)

        # Assuming client_code is the new value provided and exists in the Client model
        client = get_object_or_404(Client, client_code=selected_client)

        # Update the contact's client reference
        contact.client = client
        contact.save()

        return redirect('client_view')
    

    print("Linking contact", contact_code)



    contacts = Contact.objects.filter(client__client_code = 'NON')


    print("Conactsw", contacts)



    return render(request, 'client_linking.html', {
        'contacts': contacts,
    })

def success_contact_unlinked(request, contact_code):

    print("unlinking contact", contact_code)

    contact = get_object_or_404(Contact, id=contact_code)

    print("contact ids", contact)
    
    # # Update the client code
    contact.client = None
    contact.save() 

    print("contact ids after unlinking", contact)

    return redirect('client_view')

def deleteDB(request):
        Contact.objects.all().delete()
        Client.objects.all().delete()
        return render(request, 'deletesContent.html', {})

