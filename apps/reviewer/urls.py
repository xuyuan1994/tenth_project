from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),    # This line has changed!
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_review$', views.add_review),
    url(r'^process_review$', views.process_review),
    url(r'^users/(?P<user_id>\d+)', views.user),
    url(r'^back$', views.back),
  ]