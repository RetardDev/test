
from typing import Any
from django.conf import settings
from django.http. response import JsonResponse, HttpResponse
from django.http import  HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from store.models.userprofile import UserProfile
from store.models.provider import Provider
from store.models.service import Services
from store.models.order import Order, Notification
from django.urls import reverse
import time
import stripe
import json


def SuccessView(request):
    session_id = request.GET.get('session_id')
    if session_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try: 
            session = stripe.checkout.Session.retrieve(session_id)
            metadata = session['metadata']
            address = metadata.get('address')
            phone = metadata.get('phone')
            user_id = metadata.get('user_id')
            one_item = metadata.get('one-item')
            print(f'Metadata of success\nAddress: {address}\nPhone: {phone}\nUserId: {user_id}\n One Item: {one_item}')


            if one_item == 'false':
                cart = request.session.get('cart')
                # service_ids = list(cart.keys())
                services = Services.get_services_by_id(list(cart.keys()))

                for service in services:
                    order = Order(user=UserProfile.objects.get(user_id=user_id),
                                    service=service,
                                    price=service.price,
                                    phone=phone,
                                    address=address,
                                    quantity=cart.get(str(service.id)))
                    order.save()

                    providers = service.providers.all()
                    for provider in providers:
                        if service in provider.services_offered.all():
                            notification = Notification(
                                order=order,
                                provider=provider.user_profile,
                                message=f"New order placed for {service.name}. Order ID: {order.id}"
                            )
                            notification.save()

                request.session['cart'] = {}
            elif one_item == 'true':
                service_id = metadata.get('service_id')
                service = Services.objects.get(pk=service_id)
                print(service)
                print(service_id)
                order = Order(user=UserProfile.objects.get(user_id=user_id),
                                    service=service,
                                    price=service.price,
                                    phone=phone,
                                    address=address,
                                    quantity=1)
                order.save()
                providers = service.providers.all()
                for provider in providers:
                    if service in provider.services_offered.all():
                        notification = Notification(
                            order=order,
                            provider=provider.user_profile,
                             message=f"New order placed for {service.name}. Order ID: {order.id}"
                        )
                        notification.save()

            return HttpResponseRedirect('/orders')
        except stripe.error.InvalidRequestError as e:
            pass

    return HttpResponseRedirect('/error/')

class CancelledView(TemplateView):
    template_name = 'cancelled.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['redirect_delay'] = 5000;
        return context;

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey' : settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            post_data = request.body
            data  = json.loads(post_data)
            address = data.get('address')
            phone = data.get('phone')
            user_id = request.session.get('user')
            selected_service_stripe_id = data.get('selectedServiceStripeId')

            selected_service = Services.objects.get(stripe_id=selected_service_stripe_id)
            print(f'user id: {user_id} address {address} phone: {phone}')
            metadata = {
                'one-item': 'true',
                'service_id': selected_service.id,
                'user_id': user_id,
                'address': address,
                'phone': phone,
            }

            print(selected_service)
            checkout_session = stripe.checkout.Session.create(
                client_reference_id = request.user.id if request.user.is_authenticated else None,
                success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = domain_url + 'cancelled/',
                payment_method_types = ['card'],
                mode='payment',
                line_items=[
                     {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': selected_service.stripe_id,
                    'quantity': 1,
                },                  
                ],
                metadata=metadata,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
@csrf_exempt
def create_checkout_session_M(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            post_data = request.body
            data = json.loads(post_data)
            address = data.get('address')
            phone = data.get('phone')

            user_id = request.session.get('user')
            ids = list(request.session.get('cart').keys())
            services = Services.get_services_by_id(ids)

            metadata = {
                'one-item': 'false',
                'user_id': user_id,
                'address': address,
                'phone': phone,
            }

            print(f'user id: {user_id} address {address} phone: {phone}')
            line_items = []
            for service_id, quantity in request.session.get('cart', {}).items():
                service  = Services.objects.get(id=int(service_id))
                line_items.append({
                    'price': service.stripe_id,
                    'quantity': quantity,
                })

            checkout_session = stripe.checkout.Session.create(
                client_reference_id = request.user.id if request.user.is_authenticated else None,
                success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = domain_url + 'cancelled/',
                payment_method_types = ['card'],
                mode='payment',
                line_items= line_items,
                metadata=metadata,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("success atakilti")
        # session = event['data']['object']
        # metadata = session['metadata']

        # user_id = metadata.get('user_id')
        # address = metadata.get('address')
        # phone = metadata.get('phone')
        # print(f'222222user id: {user_id} address {address} phone: {phone}')

        # try:
        #     cart = request.session.get('cart')
        #     service_ids = list(cart.keys())
        #     services = Services.get_service_by_id(list(cart.keys()))

        #     for service in services:
        #         order = Order(user=UserProfile.objects.get(user_id=user_id),
        #                         service=service,
        #                         price=service.price,
        #                         phone=phone,
        #                         address=address,
        #                         quantity=cart.get(str(service.id)))
        #         order.save()

        #         providers = service.providers.all()
        #         for provider in providers:
        #             if service in provider.services_offered.all():
        #                 notification = Notification(
        #                     order=order,
        #                     provider=provider.user_profile,
        #                     message=f"New order placed for {service.name}. Order ID: {order.id}"
        #                 )
        #                 notification.save()

        #     request.session['cart'] = {}  # Clear the cart after order creation

        #     return HttpResponse(status=200)
        # except Exception as e:
        #     # Log or handle the exception appropriately
        #     return HttpResponse(status=500)

    return HttpResponse(status=200)