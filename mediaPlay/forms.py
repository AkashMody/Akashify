from django import forms
from .models import Listener
from django.utils.text import slugify

class ListenerForm(forms.ModelForm):
    
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Listener
        fields = ("first_name", "last_name", "gender", "contact", "email", "username", "password")
        
    
    def clean(self):
        SpecialSym =['$', '@', '#', '%', '_']
        cleaned_data = super(ListenerForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError(
                "Names should only have alphabets"
            )
        if any(char.isdigit() for char in last_name):
            raise forms.ValidationError(
                "Names should only have alphabets"
            )
        # if not username.isalnum():
        #     raise forms.ValidationError(
        #         "Username should be alphanumeric"
        #     )
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
        if len(password) < 8 or len(confirm_password) < 8:
            raise forms.ValidationError(
                "Password should be 8 characters long"
            )  
        if len(password) > 16 or len(confirm_password) > 16:
            raise forms.ValidationError(
                "Password should not be more than 16 characters long"
            )            
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(
                'Password should have at least one numeral'
            )
            
        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                'Password should have at least one uppercase letter'
            )           
            
        if not any(char.islower() for char in password):
            raise forms.ValidationError(
                'Password should have at least one lowercase letter'
            )
            
        if not any(char in SpecialSym for char in password):
            raise forms.ValidationError(
            'Password should have at least one of the symbols $@#_'
            )
        
            
        return cleaned_data