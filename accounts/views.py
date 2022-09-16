import re
from django.dispatch import receiver
from django.shortcuts import redirect, render
from allauth.account.decorators import verified_email_required, send_email_confirmation
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django import forms
from django.forms import Form, NumberInput
from django.forms.fields import *
from django.forms.widgets import *
from django.urls import reverse
from accounts.models import AvailableBanks, Message, ResponseMessage, UserAccountNumber
from .serializers import AccountCreationSerializer, EmailAddressSerializer
from donate.froms import DonateItemEditImagesForm
from donate.models import DonateItem, DonateItemImage
from farms.forms import ProduceForm
from farms.models import FarmProduce, FarmProdudeOrder
from research.forms import ResearchAddForm
from shop.models import *
from accounts.forms import EditProfileForm, MessageForm, ResponseMessageFormTwo
from django.core.paginator import Paginator
from django.db.models import Q
from research.models import *
from django.core.mail import send_mail
from django.contrib import messages
from rest_framework.generics import *
from templated_email import send_templated_mail
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()


class ItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    title = CharField(max_length=255, label='Item name:', widget=TextInput(
        attrs={
            'class': 'form-control',
            'required': True,
        }
    ))

    price = CharField(label='Item Price:', widget=NumberInput(
        attrs={
            'class': 'form-control',
            'required': True,
        }
    ))

    description = CharField(label='Item description:', widget=Textarea(
        attrs={
            'class': 'form-control',
            'required': True,
        }
    ))

    class Meta:
        model = Item
        fields = ['title', 'price', 'description']


# class TestFrom(ItemForm, Form):
#     category = ChoiceField(choices=((c.slug, c.title) for c in Category.objects.all()), widget=Select(attrs={
#         'class': 'form-control'
#     }))

#     images = FileField(allow_empty_file=False, required=True, widget=FileInput(attrs={
#         'class': 'form-control',
#         'multiple': True,
#         'accept': "image/png, image/jpeg, image/jpg"
#     }))

#     def save(self, *args, **kwargs):
#         print(self.cleaned_data.get('images'))
#         return super().save(*args, **kwargs)


# class ItemEditForm(ItemForm, Form):
#     category = ChoiceField(choices=((c.slug, c.title) for c in Category.objects.all()), widget=Select(attrs={
#         'class': 'form-control'
#     }))

#     images = FileField(widget=FileInput(attrs={
#         'class': 'form-control',
#         'multiple': True,
#         'accept': "image/png, image/jpeg, image/jpg"
#     }))

#     def save(self, *args, **kwargs):
#         print(self.cleaned_data.get('images'))
#         return super().save(*args, **kwargs)


class EmailConfirmView(RetrieveAPIView):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer
    lookup_field = 'email'

# Create your views here.


def make_user_admin(request):
    user = request.user
    user.admin = True
    user.staff = True
    user.save()

    return redirect('/')


def dashboard_view(request):
    user = request.user
    shop_items = Item.objects.complex_filter(Q(seller=user))
    sold_items = OrderItem.objects.complex_filter(
        Q(item__in=shop_items, ordered=True))
    donate_items = DonateItem.objects.complex_filter(Q(donator=user))

    return render(request, 'accounts/html/index.html')


def notification_view(request):
    return render(request, 'accounts/html/pages-account-settings-notifications.html')


@verified_email_required
def profile_view(request):
    user = request.user
    new_email = False
    banks = AvailableBanks.objects.all()
    account_qs = UserAccountNumber.objects.filter(user=user)

    form = EditProfileForm(instance=user)
    if request.POST:
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/')
        else:
            # print(form.)
            return render(request, 'accounts/html/pages-account-settings-account.html', {
                'form': form,
                'banks': banks,
                'account_qs': account_qs
            })

    return render(request, 'accounts/html/pages-account-settings-account.html', {
        'form': form,
        'banks': banks,
        'account_qs': account_qs,
    })

    # return redirect('/accounts/profile/')


class VerifyAccountNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, reqeust, *args, **kwargs):
        account_number = self.request.GET.get('account_number')
        code = self.request.GET.get('bank_code')
        url = f'https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={code}'
        headers = {
            "Authorization": "Bearer sk_test_a689bed51f515c614cd476bd37dd3e0e4efd85e3"}

        res = requests.get(url, headers=headers)
        # print(res.json())

        return Response(data=res.json())


class AccountNumberCreateView(CreateAPIView):
    queryset = UserAccountNumber.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AccountCreationSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def error_404_page(request, exception):
    return render(request, 'pages-misc-error.html')


def error_500_page(request):
    return render(request, 'pages-misc-error.html')


