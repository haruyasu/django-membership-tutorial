from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer
from datetime import datetime
from dateutil.relativedelta import relativedelta

User = get_user_model()


# アカウント登録
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data
            name = data['name']
            email = data['email'].lower()
            password = data['password']

            # ユーザーの存在確認
            if not User.objects.filter(email=email).exists():
                # ユーザーが存在しない場合は作成
                User.objects.create_user(name=name, email=email, password=password)

                return Response(
                    {'success': 'ユーザーの作成に成功しました'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': '既に登録されているメールアドレスです'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except:
            return Response(
                {'error': 'アカウント登録時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ユーザー情報取得
class UserView(APIView):
    def get(self, request):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        
        except:
            return Response(
                {'error': 'ユーザーの取得に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# サブスク定期請求
class SubscriptionView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            print("SubscriptionView")
            print(request.data)
            email = request.data["email"]
            customer_id = request.data["customer_id"]
            created = request.data["created"]
            user_data = User.objects.filter(customer_id=customer_id)
            if len(user_data):
                user_data = user_data[0]
            else:
                user_data = User.objects.get(email=email)
                user_data.customer_id = customer_id
            created = datetime.fromtimestamp(created)
            # 有効期限は1ヶ月後を設定
            user_data.current_period_end = created + relativedelta(months=1)
            user_data.save()

            return Response(
                {'success': 'サブスク有効期限の更新に成功しました'},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'サブスク有効期限の更新に失敗しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )