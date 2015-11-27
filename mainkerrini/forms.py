from django import forms
import magic, re
from mainkerrini.models import UserLogin
from mainkerrini.custom_functions import check_file_header
import bcrypt


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, required='true', widget=forms.TextInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'First Name'}))

    last_name = forms.CharField(max_length=50, required='true', widget=forms.TextInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Last Name'}))

    username = forms.CharField(max_length=50, required='true', widget=forms.TextInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Username'}))

    email_address = forms.EmailField(max_length=100, required='true', widget=forms.EmailInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Email'}))

    password = forms.CharField(max_length=50, required='true', widget=forms.PasswordInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Password'}),
                                error_messages = {'invalid': 'Your Email Confirmation Not Equal With Your Email'})
    confirm_password = forms.CharField(max_length=50, required='true', widget=forms.PasswordInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Confirm Password'}))

    def clean_email_address(self):
        email = self.cleaned_data['email_address']
        if UserLogin.objects.filter(email=email):
            raise forms.ValidationError("this email address already exists")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("password must be more than 6 characters long")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data['confirm_password']
        if len(password) < 6:
            raise forms.ValidationError("password must be more than 6 characters long")
        return password

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_pwd = cleaned_data.get("confirm_password")
        if password and confirm_pwd:
            if password != confirm_pwd:
                self.add_error('password', "passwords do not match")


class LoginForm(forms.Form):
    email_address = forms.EmailField(max_length=50, required='true', widget=forms.EmailInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=50, required='true', widget=forms.PasswordInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Password'}))

    def clean_email_address(self):
        print("checking email")
        email = self.cleaned_data['email_address']
        if not UserLogin.objects.filter(email=email):
            raise forms.ValidationError("email address not found")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("password must be more than 6 characters long")
        return password

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        password = cleaned_data.get("password")
        email = cleaned_data.get("email_address")
        if password and email:
            user = UserLogin.objects.get(email=email.lower())
            if not password == user.password:
                self.add_error('password', "password is incorrect")


class AccountForm(forms.Form):
    first_name = forms.CharField(max_length=50, required='true', widget=forms.TextInput(attrs=
                                {'class': 'form-control', 'required': 'true'}))

    last_name = forms.CharField(max_length=50, required='true', widget=forms.TextInput(attrs=
                                {'class': 'form-control', 'required': 'true'}))

    bio = forms.CharField(max_length=500, required='false', widget=forms.Textarea(attrs={'class': 'form-control'}))


class ImageForm(forms.Form):
    image = forms.FileField(label="select image to upload")


class VideoForm(forms.Form):
    LANGUAGE_CHOICES = (("ENG", "English"), ("FR", "French"), ("SPA", "Spanish"),
                        ("CHN", "Chinese"), ("ITA", "Italian"), ("ARA", "Arabic"))
    FORMAT_CHOICES = ('video/mp4', 'video/ogg', 'video/webm')

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    title = forms.CharField(min_length=1, max_length=500)
    description = forms.CharField(max_length=1000)
    file = forms.FileField(label="select video to upload")

    def clean_file(self):
        myreg = re.compile(r'(mp4)|(ogg)|(webm)', re.I)
        file = self.cleaned_data.get("file", False)
        filetype = myreg.search((magic.from_buffer(file.read(), mime=True)).decode())

        if filetype is None:
            raise forms.ValidationError("Wrong file type")
        return file

