from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username: ', max_length=50)
    password = forms.CharField(label='Password: ', min_length=6, max_length=50, widget=forms.PasswordInput)
