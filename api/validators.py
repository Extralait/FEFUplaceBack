from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+\d{10,15}$',
    message="Phone number is invalid. Try: '+(country code)(number)'. example: +79123456789."
)