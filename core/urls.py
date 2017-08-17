from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('trust_anchor.urls', namespace='trust_anchor')),
]
