import asyncio
import os.path

from operator import (
    attrgetter,
)

from django.conf import (
    settings,
)
from telethon import (
    TelegramClient,
)
from telethon.tl.functions.messages import (
    GetHistoryRequest,
)

from .models import (
    Post,
)


def get_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def get_coroutine_result(coroutine):
    loop = get_loop()
    results = loop.run_until_complete(asyncio.wait(
        (
            coroutine,
        ),
    ))
    tasks = next(iter(results))
    task = next(iter(tasks))
    return task.result()


def get_client() -> TelegramClient:
    session_path = os.path.join(
        settings.TELEGRAM_SESSION_DIRECTORY,
        settings.TELEGRAM_SESSION,
    )

    loop = get_loop()
    client = TelegramClient(
        session=session_path,
        api_id=settings.TELEGRAM_API_ID,
        api_hash=settings.TELEGRAM_API_HASH,
        loop=loop,
    )
    client.start(
        phone=settings.TELEGRAM_PHONE,
    )
    return client


def get_channel(client: TelegramClient):
    return get_coroutine_result(
        coroutine=client.get_entity(
            entity=settings.TELEGRAM_CHANNEL,
        )
    )


GET_MESSAGES_PER_TIME = 100
GET_MESSAGES_FOR_THE_FIRST_TIME = 1000


def get_posts(recent=True) -> int:
    client = get_client()
    channel = get_channel(client)

    is_empty = not Post.objects.count()
    if is_empty:
        recent = False

    offset_id = 0
    if not recent and not is_empty:
        offset_id = Post.objects.values_list('id', flat=True).last()

    loaded_messages_count = 0
    load_more = True

    while load_more:
        coroutine_getting_history = client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=GET_MESSAGES_PER_TIME,
            max_id=0,
            min_id=0,
            hash=0,
        ))
        history = get_coroutine_result(
            coroutine=coroutine_getting_history,
        )
        if not history.messages:
            break

        messages_ids = tuple(map(
            attrgetter('id'),
            history.messages,
        ))
        offset_id = messages_ids[-1]

        new_posts_iterator = (
            Post(
                id=message.id,
                published=message.date,
                content=message.raw_text,
            )
            for message in history.messages
            if message.raw_text
        )

        if recent:
            existing_ids = set(Post.objects.filter(
                id__in=messages_ids,
            ).values_list(
                'id',
                flat=True,
            ))
            if existing_ids:
                load_more = False

            new_posts_iterator = filter(
                lambda post: post.id not in existing_ids,
                new_posts_iterator,
            )

        new_posts_tuple = tuple(new_posts_iterator)

        loaded_messages_count += len(new_posts_tuple)
        if (not recent
                and loaded_messages_count >= GET_MESSAGES_FOR_THE_FIRST_TIME):
            load_more = False

        Post.objects.bulk_create(new_posts_tuple)

    return loaded_messages_count
