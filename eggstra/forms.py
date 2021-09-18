from django import forms

from .models import EggsAvailable, User, UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('location',)

# from django import forms
# from django.contrib.auth.forms import UserCreationForm

# class SignUpForm(UserCreationForm):
#     location = forms.CharField(max_length=30)

#     class Meta:
#         model = User
#         fields = ('username', 'location', 'password1', 'password2', )

class PostForm(forms.ModelForm): 
    amount = forms.IntegerField(label="Amount")
    notes = forms.CharField(label="Notes", max_length=64)

    class Meta: 
        model = EggsAvailable
        fields = ('amount', 'notes', )