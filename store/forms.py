from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from store.models import UserProfile,Project


class SignUpform(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","password1","password2"]

        widgets={

            "username":forms.TextInput(attrs={"class":"form-control","style":"width:350px;height:40px;margin-bottom:40px;"}),

            "email":forms.TextInput(attrs={"class":"form-control","style":"width:350px;height:40px;margin-bottom:40px;"}),

            "password1":forms.PasswordInput(attrs={"class":"form-control","style":"width:350px;height:40px;margin-bottom:40px;"}),

            "password2":forms.PasswordInput(attrs={"class":"form-control","style":"width:350px;height:40px;margin-bottom:40px;"})
        }




class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","style":"width:300px;height:40px;margin-bottom:30px;"}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","style":"width:300px;height:40px;margin-bottom:20px;"}))


class UserProfileForm(forms.ModelForm):

    class Meta:

        model=UserProfile

        fields=["bio","profile_picture","phone"]

        widgets={

            "bio":forms.TextInput(attrs={"class":"form-control","style":"width:350px;height:40px;margin-bottom:40px;"}),

            "profile_picture":forms.FileInput(attrs={"class":"form-control","style":"width:350px;height:40px;margin-bottom:40px;"}),

            "phone":forms.NumberInput(attrs={"class":"form-control","style":"width:350px;height:40px;margin-bottom:40px;"})

        }


class ProjectForm(forms.ModelForm):

    class Meta:

        model=Project

        fields=["title","description","preview_image",
                 
                 "price","files","tag_objects","thumbnail"
                 ]



class PasswordResetForm(forms.Form):

    username=forms.CharField()

    email=forms.CharField()

    password1=forms.CharField()

    password2=forms.CharField()
     