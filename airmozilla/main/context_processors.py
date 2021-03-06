from django.conf import settings
from django.contrib.flatpages.models import FlatPage

from funfactory.urlresolvers import reverse

from airmozilla.main.models import (
    Event,
    Channel,
    get_profile_safely
)


def sidebar(request):
    # none of this is relevant if you're in certain URLs
    if '/manage/' in request.path_info:
        return {}

    data = {
        # used for things like {% if event.attr == Event.ATTR1 %}
        'Event': Event,
    }
    featured = (Event.objects.archived()
                .filter(featured=True).order_by('-start_time'))

    upcoming = Event.objects.upcoming().order_by('start_time')
    # if viewing a specific page is limited by channel, apply that filtering
    # here too
    if getattr(request, 'channels', None):
        channels = request.channels
    else:
        channels = Channel.objects.filter(slug=settings.DEFAULT_CHANNEL_SLUG)

    if request.user.is_active:
        profile = get_profile_safely(request.user)
        if profile and profile.contributor:
            feed_privacy = 'contributors'
        else:
            feed_privacy = 'company'
    else:
        feed_privacy = 'public'

    if settings.DEFAULT_CHANNEL_SLUG in [x.slug for x in channels]:
        feed_title = 'AirMozilla RSS'
        feed_url = reverse('main:feed', args=(feed_privacy,))
        sidebar_channel = settings.DEFAULT_CHANNEL_SLUG
    else:
        _channel = channels[0]
        feed_title = 'AirMozilla - %s - RSS' % _channel.name
        feed_url = reverse('main:channel_feed',
                           args=(_channel.slug, feed_privacy))
        sidebar_channel = _channel.slug
    data['feed_title'] = feed_title
    data['feed_url'] = feed_url

    featured = featured.filter(channels__in=channels)
    upcoming = upcoming.filter(channels__in=channels)

    if not request.user.is_active:
        featured = featured.filter(privacy=Event.PRIVACY_PUBLIC)
        upcoming = upcoming.filter(privacy=Event.PRIVACY_PUBLIC)
    upcoming = upcoming[:settings.UPCOMING_SIDEBAR_COUNT]
    data['upcoming'] = upcoming
    data['featured'] = featured

    try:
        data['sidebar_top'] = FlatPage.objects.get(
            url='sidebar_top_%s' % sidebar_channel
        )
    except FlatPage.DoesNotExist:
        data['sidebar_top'] = None
    try:
        data['sidebar_bottom'] = FlatPage.objects.get(
            url='sidebar_bottom_%s' % sidebar_channel
        )
    except FlatPage.DoesNotExist:
        data['sidebar_bottom'] = None

    return data


def analytics(request):
    # unless specified, the analytics is include if DEBUG = False
    include = getattr(
        settings,
        'INCLUDE_ANALYTICS',
        not settings.DEBUG
    )
    return {'INCLUDE_ANALYTICS': include}
