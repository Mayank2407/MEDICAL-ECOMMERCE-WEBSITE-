from django.shortcuts import render
from . import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt

def Brand_Interface(request):
    try:
        admin = request.session['ADMIN']
        return render(request, 'BrandInterface.html')
    except:
        return render(request, 'AdminLogin.html')


@xframe_options_exempt


def Submit_Brand(request):

    try:
        DB,CMD=pool.ConnectionPooling()

        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        brandname = request.POST['brandname']
        contactperson = request.POST['contactperson']
        mobileno = request.POST['mobileno']
        status = request.POST['status']
        brandicon = request.FILES['brandicon']

        Q ="insert into brands(categoryid,subcategoryid,brandname,contactperson,mobileno,logo,status) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(categoryid, subcategoryid, brandname, contactperson, mobileno, brandicon.name, status)
        print(Q)

        F = open("d:/medassist_ecom/assets/" + brandicon.name, 'wb')

        for chunk in brandicon.chunks():
            F.write(chunk)
        F.close()

        CMD.execute(Q)
        DB.commit()
        DB.close()
        return render(request, "BrandInterface.html", {'message': 'Brand added'})

    except Exception as e:
        print("Error:", e)
        return render(request, "BrandInterface.html", {'message': 'Not Added'})

@xframe_options_exempt


def Display_All_Brands(request):
    try:
        admin = request.session['ADMIN']
    except:
        return render(request, 'AdminLogin.html')

    try:
      DB,CMD=pool.ConnectionPooling()
      Q="select * from brands"
      CMD.execute(Q)
      records=CMD.fetchall()

      DB.close()
      return render(request,'DisplayBrands.html',{'records':records})
    except Exception as e:
      print('Error:', e)
      return render(request,'DisplayBrands.html', {'records': None})

@xframe_options_exempt

def Edit_Brand(request):
 try:
    DB,CMD=pool.ConnectionPooling()
    brandid=request.GET['brandid']
    categoryid=request.GET['categoryid']
    subcategoryid = request.GET['subcategoryid']
    brandname=request.GET['brandname']
    contactperson=request.GET['contactperson']
    mobileno=request.GET['mobileno']
    #status = request.GET['status']

    Q = "update brands set categoryid='{0}',subcategoryid='{1}',brandname='{2}',contactperson='{3}',mobileno='{4}' where brandid='{5}'".format(categoryid, subcategoryid, brandname, contactperson, mobileno, brandid)
    print(Q)
    CMD.execute(Q)
    DB.commit()
    DB.close()

    return JsonResponse({'result': True}, safe=False)

 except Exception as e:
     print("Error:",e)
     return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt


def Delete_Brands(request):
 try:
    DB,CMD=pool.ConnectionPooling()

    brandid = request.GET['brandid']

    Q = "delete from brands where  brandid='{0}'".format(brandid)
    print(Q)
    CMD.execute(Q)
    DB.commit()
    DB.close()

    return JsonResponse({'result': True}, safe=False)

 except Exception as e:
     print("Error:",e)
     return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt


def Edit_logo(request):
     try:
         DB, CMD = pool.ConnectionPooling()

         brandid = request.POST['brandid']
         logo = request.FILES['logo']
         Q = "update brands set logo='{0}' where brandid={1}".format(logo.name, brandid)
         print(Q)
         F = open("D:/medassist_ecom/assets/" + logo.name, 'wb')
         for chunk in logo.chunks():
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

def Fetch_All_Brand_Json(request):
    try:
        DB, CMD = pool.ConnectionPooling()

        categoryid=request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        Q = "select * from brands where categoryid={0} and subcategoryid={1}".format(categoryid,subcategoryid)
        print(Q)
        CMD.execute(Q)
        records = CMD.fetchall()
        DB.close()

        return JsonResponse({'data': records}, safe=False)

    except Exception as e:
        print("Error:",e)
        return JsonResponse({'data': None}, safe=False)
