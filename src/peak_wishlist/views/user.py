from django.views.generic import (
    CreateView,
    UpdateView,
)
from django.urls import reverse_lazy
from peak_wishlist.forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth import get_user_model



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