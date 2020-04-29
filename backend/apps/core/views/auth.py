from django.http import Http404
from django.views.defaults import bad_request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.contrib.auth.models import User

from ..serializers.auth import *


class GetCredential(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        cred = request.query_params.get("username")
        try:
            User.objects.get(Q(username=cred) | Q(email=cred))
            return Response(data={'val': True, 'message': 'Success'})
        except Exception as e:
            return Response({'val': False, 'message': 'User with credentials does not exist'}, status=status.HTTP_404_NOT_FOUND)


class GetUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        return Response(data)
