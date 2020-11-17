from functools import (
    partial,
)
from itertools import (
    chain,
)
from operator import (
    attrgetter,
)

from django.contrib import (
    admin,
    messages,
)
from django.http import HttpResponseRedirect
from django.urls import (
    path, reverse,
)
from rangefilter.filter import (
    DateRangeFilter,
)

from .helpers import (
    get_posts,
)
from .models import (
    Post,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    change_list_template = 'humoresques/post_changelist.html'
    change_form_template = 'humoresques/post_changeform.html'

    list_display = (
        'get_verbose_published',
        'get_preview',
    )

    list_filter = (
        ('published', DateRangeFilter),
    )

    fields = (
        'published',
        'content',
    )

    date_hierarchy = 'published'

    def get_actions(self, request):
        result = super().get_actions(request)
        if 'delete_selected' in result:
            del result['delete_selected']
        return result

    def get_urls(self):
        result = super().get_urls()

        new_paths = (
            path('get_recent/', self._get_recent),
            path('get_more/', partial(self._get_recent, recent=False)),
        )
        result = list(chain(
            new_paths,
            result,
        ))

        return result

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def _get_recent(self, request, recent=True):
        count = get_posts(recent=recent)
        self.message_user(request, f'{count} Posts loaded!')
        return HttpResponseRedirect('../')

    def get_readonly_fields(self, request, obj=None):
        return tuple(set(chain(
            map(attrgetter('name'), self.opts.local_fields),
            map(attrgetter('name'), self.opts.local_many_to_many),
        )))

    def response_change(self, request, obj):
        require_next = '_next_post' in request.POST
        require_prev = '_prev_post' in request.POST

        if require_next or require_prev:
            if require_next:
                lookup = 'gt'
            else:
                lookup = 'lt'
            related_post_queryset = Post.objects.filter(**{
                f'published__{lookup}': obj.published,
            }).values_list(
                'id',
                flat=True,
            )

            if require_next:
                related_post_id = related_post_queryset.last()
            else:
                related_post_id = related_post_queryset.first()

            if related_post_id is None:
                self.message_user(
                    request,
                    'There is no {} post!'.format(
                        'next' if require_next else 'prev',
                    ),
                    level=messages.ERROR,
                )
                return self.changelist_view(
                    request=request,
                )

            href = reverse(
                viewname='admin:{}_{}_change'.format(
                    obj._meta.app_label,
                    obj._meta.model_name,
                ),
                args=(related_post_id,),
            )
            return HttpResponseRedirect(href)

        return super().response_change(request, obj)


