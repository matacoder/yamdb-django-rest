from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_score(value):
    if value > 10 or value < 1:
        raise ValidationError(
            _('%(value)s must be from 1 to 10'),
            params={'value': value},
        )
