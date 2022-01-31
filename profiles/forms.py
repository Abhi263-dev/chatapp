from .models import User, Interest
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):

	class Meta:
		model = User
		fields=("username", "email" ,"password1", "password2","photo","dob")


class InterestForm(forms.Form):
	interests=Interest.objects.all()
	INTEREST_CHOICES=[]
	for i in interests:
		INTEREST_CHOICES.append((i.pk, i.name))
	field=forms.MultipleChoiceField(choices=INTEREST_CHOICES, widget=forms.CheckboxSelectMultiple)