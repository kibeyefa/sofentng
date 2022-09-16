from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from donate.models import DonateItem
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages
from shop.forms import CheckOutForm, ShopItemReviewForm
from .serializers import SaleSerializer, ShopItemreviewSerializer
from .models import *
from allauth.account.decorators import verified_email_required
from allauth.account.models import EmailAddress
from random import choices, sample
from allauth.account.views import PasswordResetView
from rest_framework.generics import ListAPIView, CreateAPIView
from django.core.mail import send_mass_mail, send_mail
from templated_email import send_templated_mail


# Create your views here.


def shop_view(request):
    template_name = 'store/shop.html'
    paginator = Paginator(Item.objects.all(), 3)
    categories = Category.objects.all()
    cart, created = None, False
    cats = sample(range(1, categories.count() + 1), 2)
    print(cats)
    list1 = Category.objects.get(id=cats[0]).items.all() if Category.objects.get(
        id=cats[0]).items.all().count() < 11 else Category.objects.get(id=cats[0]).items.all()[:10]
    list2 = Category.objects.get(id=cats[1]).items.all() if Category.objects.get(
        id=cats[1]).items.all().count() < 11 else Category.objects.get(id=cats[1]).items.all()[:10]

    if request.user.is_authenticated:
        cart, created = Order.objects.get_or_create(
            user=request.user, ordered=False)

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/store/search/{q}/')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, template_name, {
        'store': True,
        'user': request.user,
        'obj_list': obj_list,
        'categories': categories,
        'cart': cart,
        'list1_name': Category.objects.get(id=cats[0]),
        'list2_name': Category.objects.get(id=cats[1]),
        'list1': list1,
        'list2': list2,
    })


def product_search_view(request, q):
    template_name = 'store/shop.html'
    paginator = Paginator(Item.objects.complex_filter(Q(title__contains=q) | Q(
        category__in=Category.objects.filter(title__icontains=q))), 4)
    categories = Category.objects.all()
    cart, created = None, False
    cats = sample(range(1, categories.count() + 1), 2)
    print(cats)
    list1 = Category.objects.get(id=cats[0]).items.all() if Category.objects.get(
        id=cats[0]).items.all().count() < 11 else Category.objects.get(id=cats[0]).items.all()[:10]
    list2 = Category.objects.get(id=cats[1]).items.all() if Category.objects.get(
        id=cats[1]).items.all().count() < 11 else Category.objects.get(id=cats[1]).items.all()[:10]

    if request.user.is_authenticated:
        cart, created = Order.objects.get_or_create(
            user=request.user, ordered=False)

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/store/search/{q}/')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, template_name, {
        'store': True,
        'user': request.user,
        'obj_list': obj_list,
        'categories': categories,
        'cart': cart,
        'list1_name': Category.objects.get(id=cats[0]),
        'list2_name': Category.objects.get(id=cats[1]),
        'list1': list1,
        'list2': list2,
    })


def product_category_page(request, slug):
    template_name = 'store/shop.html'
    category = Category.objects.get(slug=slug)
    categories = Category.objects.all()
    cats = sample(range(1, categories.count() + 1), 2)
    cart, created = None, False
    list1 = Category.objects.get(id=cats[0]).items.all() if Category.objects.get(
        id=cats[0]).items.all().count() < 11 else Category.objects.get(id=cats[0]).items.all()[:10]
    list2 = Category.objects.get(id=cats[1]).items.all() if Category.objects.get(
        id=cats[1]).items.all().count() < 11 else Category.objects.get(id=cats[1]).items.all()[:10]
    item_qs = Item.objects.complex_filter(Q(category=category))
    paginator = Paginator(item_qs, 3)

    # x = Item.objects.
    if request.user.is_authenticated:
        cart, created = Order.objects.get_or_create(
            user=request.user, ordered=False)

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/store/search/{q}/')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, template_name, {
        'store': True,
        'user': request.user,
        'obj_list': obj_list,
        'categories': categories,
        'cart': cart,
        'list1_name': Category.objects.get(id=cats[0]),
        'list2_name': Category.objects.get(id=cats[1]),
        'list1': list1,
        'list2': list2,
    })


# @verified_email_required
# def cart_view(request):
#     cart, created = Order.objects.get_or_create(
#         user=request.user, ordered=False)
#     categories = Category.objects.all()

#     return render(request, 'store/cart.html', {
#         'store': True,
#         'cart': cart,
#         'categories': categories
#     })


