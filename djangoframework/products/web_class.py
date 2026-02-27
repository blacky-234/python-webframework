from django.views import View
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView,TemplateView,FormView,RedirectView,View
from django.urls import reverse_lazy
from .models import Category,Product,Order

class ListCategoryView(ListView):
    model = Category
    template_name = "category/list.html"
    context_object_name = "page_obj"
    paginate_by = 5

    def get_paginate_by(self, queryset):
        a = super().get_paginate_by(queryset)
        print("paginate_by: ",a)
        return a