from django.urls import path
from . views import ListCustomUsersApiView, CreateCustomUserApiView, CompanyCreateListApiView, CompanyUpdateDeleteRetrieveApiView \
    , QuestionCreateListApiView, QuestionUpdateDeleteRetrieveApiView, ApplicationCreateListApiView, ApplicationUpdateDeleteRetrieveApiView \
    , InterviewCreateListApiView, InterviewUpdateDeleteRetrieveApiView, OfferCreateListApiView, OfferUpdateDeleteRetrieveApiView \
    , ResumeCreateListApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', CreateCustomUserApiView.as_view(), name='signup'),
    path('login', TokenObtainPairView.as_view(), name='signin'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('users', ListCustomUsersApiView.as_view(), name='list-users'),
    path('company', CompanyCreateListApiView.as_view(), name='list-create-company'),
    path('company/<int:pk>', CompanyUpdateDeleteRetrieveApiView.as_view(), name='crud-company'),
    path('question', QuestionCreateListApiView.as_view(), name='list-create-question'),
    path('question/<int:pk>', QuestionUpdateDeleteRetrieveApiView.as_view(), name='crud-question'),
    path('application', ApplicationCreateListApiView.as_view(), name='list-create-application'),
    path('application/<int:pk>', ApplicationUpdateDeleteRetrieveApiView.as_view(), name='crud-application'),
    path('interview', InterviewCreateListApiView.as_view(), name='list-create-interview'),
    path('interview/<int:pk>', InterviewUpdateDeleteRetrieveApiView.as_view(), name='crud-interview'),
    path('offer', OfferCreateListApiView.as_view(), name='list-create-offer'),
    path('offer/<int:pk>', OfferUpdateDeleteRetrieveApiView.as_view(), name='crud-offer'),
    path('resume', ResumeCreateListApiView.as_view(), name='list-create-resume'),
]