from rest_framework import status
from eCommerce.choices import City
from ninja import Router
from ..models import Profile
from django.contrib.auth import get_user_model
from restauth.authorization import AuthBearer
from ..schemas.profile import DataIn, ProfileOut
from eCommerce.schemas.cart import MessageOut

User = get_user_model()

profile_router = Router(tags=['Profile'])


@profile_router.put('update-profile/', response={
    200: MessageOut,
    404: MessageOut,
    422 : MessageOut
}, auth=AuthBearer())
def update_profile(request, data_in: DataIn):
    try:
        profile = Profile.objects.get(
            user=User.objects.get(id=request.auth['pk']))

        profile.user.user_name = data_in.user_name

        cities = [i[0] for i in City.choices]
        if data_in.address in cities:
            profile.address = data_in.address
        else:
            return status.HTTP_404_NOT_FOUND, {'detail': 'Invalid address'}
        
        profile.user.email  = data_in.email.strip()

        profile.save() 
        profile.user.save()

        return status.HTTP_200_OK, {'detail':'Profile updated successfully!'}

    except Profile.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'Profile does not exist'}



@profile_router.get('profile-data/', response={
    200: ProfileOut,
    404: MessageOut
}, auth=AuthBearer())
def get_profile_data(request):
    try:
        profile = Profile.objects.get(
            user=User.objects.get(id=request.auth['pk']))
        
        print(profile.user.user_name,profile.user.email)

        return status.HTTP_200_OK, {
            'user_name': profile.user.user_name,
            'email':profile.user.email,
            'address': profile.address
        }

    except Profile.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'Profile does not exist'}
