from django.urls import path
from .views import AuthorListCreateView, AuthorRetrieveUpdateDestroyView


urlpatterns = [
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorRetrieveUpdateDestroyView.as_view(), name='author-detail')
]