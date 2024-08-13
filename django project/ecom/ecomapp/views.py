from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Cart,Order
from django.db.models import Q #it is used for complex queries
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout 
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.

def home(request):
    # products = Product.objects.all() #fetch all products from db,models
    products = Product.objects.filter(is_active=True)
    context = {}
    context['products']=products
 
       
    # print(context['products'])
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")

def service(request):
    return render(request,"service.html")

def productdetail(request,pid):
    context = {}
    product = Product.objects.get(id = pid)
    context['product'] = product
    return render(request,"product_detail.html",context)

def catfilter(request,cid):
    context={}
    q1=Q(is_active=True)
    q2=Q(category=cid)
    product=Product.objects.filter(q1&q2)
    context['products']=product
    return render(request,"index.html",context)

def sortbyprice(request,s):
    context={}
    if s == '0':
        products  = Product.objects.filter(is_active=True).order_by('-price')
        context['products']=products
        return render(request,"index.html",context)
    else:
        products  = Product.objects.filter(is_active=True).order_by('price')
        context['products']=products
        return render(request,"index.html",context)

def pricerange(request):
    context={}
    if request.method == "GET":
        return render(request,"index.html",context)
    else:
        min = request.POST['min']
        max = request.POST['max']
        # products = Product.objects.filter(price_range=(min,max))  
        products = Product.objects.filter(is_active=True,price__gte=min,price__lte=max)  
        context['products']=products 
        return render(request,"index.html",context)


def search(request):
    """
    Handle search requests
    """
    context = {}
    query = request.GET.get('query')
    context['query'] = query
    if query:
        results = Product.objects.filter(Q(name__icontains=query) | Q(pdetails__icontains=query))
        context['results'] = results
        return render(request, 'search.html', context)
    else:
        results = Product.objects.none()
        return render(request, 'search.html', context)



#user accounts

def register(request):
    context={}
    if(request.method=="GET"):
        return render(request,"registration.html",context)  
    else:
        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        if(uname == '' or upass== '' or ucpass== ''):
            context['error'] = "Please fill all the fields"
        elif(upass!=ucpass):
            context['error'] = "Passwords do not match"
        elif uname in [user.username for user in User.objects.all()]:
            context['error'] = "User already exists"
            
        else:
            user_obj = User.objects.create(username=uname,password=upass,email=uname)
            user_obj.set_password(upass)
            user_obj.save()
            context['success'] = "User created successfully"

        return render(request,"registration.html",context)


def user_login(request):
    context = {}
    if(request.method=="GET"):
        return render(request,"login.html")
    else:
        uname = request.POST['uname']
        upass = request.POST['upass']
        if uname=='' or upass=='':
            context['error'] = "Please fill all the fields"
        else:
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                context['success'] = "Login successful"
                return redirect('/')
            else:
                context['error'] = "Invalid credentials"
            print(user)
        return render(request,'login.html',context)
    
# def user_login(request):
#     context={}
#     if (request.method=="GET"):
#         return render(request,"login.html")
#     else:     
#         uname = request.POST['uname']
#         upass = request.POST['upass']
#         if uname=="" or upass=="":
#             context['error']="Please fill all the fields"
#         else:
#             u=authenticate(username=uname,password=upass)
#             if u is not None:
#                 login(request,u)
#                 return redirect("/")
#             else:
#                 context['error']="Invalid credentials"
#         return render(request,"login.html",context)

def user_logout(request):
    logout(request)
    return redirect("/")


def addtocart(request,pid):
    if request.user.is_authenticated:
        uid  =request.user.id
        u=User.objects.get(id=uid)
        p=Product.objects.get(id=pid)
        c=Cart.objects.create(uid=u,pid=p) 
        c.save()
        return redirect('/')
    else:
        return redirect('/login')
    
    

def viewcart(request):
    if request.user.is_authenticated:
        context={}
        user_id= request.user.id
        c=Cart.objects.filter(uid=user_id)
        context['product']=c
        np = len(c)
        context['np']=np
    
    # total_price = sum(item.pid.price for item in c) #expression 

        total_price = 0 
        for item in c:
            total_price += item.pid.price * item.quantity
        context['total_price'] = total_price
        return render(request,"cart.html",context)
    else:
        return redirect('/login')

def removefromcart(request,cid):
    if request.user.is_authenticated:
        c=Cart.objects.get(id=cid)
        c.delete()
        return redirect('/viewcart')
    else:
        return redirect('/login')

def updateqty(request,cid,qv):
    if request.user.is_authenticated:
        c=Cart.objects.filter(id=cid)
        if qv=="1":
            t=c[0].quantity+1
            c.update(quantity=t)
            return redirect('/viewcart')  
        elif qv=="0":
            if c[0].quantity>1:
                t=c[0].quantity-1
                c.update(quantity=t)
            elif c[0].quantity==1:
                c.delete()
            return redirect('/viewcart')
    else:
        return redirect('/login')
    
def placeorder(request):
    if request.user.is_authenticated:
        context={}
        user = request.user
        c=Cart.objects.filter(uid=user)
        order_id = random.randrange(1000,9999)
        for item in c:
            o = Order.objects.create(order_id=order_id,uid=user, pid=item.pid, quantity=item.quantity)
            o.save()
            item.delete()
        o = Order.objects.filter(uid=user)   
        context['orders'] = o
        np = len(o)
        context['np']=np

        total_price = 0 
        for item in o:
            total_price += item.pid.price * item.quantity
        context['total_price'] = total_price
        return render(request,"order.html",context)
    else:
        return redirect('/login')

def makepayment(request):
    if request.user.is_authenticated:
        context={}
        o = Order.objects.filter(uid=  request.user.id  )  
        sum  = 0
        for item in o:
            sum += item.pid.price * item.quantity
            oid = item.order_id
        context['sum'] = sum*100

        client = razorpay.Client(auth=("rzp_test_2UCjdkrx0GhGju", "MxPdCoifEFQUxQXOTTn7Isr6"))
        data = { "amount": 500, "currency": "INR", "receipt": "oid" }
        payment = client.order.create(data=data)
        print(payment)
        c =Cart.objects.filter(uid=request.user)
        c.delete()
        o.delete()
        return render(request,"pay.html",context)
    

def senduseremail(request):
    send_mail(
        "Ekart Order",
        "Order placed successfully",
        "dalvisiddhesh3@gmail.com",
        ["dalvisiddhesh3@gmail.com"],
        fail_silently=False,
    )
    return redirect("/")

# lifl xbtv kilp ijxk    - pass key
    

 