from django.shortcuts import render,redirect,get_object_or_404

from store.forms import SignUpform,SignInForm,PasswordResetForm

from django.views.generic import View,FormView,CreateView,TemplateView

from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login,logout

from store.forms import UserProfileForm,ProjectForm

from store.models import Project,WishListItem,Order

from django.contrib import messages

from django.db.models import Sum

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from django.core.mail import send_mail

from store.decorators import signin_required

from django.views.decorators.cache import never_cache

from django.contrib.auth.models import User

decs=[signin_required,never_cache]

from decouple import config



def send_email():
    
    send_mail(
    "codesphere project download",
    "you are successfully download the project from codesphere",
    "salishamnas215@gmail.com",
    ["peacewithquran07@gmail.com"],
    # [request.user.email]
    fail_silently=False,
)

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

@method_decorator(decs,name="dispatch")
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

@method_decorator(decs,name="dispatch")

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



@method_decorator(decs,name="dispatch")
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


@method_decorator(decs,name="dispatch")
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


@method_decorator(decs,name="dispatch")
class ProductDetailView(View):

    template_name="project_detail.html"

    def get(self,request,*args,**kwargs):
        

        id=kwargs.get("pk")

        
        qs=Project.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})

@method_decorator(decs,name="dispatch")
class AddToWishlistItemView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=get_object_or_404(Project,id=id)

        try:

            request.user.basket.basket_item.create(project_object=project_object)

            messages.success(request,"item has benn added to wishlist")
        
        except Exception as e:

            messages.error(request,"failed to add item ")


        return redirect("index")

@method_decorator(decs,name="dispatch")
class MyWishListItemsView(View):

    template_name="mywishlist.html"

    def get(self,request,*args,**kwargs):

       
        qs=request.user.basket.basket_item.filter(is_order_placed=False)

        total=qs.values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        print("totalll",total)           


        return render(request,self.template_name,{"data":qs,"total":total})

@method_decorator(decs,name="dispatch")
class WishListItemDeleteView(View):

        def get(self,request,*args,**kwargs):

            id=kwargs.get("pk")

            WishListItem.objects.get(id=id).delete()

            return redirect("my_wishlist")

import razorpay
@method_decorator(decs,name="dispatch")
class CheckOutView(View):

    template_name="checkout.html"

    def get(self,request,*args,**kwargs):

        # step1: razorpay authentication

        KEY_ID=config('KEY_ID')   
        KEY_SECRET=config('KEY_SECRET')

        # authenticate

        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        amount=request.user.basket.basket_item.filter(is_order_placed=False).values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        data={"amount":amount*100, "currency": "INR", "receipt": "order_rcptid_codesphere"}
        
        payment=client.order.create(data=data)

        order_id=payment.get("id")

        order_object=Order.objects.create(order_id=order_id,customer=request.user)

        wishlist_items=request.user.basket.basket_item.filter(is_order_placed=False)

        for wi in wishlist_items:

            order_object.wishlist_item_objects.add(wi)

            wi.is_order_placed=True

            wi.save()



        return render(request,self.template_name,{"key_id":KEY_ID,"amount":amount,"order_id":order_id})




@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)
        KEY_ID=config('KEY_ID')

        KEY_SECRET=config('KEY_SECRET')

        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        try:
            client.utility.verify_payment_signature(request.POST)
            print("success")
            order_id=request.POST.get("razorpay_order_id")

            Order.objects.filter(order_id=order_id).update(is_paid=True)
            send_email()

        except:
            print("failed")

        
        return redirect("orders")


@method_decorator(decs,name="dispatch")
class MyOrdersView(View):

    template_name="myorders.html"

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(customer=request.user)

        return render(request,self.template_name,{"data":qs})




class PasswordResetView(View):

    template_name="password_reset.html"

    form_class=PasswordResetForm


    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            username=form_instance.cleaned_data.get("username")

            email=form_instance.cleaned_data.get("email")

            password1=form_instance.cleaned_data.get("password1")

            password2=form_instance.cleaned_data.get("password2")

            print(username,email,password1,password2)

            try:
                assert password1==password2, "password mismatch"

                user_object=User.objects.get(username=username,email=email)

                user_object.set_password(password2)

                user_object.save()

                return redirect("signin")

            except Exception as e:

                messages.error(request,f"(e)")

                return render(request,self.template_name,{"form":form_instance})


        return render(request,self.template_name,{"form":form_instance})

        






