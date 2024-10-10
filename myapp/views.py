from django.shortcuts import render,redirect

# Create your views here.

from django.contrib.auth.models import User

from myapp.forms import TaskForm,RegistrationForm,SignInForm

from django.views.generic import View

from myapp.models import Task

from django.contrib import messages

from django import forms

from django.db.models import Q

from django.db.models import Count

from django.contrib.auth import authenticate,login,logout

from myapp.decorators import signin_required

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache


decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")
class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()

        return render(request,"task_create.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save()

            messages.success(request,"created suucessfully")

            return redirect("task_list")

        else:

            messages.error(request,"creation failed")

            return render(request,"task_create.html",{"form":form_instance})        


@method_decorator(decs,name="dispatch")
class TaskListView(View):

    def get(self,request,*args,**kwargs):



        search_text=request.GET.get("search_text")         

        selected_category=request.GET.get("category","all")

        if selected_category =="all":

            qs=Task.objects.filter(user=request.user)

        else:

            qs=Task.objects.filter(category=selected_category,user=request.user)    

        if search_text!=None:

            qs=Task.objects.filter(user=request.user)

            qs=Task.objects.filter(Q(title__icontains=search_text)|Q(description__contains=search_text))       

        return render(request,"task_list.html",{"tasks":qs,"selected":selected_category})                

       

@method_decorator(decs,name="dispatch")
class TaskDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Task.objects.get(id=id)

        return render(request,"task_detail.html",{"task":qs})    


@method_decorator(decs,name="dispatch")
class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        task_obj=Task.objects.get(id=id) 

        form_instance=TaskForm(instance=task_obj)

        # add status field to form instance  

        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs=
        {"class":"form-control form-select"}),initial=task_obj.status)

       
        return render(request,"task_update.html",{"form":form_instance})   


    # def post(self,request,*args,**kwargs):

    #     # extract id

    #     id=kwargs.get("pk")

    #     # initail form with request.POST

    #     form_instance=TaskForm(request.POST)     

    #     if form_instance.is_valid():

    #     # fetch valid data

    #         data=form_instance.cleaned_data

    #         status=request.POST.get("status")

    #         Task.objects.filter(id=id).update(**data,status=status)

    #         # form_instance.save()

    #         messages.success(request,"updated successfully")

    #         return redirect("task_list")

    #     else:

    #         messages.error(request,"update failed")

    #         return render(request,"task_list.html",{"form":form_instance})


    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        task_obj=Task.objects.get(id=id)

        form_instance=TaskForm(request.POST,instance=task_obj)

        if form_instance.is_valid():

            form_instance.instance.status=request.POST.get("status")

            form_instance.save()

            messages.success(request,"updated successfullyyyyy")

            return redirect("task_list")

        else:

            messages.error(request,"update failedddddd")

            return render(request,"task_update.html",{"form":form_instance})  


@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        Task.objects.get(id=kwargs.get("pk")).delete()

        messages.error(request,"deleted!!!!!!!!!")

        return redirect("task_list")


@method_decorator(decs,name="dispatch")
class TaskSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Task.objects.all()   

        total_task_count=qs.count()  

        category_summary=Task.objects.all().values("category").annotate(cat_count=Count("category"))

        print(category_summary)

        status_summary=Task.objects.all().values("status").annotate(stat_count=Count("status"))

        print(status_summary)

        context={

            "total_task_count":total_task_count,
            
            "category_summary":category_summary,

            "status_summary":status_summary

        }   

        return render(request,"dashboard.html",context)



class SignUpView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("login")   

        else:

            return render(request,self.template_name,{"form":form_instance})


class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance}) 

    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")    

            pswrd=form_instance.cleaned_data.get("password")

            user_obj=authenticate(request,username=uname,password=pswrd)

            if user_obj:

                login(request,user_obj)

                return redirect("task_list")

        return render(request,self.template_name,{"form":form_instance})  


@method_decorator(decs,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("login")              


class DashBoard(View):

    template_name="dashboard.html"

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)


                

                                