@verified_email_required(login_url='/accounts/login/')
def self_delete_account_view(request):
    if request.POST:
        print(request.POST)
        user = request.user
        user.delete()
        return redirect('/accounts/profile/')


@verified_email_required(login_url='/accounts/login/')
def self_orders_view(request):
    user = request.user
    orders = Order.objects.filter(user=user, ordered=True)
    sales = Sale.objects.complex_filter(Q(buyer=user) & Q(used=True))

    return render(request, 'accounts/self-orders.html', {"orders": orders, 'sales': sales})


@verified_email_required(login_url='/accounts/login/')
def self_store_view(request):
    items = Item.objects.filter(seller=request.user)
    return render(request, 'accounts/self-store.html', {'items': items})


@verified_email_required(login_url='/accounts/login/')
def self_store_add_view(request):
    items = Item.objects.filter(seller=request.user)
    form = ProduceForm()

    print(form.is_multipart())

    if request.POST:
        # form = TestFrom(data=request.POST, files=request.FILES)
        print(form.is_multipart())
        if form.is_valid():
            print(request.FILES)
            print(request.FILES.get('images'))
            print('Valid form')
            item = form.save()
            for image in request.FILES.getlist('images'):
                # print(image)
                ItemImage.objects.create(image=image, item=item)
            item.seller = request.user
            item.category = Category.objects.get(slug=request.POST['category'])
            item.save()
            return redirect('/accounts/e-commerce/store/')
    return render(request, 'accounts/self-store-add.html', {'items': items, 'form': form})


@verified_email_required
def admin_self_store_single_store_item(request, slug):
    item = Item.objects.get(slug=slug)
    threads = [thread for thread in item.saleschat_set.all()
               if thread.messages.count() > 0]
    sales = item.sales.filter(used=True)

    if request.POST:
        if request.POST.get('yes') == 'yes':
            item.delete()
            return redirect('/accounts/e-commerce/store/')

    return render(request, 'accounts/self-store-single-item.html', {
        'item': item,
        'threads': threads,
        'count': len(threads),
        'sales': sales
    })


@verified_email_required
def make_sale(request, slug, username):
    item = Item.objects.get(slug=slug)
    buyer = User.objects.get(username=username)
    sale = Sale.objects.create(buyer=buyer, item=item, price=request.POST.get(
        'price'), quantity=int(request.POST.get('quantity')))

    protocol = 'http://'
    if request.is_secure():
        protocol = 'https://'

    send_templated_mail(
        template_name='sale_notification',
        from_email='contact@sofentng.org',
        recipient_list=[sale.buyer.email],
        context={
            'sender': request.user,
            'receiver': buyer,
            'sale': sale,
            'response_url': protocol + request.get_host() + f'/store/detail/{item.slug}/'
        }
    )

    messages.success(request, 'Sale added succesfully')
    return redirect(f'/accounts/e-commerce/store/{item.slug}/chat/{buyer.username}/')


@verified_email_required
def complete_sale(request, id):
    sale = Sale.objects.get(id=id)
    sale.completed = True
    sale.save()

    send_mail(
        'Notice of order completion',
        f"Order with id: {sale.id} has been completed",
        'contact@sofentng.org',
        ['kibeyefa@gmail.com', 'admin@sofentng.org']
    )

    next = request.GET.get('next')

    if next:
        return redirect(next)

    return redirect('/accounts/e-commerce/orders/')


@verified_email_required
def admin_self_store_single_store_item_chat(request, slug, username):
    receiver = User.objects.get(username=username)
    item = Item.objects.get(slug=slug)
    buyer = User.objects.get(username=username)
    thread = SalesChat.objects.get(seller=request.user, buyer=buyer, item=item)

    if request.POST:
        message = request.POST.get('message')
        chat_message = SalesChatMessage.objects.create(
            message=message, thread=thread, sender=request.user, reciever=receiver)

        protocol = 'https://'
        if not request.is_secure():
            protocol = 'http://'

        send_templated_mail(
            template_name='chat_notification',
            from_email='contact@sofentng.org',
            recipient_list=[request.user.email],
            context={
                'receiver': chat_message.reciever,
                'sender': request.user,
                'message': chat_message.message,
                'response_url': protocol + request.get_host() + f'/store/detail/{item.slug}/'
            }
        )

    return render(request, 'accounts/self-store-item-chat.html', {
        'thread': thread,
        'item': item
    })


# @verified_email_required
# def admin_self_store_single_store_item_chat(request, slug, username):
#   receiver = User.objects.get(username=username)
#   item = Item.objects.get(slug=slug)
#   buyer = User.objects.get(username=username)
#   thread = SalesChat.objects.get(seller=request.user, buyer=buyer, item=item )

