from django.contrib import (
    admin,
)
from rangefilter.filter import (
    DateRangeFilter,
)

from .models import (
    Post,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'get_verbose_published',
        'get_preview',
    )

    list_filter = (
        ('published', DateRangeFilter),
    )
