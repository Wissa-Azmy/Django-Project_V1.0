from django import forms
from .models import *
import os , string
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm


# class UserForm(forms.ModelForm):
#     class Meta:
#     	model = User
#         fields = ['email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'image','user']


class ArticleForm(forms.ModelForm):
    # read_later = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=User.objects.all())

    class Meta:
        model = Article
        fields = ['article_title', 'article_desc', 'article_body', 'article_img', 'article_status', 'article_author', 'article_tags']

class ArticleUserForm(forms.ModelForm):
    # read_later = forms.ModelMultipleChoiceField(widget=forms.CheckboxInput())
    class Meta:
        model = Article
        fields = ['article_title', 'article_desc', 'article_body', 'article_img', 'article_status', 'article_tags']


# class UserEditForm(MultiForm):
#     form_classes = {
#         'user': UserForm,
#         'profile': UserProfileForm,
#     }



class UserForm(forms.ModelForm):
    password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput())
    password2 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput())
    email = forms.EmailField(required=True,label=(u'Email Address'))
    username = forms.CharField(label=(u'Username'))
    first_name = forms.CharField(required=False,label=(u'First Name'))
    last_name = forms.CharField(required=False, label=(u'Last Name'))
    captcha1 = forms.CharField(required=True,label=(u'  '),widget=forms.TextInput(attrs={'readonly':'True'}))
    captcha2 = forms.CharField(required=True,label=(u' Please Enter this code '))


    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please Try with a different email address.')
        return email

    def clean_captcha2(self):
        captcha1 = self.cleaned_data.get('captcha1')
        captcha2 = self.cleaned_data.get('captcha2')

        if not captcha2:
            raise forms.ValidationError("You must Enter the code")
        if captcha1 != captcha2:
            raise forms.ValidationError("Code doesn't match , please try to enter it again")
        return captcha2

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match , please try again ")
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'image',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=(u'Username'))
    password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput())
    remember_me = forms.BooleanField(initial=False,required=False, widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ( 'username','password')

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
