from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Product,Wishlist,Cart
import requests
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'


def validate_signup(request):
    email=request.GET.get('email')
    data={
        'is_taken':User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


@csrf_exempt
def create_checkout_session(request):
    amount = int(json.load(request)['amount'])
    final_amount=amount*100
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Checkout Session Data',
                    },
                'unit_amount': final_amount,
                },
            'quantity': 1,
            }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success.html',
        cancel_url=YOUR_DOMAIN + '/cancel.html',)
    return JsonResponse({'id': session.id})

def success(request):
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(buyer=user,payment_status=False)
    for i in carts:
        i.payment_status=True
        i.save()
    carts=Cart.objects.filter(buyer=user,payment_status=False)
    request.session['cart_count']=len(carts)
    return render(request,'myapp/success.html')

def cancel(request):
    return render(request,'myapp/cancel.html')

def index(request):
    try:
        e = User.objects.get(email=request.session['email'])
        if e.usertype=="Buyer":
            return render(request,"myapp/index.html")
        else:
            return render(request,"myapp/sindex.html")
    except:
        return render(request,"myapp/index.html")

def sindex(request):
    return render(request,"myapp/sindex.html")

def home2(request):
    return render(request,"myapp/home-02.html")

def home3(request):
    return render(request,"myapp/home-03.html")

def about(request):
    return render(request,"myapp/about.html")

def blog(request):
    return render(request,"myapp/blog.html")

def product(request):
    products=Product.objects.all()
    return render(request,"myapp/product.html",{'products':products})

def shopingcart(request):
    return render(request,"myapp/shoping-cart.html")

def contact(request):
    return render(request,"myapp/contact.html")

def blogdetail(request):
    return render(request,"myapp/blod-detail.html")

def productdetail(request):
    return render(request,"myapp/product-detail.html")

def login(request):
    if request.method=="POST":
        try: 
            e = User.objects.get(email = request.POST['email'])
            if e.password==request.POST['password']:
                if e.usertype == "buyer":
                    request.session['email'] = e.email
                    request.session['firstname'] = e.firstname
                    request.session['profile_picture'] = e.profile_picture.url
                    wishlists=Wishlist.objects.filter(buyer=e)
                    request.session['wishlists_count']=len(wishlists)
                    carts=Cart.objects.filter(buyer=e,payment_status=False)
                    request.session['carts_count']=len(carts)
                    msg = "Login Successfully"
                    return render(request,'myapp/index.html',{'msg' : msg})
                else:
                    request.session['email'] = e.email
                    request.session['firstname'] = e.firstname
                    request.session['profile_picture'] = e.profile_picture.url
                    
                    msg = "Login Successfully"
                    return render(request,'myapp/sindex.html',{'msg' : msg}) 
            else:
                   msg = "Your Password is Incorrect"
                   return render(request,'myapp/login.html',{'msg' : msg})
        except:
              msg = "Your Email is not registered"
              return render(request,'myapp/signup.html',{'msg' : msg})     
                  
    else:
        return render(request,"myapp/login.html")
            
def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = "Youe email is already registered."
            return render(request,'myapp/signup.html',{'msg' : msg})
        
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    usertype = request.POST['usertype'],
                    email = request.POST['email'],
                    firstname = request.POST['firstname'],
                    lastname = request.POST['lastname'],
                    mobile = request.POST['mobile'],
                    password = request.POST['password'],
                    profile_picture = request.FILES['profile_picture']
                )
                msg = "Signed Up Successfully"
                return render(request,'myapp/login.html',{'msg':msg})
            else:
                msg = "Password and Current Password did not match."
                return render(request,'myapp/signup.html',{'msg':msg})
    else:
        return render(request,'myapp/signup.html')
    
def logout(request):
    email = request.session['email']
    e = User.objects.get(email = email)
    try:
        del request.session['email']
        del request.session['firstname']
        del request.session['profile_picture']
        del request.session['wishlists_count']
        del request.session['carts_count']
        return render (request,"myapp/login.html")
    except:
        if e.usertype == "Buyer":
            return render(request,"myapp/index.html")
        else:
            return render(request,"myapp/sindex.html")
    