#   if request.POST:
#     message = request.POST.get('message')
#     SalesChatMessage.objects.create(message=message, thread=thread, sender=request.user, reciever=receiver)

#   return render(request, 'accounts/self-store-item-chat.html', {
#     'thread': thread,
#     'item': item
#   })


@verified_email_required(login_url='/accounts/login/')
def self_donate_item_add_view(request):
    items = DonateItem.objects.filter(donator=request.user)
    form = DonateItemEditImagesForm()

    print(form.is_multipart())

    if request.POST:
        form = DonateItemEditImagesForm(data=request.POST, files=request.FILES)
        print(form.is_multipart())
        if form.is_valid():
            print(request.FILES)
            print('Valid form')
            item = form.save()
            for image in request.FILES.getlist('images'):
                # print(image)
                DonateItemImage.objects.create(image=image, donate_item=item)
            item.donator = request.user
            item.save()

            return redirect('/accounts/donate/items/')
    return render(request, 'accounts/self-donate-add.html', {'items': items, 'form': form})


@verified_email_required(login_url='/accounts/login/')
def self_donate_view(request):
    form = DonateItemEditImagesForm()
    user = request.user
    items = DonateItem.objects.complex_filter(Q(donator=user))
    paginator = Paginator(items, 4)
    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/self-donate.html', {'obj_list': obj_list, 'form': form})


@verified_email_required(login_url='/accounts/login/')
def self_donate_edit_view(request, pk):
    items = DonateItem.objects.get(id=pk)
    if request.POST:
        form = DonateItemEditImagesForm(
            data=request.POST, files=request.FILES, instance=items)
        if form.is_valid():
            item = form.save()
            for image in request.FILES.getlist('images'):
                DonateItemImage.objects.create(image=image, donate_item=item)
            item.save()
    return redirect('/accounts/donate/items/')


@verified_email_required(login_url='/accounts/login/')
def self_store_edit_view(request, pk):
    items = Item.objects.get(id=pk)
    if request.POST:
        form = ProduceForm(data=request.POST,
                            files=request.FILES, instance=items)
        if form.is_valid():
            item = form.save()
            for image in request.FILES.getlist('images'):
                ItemImage.objects.create(image=image, item=item)
            item.save()
    return redirect('/accounts/e-commerce/store/')


# ADMIN
@verified_email_required(login_url='/accounts/login/')
def admin_order_view(request):
    user = request.user
    paginator = Paginator(Sale.objects.filter(used=True), 4)
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/admin/orders/search/{q}')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-orders.html', {
        'obj_list': obj_list,
    })


@verified_email_required(login_url='/accounts/login/')
def admin_order_search_view(request, q):
    user = request.user
    users = User.objects.filter(username__icontains=q)
    print(users)
    order_qs = Sale.objects.complex_filter(
        Q(id=q) | Q(buyer__in=users) & Q(used=True))
    paginator = Paginator(order_qs, 4)
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/admin/orders/search/{q}')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-orders.html', {
        'obj_list': obj_list,
    })


@verified_email_required(login_url='/accounts/login/')
def admin_items_search_view(request, q):
    user = request.user
    print(q)
    users = User.objects.filter(username__icontains=q)
    print(users)
    order_qs = Item.objects.complex_filter(
        Q(id=q) | Q(title__icontains=q) | Q(seller__in=users))
    paginator = Paginator(order_qs, 4)
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/admin/items/search/{q}')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-items.html', {
        'obj_list': obj_list,
    })


@verified_email_required(login_url='/accounts/login/')
def admin_items_view(request):
    user = request.user
    paginator = Paginator(Item.objects.all(), 4)
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/admin/items/search/{q}')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-items.html', {
        'obj_list': obj_list,
    })


@verified_email_required
def admin_single_store_item(request, slug):
    item = Item.objects.get(slug=slug)
    threads = [thread for thread in item.saleschat_set.all()
               if thread.messages.count() > 0]
    sales = item.sales.filter(used=True)

    if request.POST:
        if request.POST.get('yes') == 'yes':
            item.delete()
            return redirect('/accounts/e-commerce/store/')

    return render(request, 'accounts/admin-single-item.html', {
        'item': item,
        'threads': threads,
        'count': len(threads),
        'sales': sales
    })


