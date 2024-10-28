from django.shortcuts import render,redirect

from store.forms import SignUpform,SignInForm

from django.views.generic import View,FormView,CreateView,TemplateView

from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login,logout

from store.forms import UserProfileForm,ProjectForm

from store.models import Project





class SignUpView(CreateView):

    template_name="register.html"

    form_class=SignUpform


    success_url=reverse_lazy("signin")

    # createview create cheyyan use cheyyunnu ath koduthal get post kodukanam
    # def get(self,request,*args,**kwargs):

    #     form_instance=self.form_class()

    #     return render(request,self.template_name,{"form":form_instance})


    # def post(self,request,*args,**kwargs):

    #     form_instance=self.form_class(request.POST)

    #     if form_instance.is_valid():

    #         form_instance.save()

    #         return redirect("signup")
    #     else:
    #         return render(request,self.template_name,{"form":form_instance})





# login

# formview-oru form ine html page il render cheyyikan use cheyyunnu.formview koduthal get function venda,athupole template ne render cheyyikan templateview ise cheyyam

class signInView(FormView):

    template_name="login.html"

    form_class=SignInForm



    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("index")
        return render(request,self.template_name,{"form":form_instance})


class IndexView(View):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.all().exclude(developer=request.user)

        return render(request,self.template_name,{"data":qs})


class LogOutView(View):

    def get (self,request,*args,**kwargs):

        logout(request)
        return redirect("signin")

# def logout_view(request,*args,**kwargs):

#     logout(request)

#     return redirect("signin")

class UserProfileEditView(View):
    
    template_name="profile-edit.html"

    form_class=UserProfileForm

    def get(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(instance=user_profile_instance)

        return render(request,self.template_name,{"form":form_instance})


    def post(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(request.POST,instance=user_profile_instance,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")

        return render(request,self.template_name,{"form":form_instance})




class ProjectCreateView(View):

    template_name="project_add.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.developer=request.user

            form_instance.save()

            return redirect("index")

        return render(request,self.template_name,{"form":form_instance})



class MyProjectListView(View):

    template_name="my_project.html"


    def get (self,request,*args,**kwargs):

        qs=Project.objects.filter(developer=request.user)

        return render(request,self.template_name,{"data":qs})



class ProjectUpdateView(View):

    template_name="project_update.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=Project.objects.get(id=id)

        form_instance=self.form_class(instance=project_object)

        return render(request,self.template_name,{"form":form_instance})


    def post(self,request,*args,**kwargs):


        id=kwargs.get("pk")

        project_object=Project.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=project_object,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()
            
            return redirect("my_work")

        return render(request,self.template_name,{"form":form_instance})



class ProductDetailView(View):

    template_name="project_detail.html"

    def get(self,request,*args,**kwargs):
        

        id=kwargs.get("pk")

        
        qs=Project.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})

        
