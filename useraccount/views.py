from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView



class RegisterView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'dashboard/user/register.html'
    success_url = reverse_lazy('register')

    def test_func(self):
        # Ensure only superusers can access this view
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.is_staff = True
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Unsuccessful registration. Invalid information.")
        return super().form_invalid(form)


class RegisterListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/user/register_view.html'
    context_object_name = 'query'



class RegisterEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'dashboard/user/register-update.html'
    success_url = reverse_lazy('register_view')

    def test_func(self):
        # Ensure only superusers can access this view
        return self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, "Update successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Unsuccessful update. Invalid information.")
        return super().form_invalid(form)


@login_required
def register_delete(request, pk):
    query = get_object_or_404(User, pk=pk)
    query.delete()
    return redirect('register_view')



class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/user/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)

# def change_password(request):
#     current_user = request.user
#     form = PasswordChangeForm(current_user)
#     if request.method == 'POST':
#         form = PasswordChangeForm(current_user,data = request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('dashboard')
        
#     return render(request, 'dashboard/user/change_password.html', {
#         'form': form
#     })
