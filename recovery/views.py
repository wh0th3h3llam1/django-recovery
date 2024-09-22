import logging
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializers import RecoveryCodeSerializer, ResetPasswordSerializer
from .utils import bulk_create_recovery_codes

logger = logging.getLogger(__name__)
User = get_user_model()

# Create your views here.


class RetrieveRecoveryCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieve the RecoveryCodes for the user"""

        data = RecoveryCodeSerializer(instance=request.user.recovery_codes.all(), many=True).data
        return Response(data={"recovery_codes": data}, status=HTTP_200_OK)


class GenerateRecoveryCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if codes := user.recovery_codes.filter(revoked_at__isnull=True):
            codes.update(revoked_at=timezone.now())

        try:
            recoverycodes = bulk_create_recovery_codes(user=user)
            msg = {
                "message": "Recovery Codes generated successfully",
                "data": RecoveryCodeSerializer(recoverycodes, many=True).data,
            }
            response_status = HTTP_200_OK
        except Exception as err:
            logger.error(err)
            msg = {"message": "Error generating Recovery Codes"}
            response_status = HTTP_400_BAD_REQUEST

        return Response(data=msg, status=response_status)


class ResetPasswordView(APIView):
    """Reset Password of user using one of the active recovery codes"""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        sz = ResetPasswordSerializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()

        return Response(
            data={"message": "Password Reset Successfully"},
            status=HTTP_202_ACCEPTED,
        )
