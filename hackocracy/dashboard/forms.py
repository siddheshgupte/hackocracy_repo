from django import forms
from django.contrib.auth.models import User
from .models import transactions,Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = transactions
        fields = ('to','fro','amount',)
        labels = {
            "fro": "From"
        }

class UserRegistrationForm(forms.ModelForm):
    political_party = forms.CharField(max_length=50)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    party_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('political_party', 'party_image')
