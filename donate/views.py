from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from donate.models import DonateItem, DonateItemImage
from allauth.account.decorators import verified_email_required
from shop.models import *


# Create your views here.
def donate_home_view(request):
  template_name = 'donate/index.html'
  paginator = Paginator(DonateItem.objects.all(), 1)
  if request.POST:
    q = request.POST.get('q')
    return redirect(f'/donate/search/{q}')
  page = request.GET.get('page')
  obj_list = paginator.get_page(page)

  return render(request, template_name, {'donate': True, 
   'user': request.user,
   'obj_list': obj_list,
   'list2': [i for i in range(1, 7)]
  })


def donate_search_view(request, q):
  template_name = 'donate/index.html'
  paginator = Paginator(DonateItem.objects.filter(title__icontains=q), 1)
  if request.POST:
    q = request.POST.get('q')
    return redirect(f'/donate/search/{q}')
  page = request.GET.get('page')
  obj_list = paginator.get_page(page)

  return  render(request, template_name, {
    'donate': True,
    'user': request.user,
    'obj_list': obj_list
  })


def donate_detail_view(request, pk):
  item = DonateItem.objects.get(id=pk)
  template_name = 'donate/detail.html'

  return render(request, template_name, {
    'donate': True, 
    'item': item, 
    'list': Item.objects.all()[0:10]
    }
  )


@verified_email_required(login_url='/accounts/login/')
def delete_all_item_images(request, pk):
  item = DonateItem.objects.filter(id=pk)
  if item.exists():
    f_img = item[0].images.all()[0]
    item[0].images.all().exclude(id = f_img.id).delete()

  return redirect('/accounts/donate/items/')


@verified_email_required(login_url='/accounts/login/')
def delete_single_item_image(request, pk):
  image = DonateItemImage.objects.get(id=pk)
  item = image.donate_item

  if item.images.all().count() > 1:
    image.delete()

  return redirect('/accounts/donate/items/')
