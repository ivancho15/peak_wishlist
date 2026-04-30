from django.views.generic import (
    CreateView,
    UpdateView,
)
from django.urls import reverse_lazy
from peak_wishlist.forms import CustomUserCreationForm, UserProfileForm, AvatarForm
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required # type:ignore
from django.shortcuts import render, redirect
from peak_wishlist.models import Avatar


@method_decorator(login_not_required, name='dispatch')
class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "peak_wishlist/register.html"
    success_url = reverse_lazy("peak_wishlist:login")


class Profile(UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = "peak_wishlist/profile.html"
    success_url = reverse_lazy("peak_wishlist:index")

    def get_object(self):
        return self.request.user
    


def upload_avatar(request):
    avatar, created = Avatar.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            form.save()
            return redirect('peak_wishlist:profile')
    else:
        form = AvatarForm(instance=avatar)
        
    return render(request, 'peak_wishlist/avatar.html', {'form': form})