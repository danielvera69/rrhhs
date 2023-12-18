from django.urls import reverse_lazy
from apps.security.forms.profile import ProfileForm
from apps.security.mixins.mixins import PermissionMixin, UpdateViewMixin
from apps.security.models import User
from django.views.generic import UpdateView
from django.contrib.auth.forms import PasswordChangeForm

class ProfileUpdateView(PermissionMixin,UpdateViewMixin, UpdateView):
    model = User
    template_name = 'profile/form.html'
    form_class = ProfileForm
    success_url = reverse_lazy('security:profile_update')
    permission_required = 'change_userprofile'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Perfil'
        context['back_url'] = self.success_url
        return context
    
class UserPasswordUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = User
    template_name = 'profile/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('security:auth_login')
    permission_required = 'change_userpassword'

    def get_form(self, form_class=None):
        form = self.form_class(user=self.request.user)

        field_common = {
            'class': 'form-control',
            'autocomplete': 'off',
        }
        form.fields['old_password'].widget.attrs = {
            **field_common,
            'placeholder': 'Ingrese su contraseña actual',
        }
        form.fields['new_password1'].widget.attrs = {
            **field_common,
            'placeholder': 'Ingrese su nueva contraseña',
        }
        form.fields['new_password2'].widget.attrs = {
            **field_common,
            'placeholder': 'Repita su contraseña',
        }
        return form

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = ':Actualización de contraseña'
        context['grabar'] = 'Cambiar Password'
        context['back_url'] = self.success_url
        return context
