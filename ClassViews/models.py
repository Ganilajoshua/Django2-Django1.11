# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

class Contact(models.Model):
	numOnly 	= RegexValidator(r'^\d*$', 'Please Input your Contact Number.')
	creator 	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	FirstName 	= models.CharField(max_length=45)
	LastName 	= models.CharField(max_length=45)
	ContactNo 	= models.CharField(max_length=45,validators=[numOnly])
	Address 	= models.CharField(max_length=45)