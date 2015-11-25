from django import forms
from mainkerrini.models import UserLogin

# TODO send "username/email already exist" error message back to page.
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
        print("in pwd")
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_pwd = cleaned_data.get("confirm_password")
        if password and confirm_pwd:
            if password != confirm_pwd:
                self.add_error('password', "passwords do not match")


# TODO send can't login error message.
class LoginForm(forms.Form):
    email_address = forms.EmailField(max_length=50, required='true', widget=forms.EmailInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=50, required='true', widget=forms.PasswordInput(attrs=
                                {'class': 'form-control', 'required': 'true', 'placeholder': 'Password'}))

    def is_valid(self):
        # run the parent validation first
        valid = super(LoginForm, self).is_valid()

        if not valid:
            return valid

        try:
            user = UserLogin.objects.get(email=self.cleaned_data['email_address'].lower())
            if bcrypt.hashpw(self.cleaned_data['password'].encode(), user.password.encode()) == user.password.encode():
                return True
        except Model.DoesNotExist:
            return False

        return False
