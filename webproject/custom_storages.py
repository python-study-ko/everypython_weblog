# s3에서 정적파일을 static 폴더에 저장하기 위해 커스텀 스토리지 객체를 생성함

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION

    def __init__(self, *args, **kwargs):
        if settings.AWS_CLOUDFRONT_DOMAIN:
            kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN

        super(StaticStorage, self).__init__(*args, **kwargs)
