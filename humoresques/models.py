from django.conf import (
    settings,
)
from django.db import (
    models,
)
from pytz import (
    timezone,
)


class Post(models.Model):
    class Meta:
        ordering = (
            '-published',
        )

    content = models.TextField(
        verbose_name='Content',
    )
    published = models.DateTimeField(
        verbose_name='Publish Date',
    )

    def get_preview(self):
        # customization = settings.customization_section

        preview = self.content
        max_preview_len = settings.POST_PREVIEW_LEN
        # max_preview_len = customization['POST_PREVIEW_LEN']
        if len(preview) > max_preview_len:
            trailing = settings.POST_PREVIEW_TRAILING
            cut_idx = max_preview_len - len(trailing)
            preview = '{}{}'.format(
                preview[:cut_idx],
                trailing,
            )

        return preview
    get_preview.short_description = 'preview'

    def get_verbose_published(self):
        localized_published = self.published
        if settings.USE_TZ:
            using_timezone = timezone(
                settings.TIME_ZONE,
            )
            localized_published = localized_published.astimezone(
                using_timezone,
            )
        return localized_published.strftime(
            settings.DATETIME_FORMAT,
        )
    get_verbose_published.short_description = 'published'

    def __str__(self):

        return '{published}: {preview}'.format(
            published=self.get_verbose_published(),
            preview=self.get_preview(),
        )

    def __repr__(self):
        return '{cls}(published={published}, content={content})'.format(
            cls=self.__class__.__name__,
            published=repr(self.published),
            content=repr(self.content),
        )
