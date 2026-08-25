from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Matches Egyptian mobile numbers: 010/011/012/015 followed by 8 digits,
# with or without the +20 / 0020 country code prefix.
egyptian_phone_validator = RegexValidator(
    regex=r"^(?:\+20|0020|0)?1[0125]\d{8}$",
    message="Enter a valid Egyptian mobile number, e.g. 01012345678.",
)


class User(AbstractUser):
    """
    Custom user model that logs in with email instead of username.
    We keep `username` around (Django admin still uses it internally)
    but it is auto-filled from the email so nobody has to type it.
    """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20,
        validators=[egyptian_phone_validator],
        help_text="Egyptian mobile number, e.g. 01012345678",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_number"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
