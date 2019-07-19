# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
import io
from django.views.generic import View, UpdateView, CreateView
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Contact
from .forms import ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.http import JsonResponse
decorators = login_required


@method_decorator(decorators, name='dispatch')
class ContactView(View):
    def get(self, request):
        Contacts = Contact.objects.filter(creator=request.user)
        return render(request, 'contacts/contact.html', {'Contacts': Contacts})


@method_decorator(decorators, name='dispatch')
class NewContactView(View):
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.creator = request.user
            form.save()
            return redirect('/Contact')
        return render(request, 'contacts/new_contact.html', {'form': form})

    def get(self, request):
        form = ContactForm()
        return render(request, 'contacts/new_contact.html', {'form': form})


@method_decorator(decorators, name='dispatch')
class EditContactView(UpdateView):
    model = Contact
    fields = ('FirstName', 'LastName', 'Address', 'ContactNo')
    template_name = 'contacts/edit_contact.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'contact'

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.save()
        return redirect('/Contact')


@method_decorator(decorators, name='dispatch')
class ContactDelete(View):
    template_name = "contacts/contact_confirm_delete.html"

    def get_object(self):
        id = self.kwargs.get('pk')
        obj = None
        if id is not None:
            obj = get_object_or_404(Contact, id=id)
        return obj

    def get(self, request, *args, **kwargs):
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
            return redirect('/Contact')
        return render(request, self.template_name, context)


@method_decorator(decorators, name='dispatch')
class Upload(View):

    def get(self, request):
        template = "contact_upload.html"
        prompt = {
            'order': 'Order of the CSV should be Last name, ' +
            'First name,Contact Number, Address'
        }
        if request.method == "GET":
            return render(request, template, prompt)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            prompt = {
                'order': 'Please upload .csv file only'
            }
            return render(request, template, prompt)

    def post(self, request):
        csv_file = request.FILES['file']
        date_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(date_set)
        next(io_string)
        for column in csv.reader(
                io_string, delimiter=str(u','), quotechar=str(u"|")):
            _, created = Contact.objects.update_or_create(
                creator=request.user,
                LastName=column[0],
                FirstName=column[1],
                ContactNo=column[2],
                Address=column[3],

            )
        # contacts = Contact.objects.filter(creator=request.user)
        return redirect('/Contact')


@method_decorator(decorators, name='dispatch')
class Export(View):

    def get(self, request):
        contacts = Contact.objects.filter(creator=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact.csv"'
        writer = csv.writer(response, delimiter=str(u','))
        writer.writerow([
            'Last Name',
            'First Name',
            'Contact No.',
            'Address'])
        for contact in contacts:
            writer.writerow([
                contact.LastName,
                contact.FirstName,
                contact.ContactNo,
                contact.Address])
        return response


@method_decorator(decorators, name='dispatch')
class home(View):

    def get(self, request):
        return render(request, 'home.html', {})


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
