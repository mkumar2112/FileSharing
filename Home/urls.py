from django.urls import path
from .views import *



# Client user Working
urlpatterns = [
    path('client/create', clientUserRegistration.as_view()),
    path('login', LoginView.as_view(), name='login'),
    path('client/file', clientUser.as_view()),
    path('client/file/<id>', clientUser.as_view()),
]


#  Operation User Working
urlpatterns+=[
    path('operation/create', OperationUserRegistration.as_view()),
    path('file', filesUploading.as_view()),
]




