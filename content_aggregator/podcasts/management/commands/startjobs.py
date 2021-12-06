
# Standard library
import logging

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from podcasts.models import Episode, FeedChannel

# podcast URL:
PODCAST_URLs = [r"https://realpython.com/podcasts/rpp/feed",
                r"https://www.pythonpodcast.com/feed/mp3/"]

logger = logging.getLogger(__name__)


def save_new_episodes(feed, channel):
    podcast_title = channel
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
    for channel in FeedChannel.objects.all():
        _feed = feedparser.parse(channel.url)
        save_new_episodes(_feed, channel)


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            parse_new_feed,
            trigger="interval",
            minutes=10,
            id="Podcasts",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: New podcasts")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler ...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler ...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
