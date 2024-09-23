from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from .tables import *

def client_page_view(request):
    form = ClientForm()
    if request.method == 'POST':
        name = request.POST.get('name')

        # Check if the name contains more than one word
        name_parts = name.split()

        
        if len(name_parts) == 1:
            # Single-word name: take the first 3 letters or pad with 'A'
            client_code = (name[:3].upper() if len(name) >= 3 else name.upper().ljust(3, 'A'))
        elif len(name_parts) == 2:
            # Two-word name: take the first letter of each word and pad with 'A'
            client_code = ''.join([word[0] for word in name_parts if word]).upper().ljust(3, 'A')
        else:
            # More than two words: take the first letter of up to 3 words
            client_code = ''.join([word[0] for word in name_parts[:3] if word]).upper()



        print("The generated client code is:", client_code)

        # Save the Client object with the auto-generated client_code
        client = Client(name=name, client_code=client_code)
        client.save()

        # Redirect to a success page or handle further logic
        return redirect('success_contact_added')

    else:
        form = ClientForm()
        # Fetch all clients from the database
        contacts = Contact.objects.exclude(client = 'nonfhgfh')

        # Create a table instance with the fetched clients
        contactTable = ContactTable(contacts)

        # Fetch all clients from the database
        clients = Client.objects.all()


        # Custom integer values corresponding to each client
        custom_integers = [6, 5, 65, 5, 65, 32, 32, 112, 321, 254, 23, 515]

        # Ensure the length of custom_integers matches the number of clients
        if len(custom_integers) < len(clients):
            # Extend custom_integers if it's shorter than the clients list
            custom_integers += [0] * (len(clients) - len(custom_integers))

        # Add custom integer to each client and create a new list of data
        client_data_with_int = []
        for index, client in enumerate(clients):
            # Adding custom integer and client data to the new list
            client_data_with_int.append({
                'name': client.name,
                'client_code': client.client_code,
                'num_clients_int': custom_integers[index]  # Custom integer per client
            })

        

        # Create a table instance with the modified clients data
        clientTable = ClientTable(client_data_with_int)

        return render(request, 'clients_page.html', {'form': form, 'contactTable': contactTable, 'clientTableView': clientTable})

def contact_page_view(request):
    form = ContactForm()
    if request.method == 'POST':
        contact_name = request.POST.get('contact_name')
        contact_surname = request.POST.get('contact_surname')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
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
    
    contacts = Contact.objects.filter(client__client_code = 'NON')

    return render(request, 'client_linking.html', {
        'contacts': contacts,
    })



def success_client_link(request,contact_code):
    if request.method == 'POST':
        #selected_client = request.POST.getList('selected_contacts')
        # Logic to link the selected contacts to the client
        # Assuming contact_id is provided
        #contact = get_object_or_404(Contact, id=contact_code)

        # Assuming client_code is the new value provided and exists in the Client model
        #client = get_object_or_404(Client, client_code=selected_client)

        # Update the contact's client reference
        #contact.client = client
        #contact.save()

        return redirect('client_view')
    

    print("Linking contact", contact_code)



    contacts = Contact.objects.filter(client__client_code = 'NON')


    print("Conactsw", contacts)



    return render(request, 'client_linking.html', {
        'contacts': contacts,
    })




def success_contact_unlinked(request, contact_code):

    print("unlinking contact", contact_code)

    # Retrieve the contact by ID
    contact = get_object_or_404(Contact, id=contact_code)

    # Retrieve the client instance using the provided client code
    new_client = get_object_or_404(Client, client_code= 'NON')
    
    # Update the client code
    contact.client = new_client
    contact.save() 



    return redirect('client_view')

