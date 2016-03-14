from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'),
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': _('Username'),
                                                             'required': 'required',
                                                             'title': _('Username is required')}))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': _('Password'),
                                                                 'required': 'required',
                                                                 'title': _('is required Password')}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label=_('Username'),
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': _('Username'),
                                                             'required': 'required',
                                                             'title': _('Username is required')}))
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': _('Password'),
                                                                  'required': 'required',
                                                                  'title': _('Password is required')}))
    password2 = forms.CharField(label=_('Confirm Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': _('Confirm Password'),
                                                                  'required': 'required',
                                                                  'title': _('You mush confirm password')}))
    email = forms.CharField(label=_('Email'),
                            widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': _('Email'),
                                                           'required': 'required',
                                                           'title': _('Email is required')
                                                           }))
    first_name = forms.CharField(label=_('Firstname'),
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': _('Firstname'),
                                                               'required': 'required',
                                                               'title': _('Firstname is required')}))
    last_name = forms.CharField(label=_('Family Name'),
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': _('Family Name'),
                                                              'required': 'required',
                                                              'title': _('Family Name is required')}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.set_password(self.clean_password2())
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_('Firstname'),
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': _('Firstname'),
                                                               'required': 'required',
                                                               'title': _('Firstname is required')}))
    last_name = forms.CharField(label=_('Family Name'),
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': _('Family Name'),
                                                              'required': 'required',
                                                              'title': _('Family Name is required')}))
    email = forms.CharField(label=_('Email'),
                            widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': _('Email'),
                                                           'required': 'required',
                                                           'title': _('Email is required')
                                                           }))
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': _('Password'),
                                                                  'title': _('Password is required')}),
                                required=False)
    password2 = forms.CharField(label=_('Confirm Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': _('Confirm Password'),
                                                                  'title': _('You have to confirm password')}),
                                required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Password not match!'))
        return password2

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2' )

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if self.clean_password2():
            user.set_password(self.clean_password2())
        if commit:
            user.save()
        return user