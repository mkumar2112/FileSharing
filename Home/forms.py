from click import Group
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClientUser, OperationUser

class ClientUserSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=20)
    # major = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_ClientUser = True
        if commit:
            user.save()
            ClientUser.objects.create(user=user)
            user.groups.add(Group.objects.get(name='ClientUsers'))
        return user

class OperationUserSignUpForm(UserCreationForm):
    # subject = forms.CharField(max_length=100)
    # department = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_OperationUser = True
        if commit:
            user.save()
            OperationUser.objects.create(user=user)
            user.groups.add(Group.objects.get(name='OperationUsers'))
        return user
