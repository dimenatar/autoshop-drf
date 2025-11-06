from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_url'] = '/register/'
        context['login_url'] = '/login/'
        return context


class LoginView(TemplateView):
    template_name = 'registration/login.html'


class RegisterView(TemplateView):
    template_name = 'registration/register.html'


class PasswordResetView(TemplateView):
    template_name = 'registration/password_reset.html'

class PasswordResetConfirmView(TemplateView):
    template_name = 'registration/password_reset_confirm.html'