import time
from rest_framework.views import APIView
from rest_framework.response import Response


class ItemListView(APIView):
    def get(self, request, format=None):
        items = ['Item 1', 'Item 2', 'Item 3']
        time.sleep(1)
        return Response({'items': items})
