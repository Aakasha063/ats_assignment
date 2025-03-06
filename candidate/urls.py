from django.urls import path
from .views import CandidateAPIView, SearchCandidateAPIView

urlpatterns = [
    path('candidates/', CandidateAPIView.as_view(), name='candidate-list'),
    path('candidates/<int:pk>/', CandidateAPIView.as_view(), name='candidate-detail'),
    path('candidates/search', SearchCandidateAPIView.as_view(), name='candidate-search'),
]