@verified_email_required
def admin_item_chat(request, slug, id):
    item = Item.objects.get(slug=slug)
    thread = SalesChat.objects.get(id=id)

    if request.POST:
        message = request.POST.get('message')
        SalesChatMessage.objects.create(
            message=message, thread=thread, sender=request.user, reciever=receiver)

    return render(request, 'accounts/admin-item-chat.html', {
        'thread': thread,
        'item': item
    })


@verified_email_required(login_url='/accounts/login/')
def admin_donate_items_search_view(request, q):
    user = request.user
    print(q)
    users = User.objects.filter(username__icontains=q)
    print(users)
    order_qs = DonateItem.objects.complex_filter(
        Q(description__icontains=q) | Q(title__icontains=q)).distinct()
    paginator = Paginator(order_qs, 4)
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/admin/daonate-items/search/{q}')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-donate-items.html', {
        'obj_list': obj_list,
    })


@verified_email_required(login_url='/accounts/login/')
def admin_donate_items_view(request):
    user = request.user
    paginator = Paginator(DonateItem.objects.all(), 4)
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/admin/donate-items/search/{q}')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-donate-items.html', {
        'obj_list': obj_list,
    })


@verified_email_required(login_url='/accounts/login/')
def admin_research_search_view(request, q):
    user = request.user
    form = ResearchAddForm()
    users = User.objects.filter(username__icontains=q)
    print(users)
    order_qs = ResearchDocument.objects.complex_filter(
        Q(name__icontains=q)).distinct()
    paginator = Paginator(order_qs, 4)
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/admin/reseacrh/search/{q}')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-research.html', {
        'obj_list': obj_list,
        'form': form,
    })


@verified_email_required(login_url='/accounts/login/')
def admin_research_view(request):
    form = ResearchAddForm()
    user = request.user
    paginator = Paginator(ResearchDocument.objects.all(), 4)
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/admin/research/search/{q}')

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-research.html', {
        'obj_list': obj_list,
        'form': form,
    })


@verified_email_required(login_url='/accounts/login/')
def add_document_view(request):
    if request.POST:
        form = ResearchAddForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

    return redirect(reverse('accounts:admin-research'))


@verified_email_required(login_url='/accounts/login/')
def delete_document_view(request, pk):
    ResearchDocument.objects.get(id=pk).delete()
    return redirect(reverse('accounts:admin-research'))


@verified_email_required(login_url='/accounts/login/')
def farm_items_view(request):
    user = request.user
    if not user.is_admin:
        return redirect('/accounts/profile/')

    items = FarmProduce.objects.all()
    form = ProduceForm()

    if request.POST:
        form = ProduceForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'accounts/admin-farm-items.html', {
        'items': items,
        'form': form
    })


@verified_email_required(login_url='/accounts/login/')
def farm_orders_view(request):
    user = request.user
    if not user.is_admin:
        return redirect('/accounts/profile/')

    qs = FarmProdudeOrder.objects.all()
    paginator = Paginator(qs, 4)

    page = request.GET.get('page')
    obj_list = paginator.get_page(page)
    # form = ProduceForm()

    if request.POST:
        q = request.POST.get('q')
        return redirect('accounts:farm-order-search', q=q)

    return render(request, 'accounts/admin-farm-orders.html', {
        'obj_list': obj_list,
        'items': qs,
        # 'form': form
    })


@verified_email_required(login_url='/accounts/login/')
def farm_orders_search_view(request, q):
    user = request.user
    if not user.is_admin:
        return redirect('/accounts/profile/')

    paginator = Paginator(FarmProdudeOrder.objects.complex_filter(
        Q(id=q) | Q(first_name__icontains=q) | Q(email=q)), 4)
    page = request.GET.get('page')
    obj_list = paginator.get_page(page)
    # form = ProduceForm()

    if request.POST:
        q = request.POST.get('q')
        return redirect('accounts:farm-order-search', q=q)

    return render(request, 'accounts/admin-farm-orders.html', {
        'obj_list': obj_list,
        # 'form': form
    })


@verified_email_required(login_url='/accounts/login/')
def farm_items_delete_view(request, pk):
    user = request.user
    if not user.is_admin:
        return redirect('/accounts/profile/')

    item = FarmProduce.objects.get(id=pk)
    item.delete()

    return redirect(reverse('accounts:admin-farm-items'))


@verified_email_required(login_url='/accounts/login/')
def farm_items_edit_view(request, pk):
    user = request.user
    if not user.is_admin:
        return redirect('/accounts/profile/')

    item = FarmProduce.objects.get(id=pk)
    item.available = not item.available
    item.save()

    return redirect(reverse('accounts:admin-farm-items'))


