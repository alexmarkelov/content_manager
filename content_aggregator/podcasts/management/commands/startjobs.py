
import feedparser
from dateutil import parser
from django.core.management.base import BaseCommand
from podcasts.models import Episode

# podcast URL:
PODCAST_URLs = [r"https://realpython.com/podcasts/rpp/feed", r"https://talkpython.fm/episodes/rss"]


def save_new_episodes(feed):
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            episode = Episode(
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link=item.link,
                image=podcast_image,
                podcast_name=podcast_title,
                guid=item.guid,
            )
            episode.save()


def parse_new_feed():
    for url in PODCAST_URLs:
        _feed = feedparser.parse(url)
        save_new_episodes(_feed)


class Command(BaseCommand):
    def handle(self, *args, **options):
        parse_new_feed()

