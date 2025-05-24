from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import LoginUserForm, RegisterUserForm, ProfileUpdateForm, AvatarUploadForm
from .models import Profile
from orders.models import Order



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = '/users/login/'

    def get_user_context(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items() + list(c_def.items())))


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Exception:
        Profile.objects.create(user=request.user)
        profile = request.user.profile
    orders = Order.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'users/profile.html', {'form' : form , 'orders': orders})

@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = AvatarUploadForm(instance=profile)

    return render(request, 'users/profile.html', {'avatar_form' : form })