def product_detail_page(request, slug):
    item = Item.objects.get(slug=slug)
    category = item.category
    categories = Category.objects.all()
    user = request.user
    chat, chat_created = None, None
    sales = None
    others = category.items.all().exclude(slug=slug)
    if others.count() > 10:
        others = category.items.all().exclude(slug=slug)[:10]

    if request.user.is_authenticated:
        sales = Sale.objects.complex_filter(Q(buyer=user) & Q(
            payment_confirmed=False) & Q(used=False) & Q(item=item))
        chat, chat_created = SalesChat.objects.get_or_create(
            item=item, buyer=user) if user.is_authenticated else (None, None)

    if request.method == 'POST':
        if user.is_authenticated:
            m = request.POST.get('message')
            message = SalesChatMessage.objects.create(
                message=m, sender=user, reciever=item.seller, thread=chat)
            chat.save()

            protocol = 'https://'
            if not request.is_secure():
                protocol = 'http://'

            send_templated_mail(
                template_name='chat_notification',
                from_email='contact@sofentng.org',
                recipient_list=[item.seller.email],
                context={
                    'receiver': message.reciever,
                    'sender': request.user,
                    'message': message.message,
                    'response_url': protocol + request.get_host() + f'/accounts/e-commerce/store/{item.slug}/chat/{message.reciever.username}/'
                }
            )

        return redirect(f'/store/detail/{slug}/')

    return render(request, 'store/detail.html', {
        'sales': sales,
        'chat': chat,
        'store': True,
        'list': others,
        'item': item,
        'categories': categories,
    })


@verified_email_required
def comfirm_purchase(request, id):
    sale = Sale.objects.get(id=id)
    seller = sale.item.seller
    buyer = sale.buyer
    sale.used = True
    sale.save()

    if request.GET.get('next'):
        next = request.GET.get('next')

    from paystackapi.transaction import Transaction
    from paystackapi.paystack import Paystack
    paystack = Paystack(
        secret_key='sk_test_a689bed51f515c614cd476bd37dd3e0e4efd85e3')
    response = paystack.transaction.verify(sale.id)
    # transaction = Transaction(authorization_key="sk_test_a689bed51f515c614cd476bd37dd3e0e4efd85e3")
    # response  = transaction.verify(order.id)
    if response["message"] == 'Verification successful' and response['data']['status'] == 'success':
        sale.payment_confirmed = True
        sale.save()

        protocol = 'https://'
        if not request.is_secure():
            protocol = 'http://'

        # To Seller
        send_templated_mail(
            template_name='purchase_notification',
            from_email='contact@sofentng.org',
            recipient_list=[seller.email],
            context={
                'intended_receiver': 'seller',
                'response_url': protocol + request.get_host() + f'/accounts/e-commerce/store/{sale.item.slug}/',
                'receiver': seller,
                'sale': sale,
                'sender': buyer,
            }
        )

        # To buyer
        send_templated_mail(
            template_name='buyer_purchase_notification',
            from_email='contact@sofentng.org',
            recipient_list=[buyer.email],
            context={
                'intended_receiver': 'buyer',
                'response_url': protocol + request.get_host() + f'/accounts/e-commerce/orders/',
                'receiver': buyer,
                'sale': sale,
            }
        )

        # To admins
        send_templated_mail(
            template_name='admin_purchase_notification',
            from_email='contact@sofentng.org',
            recipient_list=['contact@sofentng.org', 'admin@sofentng.org'],
            context={
                'intended_receiver': 'buyer',
                'response_url': protocol + request.get_host() + f'/accounts/admin/items/{sale.item.slug}/',
                'sale': sale,
            }
        )
        if next:
            return redirect(next)

        return HttpResponse('Something went wrong')
    else:
        return HttpResponse('Something went wrong')


@verified_email_required
def product_review_add_view(request, slug):
    item = Item.objects.get(slug=slug)

    if request.method == 'POST':
        form = ShopItemReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.sender = request.user
            review.save()

    return redirect(f'/store/detail/{slug}/')


@verified_email_required(login_url='/accounts/login/')
def add_to_cart(request, slug):
    print(request.GET.get('next'))
    item = Item.objects.get(slug=slug)
    order, order_created = Order.objects.get_or_create(
        user=request.user, ordered=False)
    order_item, item_created = OrderItem.objects.get_or_create(
        user=request.user, ordered=False, item=item)

    if order.items.filter(item__slug=item.slug).exists():
        order_item.quantity += 1
        order_item.save()
    else:
        order.items.add(order_item)

    order.save()

    if request.GET.get('next'):
        next_url = request.GET.get('next')
        return redirect(f'/store/{next_url}')

    return redirect(f'/store/detail/{slug}')


# @verified_email_required(login_url='/accounts/login/')
# def remove_from_cart(request, slug):
#     item = Item.objects.get(slug=slug)
#     try:
#         order_item = OrderItem.objects.get(
#             user=request.user, ordered=False, item=item)
#         order = Order.objects.get(user=request.user, ordered=False)
#         if order.items.filter(item__slug=item.slug).exists():
#             order.items.remove(order_item)
#             order_item.delete()

#         order.save()
#     except:
#         pass

#     if request.GET.get('next'):
#         next_url = request.GET.get('next')
#         return redirect(f'/store/{next_url}/')

#     return redirect(f'/store/detail/{slug}/')


