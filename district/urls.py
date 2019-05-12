from django.conf.urls import url, patterns
from .views import MainPage


urlpatterns = patterns(
    '',
    url(r'', MainPage.as_view(), name='index'),
)