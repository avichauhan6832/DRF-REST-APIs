from django.urls import path
from .views import ListEventView, LoginView, EventDetailView, GetRegisteredEvents, RegisterEvent, UnregisterEvent, InvitationList

urlpatterns = [
    path('events/', ListEventView.as_view(), name="events-all"),
    path('events/<int:pk>', EventDetailView.as_view(), name="event-particular"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('registered-events/', GetRegisteredEvents.as_view(), name="get-registered-events"),
    path('register/<int:pk>', RegisterEvent.as_view(), name="register"),
    path('unregister/<int:pk>', UnregisterEvent.as_view(), name="unregister"),
    path('invitation/', InvitationList.as_view(), name="invitation-list")
]
