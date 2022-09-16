from multiprocessing import context
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from .models import ResearchDocument
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def research_view(request):
  template_name = 'research/index.html'
  paginator = Paginator(ResearchDocument.objects.all(), 1)
  if request.POST:
    q = request.POST.get('q')
    return redirect(f'/research/search/{q}')
  page = request.GET.get('page')
  obj_list = paginator.get_page(page)
  return render(request, template_name, {'research': True, 'obj_list': obj_list})

# def get_context_data(request):
#   query_set = get_query_set(request)
#   if request.GET:
#     page = request.GET.get('page')

# def get_query_set(request):
#   query_set = ResearchDocument.objects.all()
#   if request.GET.get('q'):
#     q = request.GET.get('q')
#     query_set = query_set.filter(name__icontains=q)
#   return query_set

def search_docs(request, q):
  template_name = 'research/index.html'
  paginator = Paginator(ResearchDocument.objects.filter(name__icontains=q), 1)
  if request.POST:
    q = request.POST.get('q')
    return redirect(f'/research/search/{q}')
  page = request.GET.get('page')
  obj_list = paginator.get_page(page)
  return render(request, template_name, {'research': True, 'obj_list': obj_list})