def forgotpassword(request):
     if request.method=="POST":
          try:
               otp = random.randint(1000,9999)
               e = User.objects.get(mobile=request.POST['mobile'])
               mobile = request.POST['mobile']

               url = "https://www.fast2sms.com/dev/bulkV2"

               querystring = {"authorization":"EM5TxhCfzI9UyJ80Nijw7soGmOrVaAbtQ3nFZeRYqdB2KgWv61ikQ0M538obtfGCvKAlR7xrVXF6mOY9","variables_values":str(otp),"route":"otp","numbers":str(mobile)}

               headers = {
                    'cache-control': "no-cache"
                         }

               response = requests.request("GET", url, headers=headers, params=querystring)
               print(response.text)
               request.session['mobile']=mobile
               request.session['otp']=otp

               return render (request,"myapp/verifyotp.html")
                 
          except:
               msg = "Invalid Mobile Number!!"
               return render(request,'myapp/forgotpassword.html',{'msg':msg})
     else:     
        return render (request,"myapp/forgotpassword.html")

def verifyotp(request):
     otp = int(request.session['otp'])
     uotp = int(request.POST['uotp'])
    
     if otp==uotp:
          del request.session['otp']
          return render(request,'myapp/newpass.html')
     else:
          msg = "Invalid Otp!!"
          return render (request,"myapp/forgotpassword.html",{'msg' : msg})
     
def newpass(request):
    if request.method =="POST":
        if request.POST['newpassword']==request.POST['cpassword']:
            mobile = request.session['mobile']
            e=User.objects.get(mobile=mobile)
            e.password=request.POST['newpassword']
            e.save()
            msg = "Password Updated successfully"
            return render(request,"myapp/login.html",{'msg':msg})
        else:
            msg = "Your password and current password did not match"
            return render(request,"myapp/newpass.html",{'msg':msg})
    else:
        return render(request,"myapp/newpass.html")

def changepass(request):
    email = request.session['email']
    e = User.objects.get(email = email)
    if request.method=="POST":
        if e.password==request.POST['oldpassword']:
            print("first if")
            if request.POST['newpassword']==request.POST['cpassword']:
                
                e.password = request.POST['newpassword']
                e.save()
                msg = "Password Updated Successfully!!"
                return redirect(logout)

            else:
                
                msg = "New Password and Confirm new password does not match"
                if e.usertype=="Buyer":
                    return render(request,"myapp/changepass.html",{'msg':msg})
                else:
                    return render(request,"myapp/spass.html",{'msg':msg})
        else:
            msg="Old Password Is Incorrect"
            if e.usertype=="Buyer":
                return render(request,"myapp/changepass.html",{'msg':msg})
            else:
                return render(request,"myapp/spass.html",{'msg':msg})
                                
    else:
        
        if e.usertype=="Buyer":
            return render(request,"myapp/changepass.html")          
        else:
            return render(request,"myapp/spass.html")
    
def profileupdate(request):
    if request.method=="POST":
            e = User.objects.get(email=request.session['email'])   
            e.firstname = request.POST['firstname']
            e.lastname = request.POST['lastname']
            e.email = request.POST['email']
            e.mobile = request.POST['mobile']
            try:
                e.profile_picture = request.FILES['profile_picture']
                e.save()
            
            except:
                pass

            e.save()
            request.session['profile_picture'] = e.profile_picture.url
            msg = "Profile Updated Successfully"
            if e.usertype == "Buyer":
                return render (request,"myapp/index.html",{'msg' : msg})
            else:
                return render(request,"myapp/sindex.html",{'msg':msg})
    else:
        e = User.objects.get(email=request.session['email'])
        if e.usertype == "Buyer":
            return render(request,'myapp/profileupdate.html',{'e':e})
        else:
            return render(request,"myapp/sprofile.html",{'e':e})

