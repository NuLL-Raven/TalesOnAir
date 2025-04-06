from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Try to get user by username or email
        user = User.objects.filter(email=username_or_email).first()
        if user:
            username = user.username
        else:
            username = username_or_email

        self.user_cache = authenticate(self.request, username=username, password=password)

        if self.user_cache is None:
            raise forms.ValidationError("Invalid credentials")

        self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