# @verified_email_required(login_url='/accounts/login/')
# def reduce_item_number_in_cart(request, slug):
#     item = Item.objects.get(slug=slug)
#     order_item = OrderItem.objects.get(
#         user=request.user, ordered=False, item=item)
#     order = Order.objects.get(user=request.user, ordered=False)
#     if order.items.filter(item__slug=item.slug).exists():
#         if order_item.quantity > 1:
#             order_item.quantity -= 1
#             order_item.save()
#         else:
#             order.items.remove(order_item)
#             order_item.delete()
#     order.save()

#     if request.GET.get('next'):
#         next_url = request.GET.get('next')
#         return redirect(f'/store/{next_url}/')

#     return redirect(f'/store/detail/{slug}/')


# @verified_email_required(login_url='/accounts/login/')
# def check_out_view(request):
#     user = request.user
#     form = CheckOutForm()
#     b = False
#     order = Order.objects.get(user=request.user, ordered=False)
#     categories = Category.objects.all()

#     if order.items.all().count() < 1:
#         return redirect('/store/cart/')

#     try:
#         x = BillingAddress.objects.get(user=user, order=order)
#         if x:
#             b = True
#     except Exception as e:
#         pass

#     if request.POST:
#         # print(request.POST)
#         form = CheckOutForm(request.POST)

#         if form.is_valid():
#             print(form.cleaned_data)
#             if b:
#                 x.delete()
#             first_name, last_name, email, phone, address, update_profile, payment_options = form.cleaned_data.values()
#             billing_address = BillingAddress.objects.create(first_name=first_name,
#                                                             last_name=last_name, email=email, phone=phone, address=address, payment_method=payment_options, user=user, order=order)
#             if update_profile:
#                 user.firstname = first_name
#                 user.last_name = last_name
#                 user.phone = phone
#                 user.address = address
#                 user.save()
#             return redirect('/store/confirm-payment/')
#         else:
#             return render(request, 'store/index.html', {
#                 'store': True,
#                 'form': form,
#                 'cart': order,
#                 'categories': categories
#             })
#     return render(request, 'store/index.html', {
#         'store': True,
#         'form': form,
#         'cart': order,
#         'categories': categories
#     })


# @verified_email_required(login_url='/accounts/login/')
# def confirm_payment_view(request):
#     user = request.user
#     order = Order.objects.get(user=request.user, ordered=False)

#     if order.items.all().count() < 1:
#         return redirect('/store/cart/')

#     categories = Category.objects.all()

#     if request.POST:
#         print(request.POST)
#         if request.POST.get('cancel'):
#             for item in order.items.all():
#                 item.delete()
#             order.delete()

#         if request.POST.get('confirm'):

#             if order.billingaddress.payment_method == 'd':
#                 order.ordered = True
#                 for item in order.items.all():
#                     item.ordered = True
#                     item.save()
#                 order.save()

#             if order.billingaddress.payment_method == 'c':
#                 from paystackapi.transaction import Transaction
#                 from paystackapi.paystack import Paystack
#                 paystack = Paystack(
#                     secret_key='sk_test_a689bed51f515c614cd476bd37dd3e0e4efd85e3')

#                 response = paystack.transaction.verify(order.id)
#                 # transaction = Transaction(authorization_key="sk_test_a689bed51f515c614cd476bd37dd3e0e4efd85e3")
#                 # response  = transaction.verify(order.id)
#                 if response["message"] == 'Verification successful' and response['data']['status'] == 'success':
#                     order.ordered = True
#                     for item in order.items.all():
#                         item.ordered = True
#                         item.save()
#                     order.save()

#                 else:
#                     return HttpResponse('Something went wrong')

#         messages.success(request, 'Order placed succesfully')
#         return redirect('/store/')

#     return render(request, 'store/confirm-payment.html', {
#         'store': True,
#         'cart': order,
#         'categories': categories
#     })


@verified_email_required(login_url='/accounts/login/')
def delete_all_item_images(request, pk):
    item = Item.objects.filter(id=pk)
    if item.exists():
        f_img = item[0].images.all()[0]
        item[0].images.all().exclude(id=f_img.id).delete()

    return redirect('/accounts/e-commerce/store/')


@verified_email_required(login_url='/accounts/login/')
def delete_single_item_image(request, pk):
    image = ItemImage.objects.get(id=pk)
    item = image.item

    if item.images.all().count() > 1:
        image.delete()

    return redirect('/accounts/e-commerce/store/')


# @verified_email_required(login_url='/accounts/login/')
# def mark_order_as_completed(request, pk):

#     item = Order.objects.get(id=pk)
#     item.completed = True
#     item.save()

#     return redirect('/accounts/admin/orders/')


@verified_email_required
def delete_sale(request, id):
    sale = Sale.objects.get(id=id)
    sale.delete()

    next = request.GET.get('next')
    return redirect(next)


class ShopItemReviewApiView(ListAPIView):
    serializer_class = ShopItemreviewSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.request.path.split('/')
        slug = slug[3]
        return ShopItemReview.objects.complex_filter(Q(item=Item.objects.get(slug=slug)))


class SaleCreateApiView(CreateAPIView):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
