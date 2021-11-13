from django.urls import path
from .views import RegisterView, UserView, SubscriptionView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('user/', UserView.as_view()),
    path('subscription/', SubscriptionView.as_view()),
]
