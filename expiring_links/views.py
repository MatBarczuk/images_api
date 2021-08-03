from datetime import datetime, timedelta
from uuid import uuid4

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from expiring_links.models import ExpiringLink
from expiring_links.serializers import ExpiringLinkGeneratorSerializer


class ExpiringLinkView(viewsets.ViewSet):
    def create(self, request):
        result = ExpiringLinkGeneratorSerializer(data=request.data, context={'user': request.user})
        if result.is_valid():
            token = uuid4()
            expiration_date = datetime.now() + timedelta(seconds=result.data.get('expiration_time'))
            print(expiration_date)
            url = result.data.get('url')
            ExpiringLink.objects.create(url=url, token=token, expiration_date=expiration_date)

            expiring_link_parts = url.rsplit('.', 1)
            expiring_link = f'{expiring_link_parts[0]}{token}.{expiring_link_parts[1]}'
            return Response({'link': expiring_link})
        return Response(result.errors)