@verified_email_required(login_url='/accounts/login/')
def admin_user_view(request):
    user = request.user
    if not user.is_admin:
        return redirect('/accounts/profile/')

    user_qs = User.objects.all()
    paginator = Paginator(user_qs, 4)
    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-users.html', {
        'obj_list': obj_list
    })


@verified_email_required(login_url='/accounts/login/')
def admin_messages_view(request):
    user = request.user
    if not user.is_admin:
        return redirect('/accounts/profile/')

    form = ResponseMessageFormTwo()
    paginator = Paginator(Message.objects.all(), 4)
    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    if request.POST:
        q = request.POST.get('q')
        user_ = User.objects.filter(username=q)[0]
        qs = Message.objects.complex_filter(
            Q(sender=user_) | Q(subject__icontains=q))
        paginator = Paginator(qs, 4)
        page = request.GET.get('page')
        obj_list = paginator.get_page(page)

    return render(request, 'accounts/admin-messages.html', {'obj_list': obj_list, 'form': form, 'page': True})


@verified_email_required(login_url='/accounts/login/')
def admin_messages_respond_view(request):
    user = request.user
    if not user.is_admin:
        return redirect('/accounts/profile/')

    if request.POST:
        form = ResponseMessageFormTwo(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.receiver = User.objects.get(
                username=request.POST.get('receiver'))
            x.save()

            try:
                # send_mail(message.subject, message.message, 'contact@sofentng.org', [message.sender.email])
                if request.is_secure():
                    protocol = 'https://'
                else:
                    protocol = 'http://'

                from templated_email import send_templated_mail
                send_templated_mail(
                    template_name='contact_message',
                    from_email='contact@sofentng.org',
                    recipient_list=[x.receiver.email],
                    context={
                        'subject': x.subject,
                        'name': 'admin@sofent',
                        'message': x.message,
                        'url': protocol + request.get_host()
                    },
                    # Optional:
                    # cc=['cc@example.com'],
                    # bcc=['bcc@example.com'],
                    # headers={'My-Custom-Header':'Custom Value'},
                    # template_prefix="my_emails/",
                    # template_suffix="email",
                )
                messages.success(request, 'Message sent succesfully.')
            except:
                messages.error(
                    request, 'Something went wrong, couldn\'t send reply.')
                x.delete()

            return redirect('/accounts/admin/messages/')

    return redirect('/accounts/admin/messages/')


@verified_email_required(login_url='/accounts/login/')
def contact(request):
    form = MessageForm()

    if request.POST:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            message.sender = request.user
            message.save()

            try:
                # send_mail(message.subject, message.message, 'contact@sofentng.org', [message.sender.email])
                if request.is_secure():
                    protocol = 'https://'
                else:
                    protocol = 'http://'

                from templated_email import send_templated_mail
                send_templated_mail(
                    template_name='contact_message',
                    from_email=message.sender.email,
                    recipient_list=['contact@sofentng.org',
                                    'admin@sofentng.org'],
                    context={
                        'subject': message.subject,
                        'name': message.sender.username,
                        'message': message.message,
                        'url': protocol + request.get_host()
                    },
                    # Optional:
                    # cc=['cc@example.com'],
                    # bcc=['bcc@example.com'],
                    # headers={'My-Custom-Header':'Custom Value'},
                    # template_prefix="my_emails/",
                    # template_suffix="email",
                )
                messages.success(request, 'Message sent succesfully.')
                form = MessageForm()
                return render(request, 'accounts/contact.html', {'form': form})
            except:
                messages.error(
                    request, 'Something went wrong, couldn\'t send mesage')
                message.delete()

    return render(request, 'accounts/contact.html', {'form': form})


@verified_email_required(login_url='/accounts/login/')
def account_notifications_view(request):
    response_messages = ResponseMessage.objects.complex_filter(
        Q(receiver=request.user))

    # form = ResponseMessageFormTwo()
    paginator = Paginator(response_messages, 4)
    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/notifications/search/{q}/')

    return render(request, 'accounts/admin-messages.html', {'obj_list': obj_list, 'form': None})


@verified_email_required(login_url='/accounts/login/')
def account_notifications_search_view(request, q):
    response_messages = ResponseMessage.objects.complex_filter(
        Q(receiver=request.user) & Q(subject__icontains=q))

    # form = ResponseMessageFormTwo()
    paginator = Paginator(response_messages, 4)
    page = request.GET.get('page')
    obj_list = paginator.get_page(page)

    if request.POST:
        q = request.POST.get('q')
        return redirect(f'/accounts/notifications/search/{q}/')

    return render(request, 'accounts/admin-messages.html', {'obj_list': obj_list, 'form': None})


# Helpers
