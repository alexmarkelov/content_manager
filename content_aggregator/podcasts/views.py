from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Episode


class HomePageView(View):
    template_name = "podcasts/homepage.html"

    def get(self, request):
        return render(request, self.template_name)


class LastPodcastsView(LoginRequiredMixin, ListView):
    template_name = "podcasts/last_podcasts.html"
    model = Episode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = Episode.objects.filter().order_by("-pub_date")[:10]
        return context

# Create your views here.
