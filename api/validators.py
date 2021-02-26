from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+\d{10,15}$',
    message="Phone number is invalid. Try: '+(country code)(number)'. example: +79123456789."
)

class ImageValidator:
    """
    Base Image Validation class
    Validates image format
    Wont work if Pillow isn't installed
    :param extensions: Tuple or List of file extensions, that should pass the validation
    Raises rest_framework.exceptions.ValidationError: in case file extension are not in the list
    """
    warning_msg = 'Warning! Pillow is not installed, validation has not been done'
    default_extensions: _t.Union[_t.Tuple, _t.List] = [
        'bmp',
        'jpeg',
        'jpg',
        'png',
    ]

    def __init__(self, extensions: _t.Optional[_t.Union[_t.Tuple, _t.List]] = None, **kwargs):
        if extensions is not None:
            assert isinstance(extensions, (tuple, list)), "extensions must be list or tuple"
            self.extensions = extensions
        else:
            self.extensions = self.default_extensions
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self, value):
        if not self.has_pillow:
            warnings.warn(self.warning_msg, ImportWarning)
            return
        if isinstance(value, (str, bytes)):
            value = orjson.loads(value)
        file_extension = PurePosixPath(value['name']).suffix
        if value and file_extension[1:] not in self.extensions:
            raise serializers.ValidationError(f'unsupported image file format,'
                                              f' expected ({",".join(self.extensions)}),'
                                              f' got {file_extension[1:]}')

    @property
    def has_pillow(self):
        """
        Check if Pillow is installed
        """
        return has_pillow


class ImageOpenValidator(ImageValidator):
    """
    Image validator that checks if image can be unpacked from b64 to PIL Image obj

    Raises rest_framework.exceptions.ValidationError: in case PIL throws error when trying to open given file
    """
    error_msg = 'for some reason, this image file cannot be opened'

    def __call__(self, value):
        if not self.has_pillow:
            warnings.warn(self.warning_msg, ImportWarning)
            return
        if isinstance(value, (str, bytes)):
            value = orjson.loads(value)
        super().__call__(value)
        try:
            self.img = Image.open(BytesIO(base64.b64decode(value['content'])))
        except UnidentifiedImageError:
            raise serializers.ValidationError(self.error_msg)


class ImageBaseSizeValidator(ImageOpenValidator):
    """
    If you want you want to use this class for validating image width/height, you should rewrite
    self.orientation to ('height',) or ('width',) or ('height', 'width')

    Raises rest_framework.exceptions.ValidationError: if not(min <= (height or width) <= max)
    """
    orientation: _t.Union[_t.Union[_t.Tuple[str], _t.Tuple[str, str]], _t.Tuple] = ()

    def __call__(self, value):
        if not self.has_pillow:
            warnings.warn(self.warning_msg, ImportWarning)
            return
        if isinstance(value, (str, bytes)):
            value = orjson.loads(value)
        super().__call__(value)
        self.validate()

    def validate(self):
        for orientation in self.orientation:
            min_value = getattr(self, f'min_{orientation}', 1)
            max_value = getattr(self, f'max_{orientation}', float('inf'))
            value = getattr(self.img, orientation)
            if not (min_value <= value <= max_value):
                raise serializers.ValidationError(f'Invalid image {orientation}. Expected from {min_value}'
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