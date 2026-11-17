from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Cliente

CAMPO = (
    "w-full border-2 border-tinta bg-white/70 px-4 py-3 text-tinta outline-none "
    "transition duration-200 placeholder:text-suave "
    "focus:-translate-y-0.5 focus:border-tijolo focus:bg-white focus:shadow-hard-sm"
)


class EstiloMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs['class'] = CAMPO


class LoginForm(EstiloMixin, AuthenticationForm):
    pass


class CadastroForm(EstiloMixin, UserCreationForm):
    nome = forms.CharField(max_length=150, label='Nome completo')
    field_order = ['nome', 'username', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nome']
        if commit:
            user.save()
            Cliente.objects.update_or_create(
                usuario=user, defaults={'nome': self.cleaned_data['nome']}
            )
        return user
