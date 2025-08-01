import re
from rest_framework.serializers import ValidationError


class VideoReferenceValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = r"http?://(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})"
        tmp_val = dict(value).get(self.field)

        if tmp_val is None:
            return

        matches = re.findall(pattern, tmp_val)
        if matches and not 'youtube.com' in matches:
                raise ValidationError('Нельзя прикреплять ссылки на сторонние ресурсы, кроме youtube.com')
