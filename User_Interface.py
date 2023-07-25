from django.shortcuts import render
from . import pool
from django.http import JsonResponse
import json
from urllib.parse import unquote

def Index(request):
    return render(request ,"Index.html")

def Add_To_Cart(request):
    try:
     product=request.GET['product']
     qty = request.GET['qty']
     product = product.replace("'", "\"")
     product = json.loads(product)
     product['qty'] = qty
     print('UPDATED PRODUCTS:', product)

     # create cart container using Session Management
     try:
         Cart_Container = request.session['Cart_Container']
         Cart_Container[str(product['productid'])] = product
         request.session['Cart_Container'] = Cart_Container
     except:
         Cart_Container={}
         Cart_Container[str(product['productid'])] = product
         request.session['Cart_Container'] = Cart_Container

     print("Cart_Container:",Cart_Container)
     Cart_Container = str(Cart_Container).replace("'", "\"")

     return JsonResponse({'data': Cart_Container}, safe=False)

    except Exception as error:
        print("Eroooorrrrrrr:",error)
        return JsonResponse({'data': []}, safe=False)

def Fetch_Cart(request):
    try:
     try:
       Cart_Container=request.session['Cart_Container']

     except:
       Cart_Container={}

     print("Cart_Container:",Cart_Container)
     Cart_Container = str(Cart_Container).replace("'", "\"")

     return JsonResponse({'data': Cart_Container}, safe=False)
    except Exception as err:
        print("ERRORRRRR:",err)
        return JsonResponse({'data': []}, safe=False)

def RemoveFromCart(request):
    try:
       productid = request.GET['productid']

       Cart_Container=request.session['Cart_Container']
       del Cart_Container[productid]
       request.session['Cart_Container']=Cart_Container
       print("Remove Cart_Container:",Cart_Container)
       Cart_Container = str(Cart_Container).replace("'", "\"")
       return JsonResponse({'data': Cart_Container}, safe=False)
    except Exception as err:
        print("ERRORRRRR:",err)
        return JsonResponse({'data': []}, safe=False)

def Shopping_Cart(request):
    try:
        try:
            Cart_Container = request.session['Cart_Container']
            total = 0
            totalprice = 0
            totalsavings = 0

            for key in Cart_Container.keys():
                amt = int(Cart_Container[key]['price']) - int(Cart_Container[key]['offerprice'])
                Cart_Container[key]['save'] = amt * int(Cart_Container[key]['qty'])
                totalsavings += Cart_Container[key]['save']
                Cart_Container[key]['productprice'] = int(Cart_Container[key]['offerprice']) * int(Cart_Container[key]['qty'])
                total+= int(Cart_Container[key]['offerprice']) * int(Cart_Container[key]['qty'])
                totalprice+= int(Cart_Container[key]['price']) * int(Cart_Container[key]['qty'])

        except Exception as err:
            Cart_Container = {}
            print("Errrrrrrrorrrrrrrrrrrrrrrrrrrrrrr", err)

        print("My Shopping Cart_Container:", Cart_Container.values())
        # CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")

        return render(request, "Cart.html", {'data': Cart_Container.values(), 'totalamount': total, 'totalproducts': len(Cart_Container.keys()), 'totalprice': totalprice, 'totalsavings': totalsavings})

    except Exception as err:
        print("ERRORRRRR:", err)
        return render(request, "Cart.html", {'data': {}})


def Products_Buy(request):
    product=unquote(request.GET['product'])
    product=json.loads(product)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", product)
    DB, CMD = pool.ConnectionPooling()
    Q = "select * from pictures where productid={0}".format(product['productid'])
    CMD.execute(Q)
    pictures = CMD.fetchall()
    DB.close()
    return render(request, "Products_Buy.html", {'product': product,'pictures':pictures})


def Fetch_All_Products(request):
    try:
        admin = request.session['ADMIN']
    except:
        return render(request, 'AdminLogin.html')

    try:
      DB,CMD=pool.ConnectionPooling()
      Q= "select p.*,(select c.categoryname from categories c where c.categoryid=p.categoryid) as cname,(select s.subcategoryname from subcategories s where p.subcategoryid=s.subcategoryid) as scname,(select b.brandname from brands b where p.brandid=b.brandid) as bname from products p"
      CMD.execute(Q)
      products=CMD.fetchall()
      print(products)
      DB.close()
      return JsonResponse({'data': products}, safe=False)
    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)

def Fetch_All_Category_JSON(request):
    try:
      DB,CMD=pool.ConnectionPooling( )
      Q="select * from categories"
      CMD.execute(Q)
      records=CMD.fetchall()
      print('Records:',records)
      DB.close()
      return JsonResponse({'data': records}, safe=False)
    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)

def Fetch_All_SubCategory_JSON(request):
    try:
      DB, CMD = pool.ConnectionPooling()
      Q = "select * from subcategories"
      CMD.execute(Q)
      records = CMD.fetchall()
      print('Records:', records)
      DB.close()
      return JsonResponse({'data': records}, safe=False)
    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)

def CheckUserMobileno(request):
    mobileno=request.GET['mobileno']
    try:
      DB, CMD = pool.ConnectionPooling()
      Q = "select * from  users where mobileno='{0}'".format(mobileno)
      CMD.execute(Q)
      record = CMD.fetchone()
      print('User:', record)
      if(record):
          return JsonResponse({'data': record,'status':True}, safe=False)
      else:
          return JsonResponse({'data':[], 'status': False}, safe=False)
      DB.close()

    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)

def  InsertUser(request):
    mobileno=request.GET['mobileno']
    emailid = request.GET['emailid']
    firstname = request.GET['firstname']
    lastname = request.GET['lastname']
    password = request.GET['password']
    try:
      DB, CMD = pool.ConnectionPooling()
      Q = "insert into users values('{0}','{1}','{2}','{3}','{4}')".format(emailid,mobileno,firstname,lastname,password)
      CMD.execute(Q)
      DB.commit()
      DB.close()
      return JsonResponse({'status':True}, safe=False)


    except Exception as e:
      print('Error:', e)
      return JsonResponse({'status':False}, safe=False)

def  CheckUserMobilenoForAddress(request):
    mobileno=request.GET['mobileno']
    try:
      DB, CMD = pool.ConnectionPooling()
      Q = "select UA.*,(select U.firstname from users U where U.mobileno=UA.mobileno) as firstname,(select U.lastname from users U where U.mobileno=UA.mobileno) as lastname  from  users_address UA where UA.mobileno='{0}'".format(mobileno)
      CMD.execute(Q)
      record = CMD.fetchone()
      print('User:', record)
      if(record):
          return JsonResponse({'data': record,'status':True}, safe=False)
      else:
          return JsonResponse({'data':[], 'status': False}, safe=False)
      DB.close()

    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)

def InsertUserAddress(request):
    mobileno=request.GET['mobileno']
    emailid = request.GET['emailid']
    addressone = request.GET['addressone']
    addresstwo = request.GET['addresstwo']
    landmark = request.GET['landmark']
    city = request.GET['city']
    state = request.GET['state']
    zipcode = request.GET['zipcode']
    try:
      DB, CMD = pool.ConnectionPooling()
      Q = "insert into users_address(mobileno, emailid, address1, address2, landmark, city, state, zipcode) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(mobileno,emailid,addressone,addresstwo,landmark,city,state,zipcode)
      print(Q)
      CMD.execute(Q)
      DB.commit()
      DB.close()
      return JsonResponse({'status':True}, safe=False)
    except Exception as e:
      print('Error:', e)
      return JsonResponse({'status':False}, safe=False)