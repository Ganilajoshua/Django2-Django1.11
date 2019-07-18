# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView,View,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import render,redirect
from .models import Contact
from .forms import ContactForm
class ContactView(TemplateView):
    def get(self, request):
        Contacts = Contact.objects.all()
        return render(request, 'contacts/contact.html', {'Contacts': Contacts})
class NewContactView(View):
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
       		form = form.save(commit=False)
        	form.creator = request.user
       		form.save()
       		Contacts = Contact.objects.all()
       		return redirect('/Contact')
        return render(request, 'contacts/new_contact.html', {'form': form})
    def get(self, request):
        form = ContactForm()
        return render(request, 'contacts/new_contact.html', {'form': form})

class EditContactView(UpdateView):
    model = Contact
    fields = ('FirstName','LastName','Address','ContactNo')
    template_name = 'contacts/edit_contact.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'contact'

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.save()
        return redirect('/Contact')

class DeleteContactView(DetailView):
	model = Contact
	template_name = 'contacts/confirm_delete_contact.html'
	context_object_name = 'delete_contact'
# class DeleteContactView(DeleteView):
#     model = Contact
#     fields = ('FirstName','LastName','Address','ContactNo')
#     template_name = 'contacts/edit_contact.html'
#     pk_url_kwarg = 'pk'
#     context_object_name = 'contact'

#     def form_valid(self, form):
#         contact = form.save(commit=False)
#         contact.delete()
#         return redirect('/Contact')