import re
from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/((watch\?v=)|(embed/)|(v/)|(.+\?v=))')
        # tmp_val = dict(value).get(self.field)
        if value:
            if reg.match(value):
                raise ValidationError(f'{self.field}: ссылки на Youtube запрещены')
