from django.shortcuts import render , redirect , HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from store.models.service import Services, ServiceImages
from store.models.category import Category
from store.models.review import Reviews 
from django.views import View
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages

class ServiceView(View):
    def get(self, request):
      parent_categories = Category.get_parent_categories()
      services = Services.get_all_services()
      return render(request, 'service.html', {'parent_categories': parent_categories, 'services' : services})

def servicesCategory(request, foo):
      try:
            foo = foo.replace('%20', ' ')
            parent_categories = Category.get_parent_categories()
            category = Category.objects.get(name=foo)     
            print(f"category {category}") 
            print(f'foo {foo}')
            services = []
            if category in parent_categories:
                  print("we in ")
                  categories = Category.objects.filter(parent_category=category)
                  print(f"the subcategories {categories}")
                  for sub_category in categories:
                        sub_category = Category.objects.get(name=sub_category)
                        print(f'sub_category confirmed {sub_category}\n')
                        services.extend(Services.objects.filter(category=sub_category))
                  print(services)
            else:       
                  services = Services.get_all_services_by_categoryid(category)
                  print(services)
            return render(request, 'service.html', {'parent_categories' : parent_categories, 'services' : services})
      except:
            messages.success(request, ("not "))
            return redirect('service')
      #   if category_id:
      #         services = Services.get_all_services_by_category_id(category_id)
      #   else:
      #         services = Services.get_all_services()

      # return render(request, 'service.html', {'services': services, 'categories': categories})
def serviceSingle(request, id):
      service = Services.get_service_by_id(id)
      service_image = ServiceImages.objects.filter(service=service)
      return render(request, 'serviceSingle.html', {'service' : service, 'service_image': service_image})