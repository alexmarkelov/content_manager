from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from .models import Episode, FeedChannel
# test data
test_title = "Test title"
test_description = "Some information about episode"
test_link = "https\\coubs.com"
test_image = "http:\\www.w3.org\\2000\\svg"
test_podcast_name = "My test podcast"
test_guid = "22345200-abe8-4f60-90c8-0d43c5f6c0f6"

class PodCastsTests(TestCase):
    def setUp(self) -> None:
        self.feed_channel = FeedChannel.objects.create(
            name=test_podcast_name,
            description=test_description,
            url=test_link,
        )
        self.episode = Episode.objects.create(
            title=test_title,
            description=test_description,
            pub_date=timezone.now(),
            link=test_link,
            image=test_image,
            podcast_name=self.feed_channel,
            guid=test_guid,
        )

    def test_episode_content(self):
        self.assertEqual(self.episode.description, test_description)
        self.assertEqual(self.episode.link, test_link)
        self.assertEqual(self.episode.guid, test_guid)

    def test_episode_str_repr(self):
        self.assertEqual(str(self.episode), test_podcast_name + ': ' + test_link + ': ' + test_title)

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("podcasts:homepage"))
        self.assertTemplateUsed(response, "podcasts/homepage.html")
