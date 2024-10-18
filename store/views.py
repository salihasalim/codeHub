from django.shortcuts import render,redirect

from store.forms import SignUpform

from django.views.generic import View





class SignUpView(View):

    template_name="register.html"

    form_class=SignUpform

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})


    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("signup")
        else:
            return render(request,self.template_name,{"form":form_instance})
