from ..models import UserAccountDetails
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_nickname(request):
    try:
        user = request.user
        user_account_details = UserAccountDetails.objects.get_or_create(
            user=user)[0]
        user_account_details.nick_name = request.data['nickname']
        user_account_details.save()
        return Response({'success': 'Nickname changed successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
