from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import EventSerializers, TokenSerializer
from .models import Event
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListEventView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = Event.objects.filter(public=True)
        return Response(
            data=EventSerializers(queryset, many=True).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        print(request.data)
        user = request.user
        # registered_events = user.registered_user.all()

        if user.registered_user.filter(event_date=datetime.strptime(request.data['event_date'], '%Y-%m-%d').date()).exists():
            return Response(
                data={
                    "message": "Sorry, You can't make an event, your previous one overlaps with this one"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        an_event = Event.objects.create(
            title=request.data['title'],
            author=user,
            event_date=request.data['event_date'],
            limit=request.data['limit'],
            public=request.data['public']
        )
        an_event.registered_user.add(user)

        for i in request.data['invited_user']:
            an_event.invited_user.add(User.objects.get(pk=i))

        return Response(
            data=EventSerializers(an_event).data,
            status=status.HTTP_201_CREATED
        )


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            event = self.queryset.get(pk=kwargs["pk"])
            return Response(EventSerializers(event).data)
        except Event.DoesNotExist:
            return Response(
                data={
                    "message": "Event with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            event = self.queryset.get(pk=kwargs["pk"])
            if event.author == request.user:
                event.delete()
                return Response(
                    data={
                        "message": "Deleted Successfully"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={
                        "message": "You are not authorized to delete this event"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Event.DoesNotExist:
            return Response(
                data={
                    "message": "Event with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class GetRegisteredEvents(generics.ListAPIView):
    serializer_class = EventSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        registered_events = user.registered_user.all()
        return Response(EventSerializers(registered_events, many=True).data)


class RegisterEvent(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs["pk"])
        user = request.user

        if event.limit <= event.registered_user.all().count():
            return Response(
                data={
                    "message": "Sorry, Event is full!"
                },
                status=status.HTTP_204_NO_CONTENT
            )

        previously_registered_events = user.registered_user.all()
        overlap = False
        for e in previously_registered_events:
            if e.event_date == event.event_date:
                overlap = True

        if overlap:
            return Response(
                data={
                    "message": "Sorry, You can't make to this event, your previous one overlaps with this one"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        registered_users = event.registered_user.all()
        if request.user in registered_users:
            return Response(
                data={
                    "message": "You are already registered!"
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            event.registered_user.add(request.user)
            return Response(
                data={
                    "message": "You are registered!"
                },
                status=status.HTTP_201_CREATED
            )


class UnregisterEvent(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            event = Event.objects.get(pk=kwargs["pk"])
            event.registered_user.remove(request.user)
            return Response(
                data={
                    "message": "You are unregistered from an event"
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                data={
                    "message": "Some error occurred"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )


class InvitationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        invitation = user.invited_user.all()
        return Response(EventSerializers(invitation, many=True).data)


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will override the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
