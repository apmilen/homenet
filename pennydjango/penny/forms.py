from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from penny.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'That email is already in use with a different account'
            )
        return email
