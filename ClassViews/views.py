# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView,View,UpdateView,DeleteView,DetailView
# from django.views.generic.detail import 
from django.shortcuts import render,redirect,get_object_or_404
from .models import Contact
from .forms import ContactForm
from django.urls import reverse_lazy
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

# class DeleteContactView(DetailView):
# 	template_name = 'contacts/confirm_delete_contact.html'
# 	def get_object(self):
# 		pk = self.kwargs.get("pk")
# 		return get_object_or_404(Contact,pk=pk)

# class ContactDelete(DeleteView):
#     model = Contact
#     template_name = 'templates/contacts/confirm_delete_contact.html'
#     success_url = reverse_lazy('list_contact')

class ContactDelete(View):
	template_name = "contacts/contact_confirm_delete.html"
	def get_object(self):
		id = self.kwargs.get('pk')
		obj =  None
		if id is not None:
			obj = get_object_or_404(Contact, id=id)
		return obj
	def get(self, request, id=None, *args, **kwargs):
		context = {}
		obj = self.get_object()
		if obj is not None:
			context['object'] = obj
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = {}
		obj = self.get_object()
		if obj is not None:
			obj.delete()
			context['object'] = None
			print('Here')
			return redirect('/Contact')
		print('dito')
		return render(request, self.template_name, context)