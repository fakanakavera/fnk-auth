from ..models import UserAccountDetails


def get_or_create_user_account_details(user):
    user_account_details, created = UserAccountDetails.objects.get_or_create(
        user=user)
    return user_account_details, created
