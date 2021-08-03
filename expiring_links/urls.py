from django.urls import path

from expiring_links.views import ExpiringLinkView

expiring_link = ExpiringLinkView.as_view({'post': 'create'})
urlpatterns = [
    path('links/', expiring_link)
]
