# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Expense
# from .serializers import ExpenseSerializer
# from rest_framework import status

# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from .models import Expense
# from .serializers import ExpenseSerializer

# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# from .serializers import RegisterSerializer, ExpenseSerializer


# class ExpenseViewSet(ModelViewSet):
#     queryset = Expense.objects.all()
#     serializer_class = ExpenseSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

# @api_view(['GET', 'POST'])
# def expense_list(request):

#     if request.method == "GET":
#         expenses = Expense.objects.all()
#         serializer = ExpenseSerializer(expenses, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = ExpenseSerializer(data=request.data)
#         if serializer.is_valid():
#             expense = serializer.save()
#             print("SAVED:", expense)   # 👈 ADD THIS
#             return Response(serializer.data, status=201)

# @api_view(['GET','PUT','DELETE'])
# def expense_detail(request, pk):
#     try:
#         expense= Expense.objects.get(pk=pk)
#     except Expense.DoesNotExist:
#         return Response({'error':"Expense not found"}, status=status.HTTP_404_NOT_FOUND)
    

#     # GET single expense
#     if request.method == 'GET':
#         serializer = ExpenseSerializer(expense)
#         return Response(serializer.data)

#     # PUT update expense
#     elif request.method == 'PUT':
#         serializer = ExpenseSerializer(expense, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # DELETE expense
#     elif request.method == 'DELETE':
#         expense.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['POST'])
# def register_user(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         token = Token.objects.create(user=user)
#         return Response({
#             'token': token.key,
#             'username': user.username
#         }, status=201)
#     return Response(serializer.errors, status=400)



from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Expense
from .serializers import ExpenseSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny


# ------------------------
# Expense CRUD with ViewSet
# ------------------------
class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        # If user is NOT logged in → return empty list
        if user.is_anonymous:
            return Expense.objects.none()

        # Logged-in user → only their expenses
        return Expense.objects.filter(user=user)

    def perform_create(self, serializer):
        # Expense is saved for the logged-in user
        serializer.save(user=self.request.user)

# ------------------------
# User Registration
# ------------------------
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        }, status=201)
    return Response(serializer.errors, status=400)
