import base64
import json
import warnings
from io import BytesIO
from pathlib import PurePosixPath

from PIL import UnidentifiedImageError
from PIL.Image import Image
from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError

phone_regex = RegexValidator(
    regex=r'^\+\d{10,15}$',
    message="Phone number is invalid. Try: '+(country code)(number)'. example: +79123456789."
)


class ImageValidator:
    """
    Base Image Validation class
    Validates image format
    :param extensions: Tuple or List of file extensions, that should pass the validation
    Raises rest_framework.exceptions.ValidationError: in case file extension are not in the list
    """
    warning_msg = 'Warning! Pillow is not installed, validation has not been done'
    default_extensions = [
        'bmp',
        'jpeg',
        'jpg',
        'png',
    ]

    def __init__(self, extensions=None, **kwargs):
        if extensions is not None:
            assert isinstance(extensions, (tuple, list)), "extensions must be list or tuple"
            self.extensions = extensions
        else:
            self.extensions = self.default_extensions
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self, value):
        if isinstance(value, (str, bytes)):
            value = json.loads(value)
        file_extension = PurePosixPath(value['name']).suffix
        if value and file_extension[1:] not in self.extensions:
            raise ValidationError(f'unsupported image file format,'
                                              f' expected ({",".join(self.extensions)}),'
                                              f' got {file_extension[1:]}')


class ImageOpenValidator(ImageValidator):
    """
    Image validator that checks if image can be unpacked from b64 to PIL Image obj

    Raises rest_framework.exceptions.ValidationError: in case PIL throws error when trying to open given file
    """
    error_msg = 'for some reason, this image file cannot be opened'

    def __call__(self, value):
        if isinstance(value, (str, bytes)):
            value = json.loads(value)
        super().__call__(value)
        try:
            self.img = Image.open(BytesIO(base64.b64decode(value['content'])))
        except UnidentifiedImageError:
            raise ValidationError(self.error_msg)


class ImageBaseSizeValidator(ImageOpenValidator):
    """
    If you want you want to use this class for validating image width/height, you should rewrite
    self.orientation to ('height',) or ('width',) or ('height', 'width')

    Raises rest_framework.exceptions.ValidationError: if not(min <= (height or width) <= max)
    """
    orientation = ()

    def __call__(self, value):
        if isinstance(value, (str, bytes)):
            value = json.loads(value)
        super().__call__(value)
        self.validate()

    def validate(self):
        for orientation in self.orientation:
            min_value = getattr(self, f'min_{orientation}', 1)
            max_value = getattr(self, f'max_{orientation}', float('inf'))
            value = getattr(self.img, orientation)
            if not (min_value <= value <= max_value):
                raise ValidationError(f'Invalid image {orientation}. Expected from {min_value}'
                                                  f' to {max_value}, got {value}')


class ImageHeightValidator(ImageBaseSizeValidator):
    """
    Wrapper for _ImageBaseSizeValidator that validates only height

    :param min_height: minimal height of an image being validated
    :param max_height: maximal height of an image being validated
    """
    orientation = ('height',)


class ImageWidthValidator(ImageBaseSizeValidator):
    """
    Wrapper for _ImageBaseSizeValidator that validates only height

    :param min_width: minimal width of an image being validated
    :param max_width: maximal width of an image being validated
    """
    orientation = ('width',)


class ImageResolutionValidator(ImageBaseSizeValidator):
    """
    Wrapper for _ImageBaseSizeValidator that validates both height and width

    :param min_height: minimal height of an image being validated
    :param max_height: maximal height of an image being validated
    :param min_width: minimal width of an image being validated
    :param max_width: maximal width of an image being validated
    """
    orientation = ('height', 'width')
