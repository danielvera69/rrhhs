from django import forms
from django.forms import ModelForm
from apps.security.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "dni",
            "email",
            "organization",
            "groups",
            "image",
            "is_active"
        ]
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Guarda el valor actual del campo como valor inicial
        self.fields['password'].initial = self.instance.password if self.instance else None