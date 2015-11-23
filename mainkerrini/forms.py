from django import forms
from mainkerrini.models import UserLogin
from cassandra.cqlengine.models import Model

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, required='true', widget=forms.TextInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'First Name'}))

    last_name = forms.CharField(max_length=50, required='true', widget=forms.TextInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Last Name'}))

    username = forms.CharField(max_length=50, required='true', widget=forms.TextInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Username'}))

    email_address = forms.EmailField(max_length=100, required='true', widget=forms.EmailInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Email'}))

    password = forms.CharField(min_length=6, max_length=50, required='true', widget=forms.PasswordInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(min_length=6, max_length=50, required='true', widget=forms.PasswordInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Confirm Password'}))

    def is_valid(self):
        # run the parent validation first
        valid = super(RegisterForm, self).is_valid()

        if not valid:
            return valid

        try:
            user1 = UserLogin.objects.get(email=self.cleaned_data['email_address'].lower())
            return False
        except Model.DoesNotExist:
            user2 = UserLogin.objects.filter(username=self.cleaned_data['username'])
            if len(user2) > 0:
                return False
            return self.cleaned_data['password'] == self.cleaned_data['confirm_password']

