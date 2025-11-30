from django.urls import path
from . import views

urlpatterns = [
    path('form-schema', views.get_form_schema, name='form-schema'),
    path('submissions', views.submissions_view, name='submissions'),
]