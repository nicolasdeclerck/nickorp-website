from django.contrib.auth.views import LoginView
from django.contrib import messages


class SuperuserLoginView(LoginView):
    template_name = 'auth/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_superuser:
            messages.error(self.request, "Accès réservé aux administrateurs.")
            return self.form_invalid(form)
        return super().form_valid(form)
