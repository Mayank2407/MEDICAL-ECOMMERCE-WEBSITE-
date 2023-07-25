from django.shortcuts import render
from . import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt

def Product_Interface(request):
    try:
        admin = request.session['ADMIN']
        return render(request, 'ProductInterface.html')
    except:
        return render(request, 'AdminLogin.html')
@xframe_options_exempt

def Submit_Product(request):

    try:
        DB,CMD=pool.ConnectionPooling()

        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        brandid=request.POST['brandid']
        productname=request.POST['productname']
        price=request.POST['price']
        offerprice=request.POST['offerprice']
        packingtype=request.POST['packingtype']
        quantity=request.POST['quantity']
        rating=request.POST['rating']
        salestatus=request.POST['salestatus']
        status=request.POST['status']
        productimage=request.FILES['productimage']

        Q="insert into products(categoryid,subcategoryid,brandid,productname,price,offerprice,packingtype,status,salestatus,productimage,quantity,rating) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')".format(categoryid,subcategoryid,brandid,productname,price,offerprice,packingtype,status,salestatus,productimage,quantity,rating)
        print(Q)

        F = open("d:/medassist_ecom/assets/" + productimage.name, 'wb')
        for chunk in productimage.chunks():

         F.write(chunk)

        F.close()
        CMD.execute(Q)
        DB.commit()
        DB.close()
        return render(request, "ProductInterface.html", {'message': 'Product added successfully'})

    except Exception as e:
        print("error:",e)

        return render(request, "ProductInterface.html", {'message': 'Something went wrong'})
@xframe_options_exempt
def Display_All_Products(request):
    try:
        admin = request.session['ADMIN']
    except:
        return render(request, 'AdminLogin.html')
    try:
      DB,CMD=pool.ConnectionPooling()
      Q="select * from products"
      CMD.execute(Q)
      records=CMD.fetchall()

      DB.close()
      return render(request,'DisplayProducts.html',{'records':records})
    except Exception as e:
      print('Error:', e)
      return render(request,'DisplayProducts.html', {'records': None})
@xframe_options_exempt
def Edit_Products(request):
 try:
    DB,CMD=pool.ConnectionPooling()

    productid=request.GET['productid']
    categoryid=request.GET['categoryid']
    subcategoryid = request.GET['subcategoryid']
    brandid=request.GET['brandid']
    productname=request.GET['productname']
    packingtype=request.GET['packingtype']
    quantity=request.GET['quantity']
    price = request.GET['price']
    offerprice = request.GET['offerprice']
    rating = request.GET['rating']
    status = request.GET['status']

    Q = "update products set categoryid='{0}',subcategoryid='{1}',brandid='{2}',productname='{3}',packingtype='{4}',quantity='{5}',price='{6}',offerprice='{7}',rating='{8}',status='{9}' where productid='{10}'".format(categoryid, subcategoryid,brandid,productname,packingtype,quantity,price,offerprice,rating,status,productid)
    print(Q)
    CMD.execute(Q)
    DB.commit()
    DB.close()

    return JsonResponse({'result': True}, safe=False)

 except Exception as e:
     print("Error:",e)
     return JsonResponse({'result': False}, safe=False)
@xframe_options_exempt
def Delete_Products(request):
 try:
    DB,CMD=pool.ConnectionPooling()

    productid = request.GET['productid']

    Q = "delete from products where productid='{0}'".format(productid)
    print(Q)
    CMD.execute(Q)
    DB.commit()
    DB.close()

    return JsonResponse({'result': True}, safe=False)

 except Exception as e:
     print("Error:",e)
     return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def Edit_ProductIcon(request):
     try:
         DB, CMD = pool.ConnectionPooling()

         productid = request.POST['productid']
         producticon = request.FILES['producticon']
         Q = "update products set productimage='{0}' where productid={1}".format(producticon.name, productid)
         print(Q)
         F = open("d:/medassist_ecom/assets/" + producticon.name, 'wb')
         for chunk in producticon.chunks():
             F.write(chunk)
         F.close()

         CMD.execute(Q)
         DB.commit()
         DB.close()
         return JsonResponse({'result': True}, safe=False)
     except Exception as e:
         print("Error:", e)
         return JsonResponse({'result': False}, safe=False)
@xframe_options_exempt
def Images_Interface(request):
    try:
        admin = request.session['ADMIN']
    except:
        return render(request, 'AdminLogin.html')
    return render(request,"AddPictures.html")
@xframe_options_exempt
def Add_Picture(request):
    try:
        DB,CMD=pool.ConnectionPooling()
        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        brandid=request.POST['brandid']
        productid=request.POST['productid']
        productimage=request.FILES['productimage']
        Q="insert into pictures(categoryid,subcategoryid,brandid,productid,productimage) values('{0}','{1}','{2}','{3}','{4}')".format(categoryid,subcategoryid,brandid,productid,productimage)
        F = open("d:/medassist_ecomd/assets/" + productimage.name, 'wb')
        for chunk in productimage.chunks():
            F.write(chunk)
        F.close()
        CMD.execute(Q)
        DB.commit()
        DB.close()
        return render(request,"AddPictures.html",{'message':'Picture added '})
    except Exception as e:
        return render(request,"AddPictures.html",{'message':'Something wrong'})
@xframe_options_exempt
def Fetch_All_Product_Json(request):
    try:
        DB, CMD = pool.ConnectionPooling()
        subcategoryid=request.GET['subcategoryid']
        categoryid=request.GET['categoryid']
        brandid=request.GET['brandid']
        Q = "select * from products where categoryid={0} and subcategoryid={1} and brandid={2}".format(categoryid,subcategoryid,brandid)
        CMD.execute(Q)
        records = CMD.fetchall()
        DB.close()
        return JsonResponse({'data': records}, safe=False)
    except Exception as e:
        return JsonResponse({'data': None}, safe=False)