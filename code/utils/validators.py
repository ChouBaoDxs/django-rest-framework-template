from django.core.validators import FileExtensionValidator
from rest_framework import validators

from utils.regex import REGEX_PHONE


def validate_phone(phone):
    if not REGEX_PHONE.match(phone):
        raise validators.ValidationError('手机号不合法')


ZipFileExtensionValidator = FileExtensionValidator(['zip'])
