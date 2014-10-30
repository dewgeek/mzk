from django import forms
from django.forms import ModelForm
from django.db import models
from models import *
from django.contrib.auth.models import User

class registerForm(forms.Form):	
	username = forms.CharField() 
	email = forms.EmailField()	
	pswd = forms.CharField(widget = forms.PasswordInput(render_value = False),min_length=8)
	password = forms.CharField(widget = forms.PasswordInput(render_value = False))

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username = username)
			raise forms.ValidationError("That username is already taken")
		except User.DoesNotExist:
			return username

	def clean_password(self):
		pswd = self.cleaned_data.get('pswd', '')
		pswd1 = self.cleaned_data['password']
		if pswd == '':
			raise forms.ValidationError("Password should be atleast 8 characters ")
		if pswd != pswd1:
			raise forms.ValidationError("Passwords do not match")
		return pswd	
	
	def clean_email(self):
		email_id = self.cleaned_data["email"]
		try:
			user_id = User.objects.get(email = email_id)
			raise forms.ValidationError("That email is already taken")
		except User.DoesNotExist:
			return email_id

class loginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput(render_value = False))
	
class AddressForm(forms.Form):
	order_id =forms.CharField(widget = forms.HiddenInput()) 
	address = forms.CharField(label='Address',widget=forms.Textarea)
	landmark = forms.CharField(label='Landmark')	
	mobile = forms.CharField(label='Mobile')
	quantity = forms.ChoiceField(widget=forms.Select(),choices=([(1,1), (2,2),(3,3),(4,4),(5,5),(6,6) ]))
	date = forms.CharField(widget = forms.HiddenInput())
	month = forms.CharField(widget = forms.HiddenInput())
	year = forms.CharField(widget = forms.HiddenInput())

class contactForm(forms.Form):
	name=forms.CharField() 
	email=forms.EmailField(required=False) 
	message=forms.CharField(label='Message',widget=forms.Textarea) 

class pswdForm(forms.Form):
	pswd = forms.CharField() 
	confirm_pswd = forms.CharField() 
	def clean_pswd(self):
		if len(self.cleaned_data["pswd"]) < 8:
			raise forms.ValidationError("Password should be atleast 8 characters")
		return self.cleaned_data["pswd"]
	def clean_confirm_pswd(self):
		if self.cleaned_data["pswd"] != self.cleaned_data["confirm_pswd"]:
			raise forms.ValidationError("Passwords do not Match")
		return self.cleaned_data["confirm_pswd"]