def sadd(request):
     seller = User.objects.get(email = request.session['email'])
     if request.method=="POST":
          try:
               Product.objects.create(
                    seller = seller,
                    cname = request.POST['cname'],
                    bname = request.POST['bname'],
                    pname = request.POST['pname'],
                    si = request.POST['si'],
                    price = request.POST['price'],
                    desc = request.POST['desc'],
                    pimage = request.FILES['pimage'],
               )
               msg = "Product Added Sucesffully!!"
               return render(request,'myapp/sadd.html',{'msg':msg})
          
          except:
               return render(request,"myapp/index.html")
     else:
          return render(request,'myapp/sadd.html')
     
def sview(request):
    seller = User.objects.get(email=request.session['email'])
    Products = Product.objects.filter(seller = seller)
    return render(request,"myapp/sview.html",{'Products':Products})

def pdetail(request,pk):
    Products = Product.objects.get(pk=pk)
    return render(request,"myapp/product-detail.html",{'Products':Products})

def sedit(request,pk):
    Products = Product.objects.get(pk=pk)
    if request.method=="POST":
            Products.cname = request.POST['cname']
            Products.pname = request.POST['pname']
            Products.bname = request.POST['bname']
            Products.si = request.POST['si']
            Products.si = request.POST['desc']
            try:
                Products.pimage = request.FILES['pimage']
                
            except:
                pass

            Products.save()
            msg = "Changed Successfully"
            return render(request,"myapp/sview.html",{'Products':Products},{'msg':msg})
    else:
        return render(request,"myapp/sedit.html",{'Products':Products})

def sdelete(request,pk):
    Products = Product.objects.get(pk=pk)
    Products.delete()
    msg = "Product deleted successfully"
    return render(request,"myapp/sview.html",{'msg':msg})

def buyer_product_detail(request,pk):
    wishlist_flag=False
    cart_flag=False
    product=Product.objects.get(pk=pk)
    buyer=User.objects.get(email=request.session['email'])
    try:
        Wishlist.objects.get(product=product,buyer=buyer)
        wishlist_flag=True
    except:
        pass
    try:
        Cart.objects.get(product=product,buyer=buyer,payment_status=False)
        cart_flag=True
    except:
        pass
    return render(request,'myapp/buyer-product-detail.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def add_to_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    buyer=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(buyer=buyer,product=product)
    return redirect('wishlist')

def wishlist(request):
    buyer=User.objects.get(email=request.session['email'])
    wishlists=Wishlist.objects.filter(buyer=buyer)
    request.session['wishlists_count']=len(wishlists)
    return render(request,'myapp/wishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    buyer=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.get(product=product,buyer=buyer)
    wishlist.delete()
    return redirect('wishlist')

def add_to_cart(request,pk):
    product=Product.objects.get(pk=pk)
    buyer=User.objects.get(email=request.session['email'])
    Cart.objects.create(
        buyer=buyer,
        product=product,
        product_price=product.price,
        product_qty=1,
        total_price=product.price,
        payment_status=False
        )
    return redirect('cart')

def cart(request):
    net_price=0
    buyer=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(buyer=buyer,payment_status=False)
    request.session['carts_count']=len(carts)
    for i in carts:
        net_price=net_price+i.total_price
    return render(request,'myapp/cart.html',{'carts':carts,'net_price':net_price})

def remove_from_cart(request,pk):
    product=Product.objects.get(pk=pk)
    buyer=User.objects.get(email=request.session['email'])
    cart=Cart.objects.get(product=product,buyer=buyer)
    cart.delete()
    return redirect('cart')

def change_qty(request,pk):
    cart=Cart.objects.get(pk=pk)
    product_qty=int(request.POST['product_qty'])
    total_price=cart.product_price*product_qty
    cart.total_price=total_price
    cart.product_qty=product_qty
    cart.save()
    return redirect('cart')