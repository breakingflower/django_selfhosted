from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import EggPost, Profile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location',)

class EggPostForm(forms.ModelForm): 

    class Meta: 
        model = EggPost
        exclude=['user',]

class RegisterForm(UserCreationForm): 
    email = forms.EmailField(required=True)
    location = forms.CharField(max_length=64)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit: 
            user.save() 
        
        user.profile.location = self.cleaned_data['location']

        return user