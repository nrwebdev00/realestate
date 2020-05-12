from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
          user_id = request.user.id
          has_sent_contacted_already = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
          if has_sent_contacted_already:
              messages.error(request, 'You have already made an inquiry for this listing')
              return redirect('/listings/'+listing_id)  
        
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        send_mail(
            'Property Listing Inquiry for ' + listing,
            'There has been inquiry for ' + listing + ' please sign in to the admin panel to view.',
            'reproject.email@gmail.com',
            [realtor_email, 'nrwebdev00@gmail.com'],
            fail_silently=False
        )
        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/'+listing_id)
