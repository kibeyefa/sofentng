from django.http import HttpResponse
from django.shortcuts import redirect, render

from farms.serializers import FarmProduceOrderSerialzer
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from allauth.account.decorators import verified_email_required
from paystackapi.transaction import Transaction
from paystackapi.paystack import Paystack
from django.core.mail import send_mail, mail_admins


# Create your views here.

def farm_home_vew(request):
    template_name = 'farms/index.html'
    farm_produce = FarmProduce.objects.all()

    if request.method == 'POST':
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        produce = request.POST.get('produce')
        unit = request.POST.get('unit')
        farm_produce = FarmProduce.objects.get(name=produce)

        order = FarmProdudeOrder.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_no=phone,
            address=address,
            produce=farm_produce,
            unit=int(unit)
        )

        return redirect(f'/farms/{order.id}')
    return render(request, template_name, {'farms': True, 'farm_produces': farm_produce})


@api_view(['POST'])
def farm_payment_view(request, refID):
    order = FarmProdudeOrder.objects.get(id=refID)
    return Response(data={'APi works'})
    # return redirect(f'/farms/{refID}/')


class FarmPaymentView(CreateAPIView):
    queryset = FarmProdudeOrder.objects.all()
    serializer_class = FarmProduceOrderSerialzer


@api_view(['GET'])
def farm_payment_confirm(request, refID):
    paystack = Paystack(
        secret_key='sk_test_a689bed51f515c614cd476bd37dd3e0e4efd85e3')

    response = paystack.transaction.verify(refID)
    order = FarmProdudeOrder.objects.get(id=refID)
    print(response['message'])
    if response["message"] == 'Verification successful' and response['data']['status'] == 'success':
        order.completed = True
        order.save()

        from django.core.mail import send_mail

        # To buyer
        send_mail(
            subject=f'Notification of order with ref {order.id}',
            message=f"""
Your order has been placed, and payment received. We will reach out to you with the progress on your order.
Your SOFENT farms order reference is {order.id}


For any complaint, reach out to us on contact@sofentng.ng and admin@sofentng.org.
            """,
            from_email='contact@sofentng.org',
            recipient_list=[order.email]
        )

        # To admin
        send_mail(
            subject=f'Notification of order with ref {order.id}',
            message=f"""
An order has been placed on SOFENT farms, and payment received.
The order reference is {order.id}


Reach out to the buyer at {order.email}.
            """,
            from_email='contact@sofentng.org',
            recipient_list=['contact@sofentng.org', 'admin@sofentng.org']
        )
        return Response(data={'message': 'Order placed sucessfully.'})

    return Response(data={'message': 'Order placement unsuccesful.'})
