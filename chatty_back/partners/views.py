from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from . import models, serializers
from chatty_back.diary.views import check_user



def get_partner(self, partner_id, creator):

    try:
        found_partner = models.Partner.objects.get(id=partner_id, creator=creator)
        return found_partner
    except models.Partner.DoesNotExist:
        return None


class Partner(APIView):

    @method_decorator(check_user())
    def post(self, request, user, format=None):

        new_partner_name = request.data.get('name', None)
        
        try:
            found_partner = models.Partner.objects.get(name=new_partner_name, creator=user)
            
        except models.Partner.DoesNotExist:
        
            serializer = serializers.CreatePartnerSerializer(data=request.data, partial=True)

            if serializer.is_valid():

                new_partner = serializer.save(creator=user)
                #파트너가 생성된 후, 직전에 생성된 파트너를 함께 일기 쓸 파트너로 선택하기
                user.partner = new_partner

                user.save()

                print(user.partner.name)

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                
            else:

                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PartnerProfile(APIView):

    @method_decorator(check_user())
    def get(self, request, user, partner_id, format=None):

        found_partner = get_partner(self, partner_id, user)

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else: 

            serializer = serializers.PartnerProfileSerializer(found_partner)

            return Response(data=serializer.data, status=status.HTTP_200_OK)


    @method_decorator(check_user())
    def put(self, request, user, partner_id, format=None):

        found_partner = get_partner(self, partner_id, user)

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            serializer = serializers.PartnerProfileSerializer(
                found_partner, data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)

            else:
                
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePartner(APIView):
    
    @method_decorator(check_user())
    def delete(self, request, user, partner_id, format=None):
        
        found_partner = get_partner(self, partner_id, user)

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            found_partner.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)


class SetPartner(APIView):

    @method_decorator(check_user())
    def put(self, request, user, partner_id, format=None):

        found_partner = get_partner(self, partner_id, user)
        
        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            user.partner = found_partner

            user.save()

            return Response(status=status.HTTP_200_OK)


# Main 화면에 있는 Partner 부분(Main 화면의 module화를 위한 API)
class Partner_Main(APIView):

    @method_decorator(check_user())
    def get(self, request, user, format=None):

        found_partner = user.partner

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            serializer = serializers.MainPartnerSerializer(found_partner)

            return Response(data=serializer.data, status=status.HTTP_200_OK)


class PartnerProfile_setting(APIView):

    @method_decorator(check_user())
    def get(self, request, user, format=None):

        found_partner = user.partner

        if found_partner is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            serializer = serializers.PartnerProfileSerializer(found_partner)

            return Response(data=serializer.data, status=status.HTTP_200_OK)