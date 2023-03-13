from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from . serializers import ListCustomUserSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, CompanySerializer \
    , QuestionSerializer, ApplicationSerializer, InterviewSerializer, OfferSerializer, ResumeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from core.models import CustomUser, Company, Question, Application, Interview, Offer, Resume


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()


class CompanyCreateListApiView(ListCreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request = serializer.context['request']
        serializer.save(user_id=request.user)


class CompanyUpdateDeleteRetrieveApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]


class QuestionCreateListApiView(ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request = serializer.context['request']
        company = get_object_or_404(Company, id=serializer.validated_data['company_id'].id)
        serializer.save(user_id=request.user, company_id=company)


class QuestionUpdateDeleteRetrieveApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]


class ApplicationCreateListApiView(ListCreateAPIView):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request = serializer.context['request']
        company = get_object_or_404(Company, id=serializer.validated_data['company_id'].id)
        serializer.save(user_id=request.user, company_id=company)


class ApplicationUpdateDeleteRetrieveApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]


class InterviewCreateListApiView(ListCreateAPIView):
    serializer_class = InterviewSerializer
    queryset = Interview.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        application = get_object_or_404(Application, id=serializer.validated_data['application_id'].id)
        serializer.save(application_id=application)


class InterviewUpdateDeleteRetrieveApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = InterviewSerializer
    queryset = Interview.objects.all()
    permission_classes = [IsAuthenticated]


class OfferCreateListApiView(ListCreateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request = serializer.context['request']
        company = get_object_or_404(Company, id=serializer.validated_data['company_id'].id)
        serializer.save(user_id=request.user, company_id=company)


class OfferUpdateDeleteRetrieveApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]


class ResumeCreateListApiView(ListCreateAPIView):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request = serializer.context['request']
        company = get_object_or_404(Company, id=serializer.validated_data['company_id'].id)
        serializer.save(user_id=request.user, company_id=company)