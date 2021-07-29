from django.urls import path

from expiring_links.views import ExpiringLinksView

expiring_link = ExpiringLinksView.as_view({'post': 'create'})
urlpatterns = [
    path('links/', expiring_link)
]
