from django.shortcuts import render
from . import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def SubCategory_Interface(request):
  try:
    admin = request.session['ADMIN']
    return render(request, 'SubcategoryInterface.html')
  except:
    return render(request, 'AdminLogin.html')
@xframe_options_exempt
def Submit_SubCategory(request):
  try:
    DB,CMD=pool.ConnectionPooling()
    categoryid = request.POST['categoryid']
    subcategoryname=request.POST['subcategoryname']
    subcategoryicon=request.FILES['subcategoryicon']
    Q="insert into subcategories(categoryid,subcategoryname,subcategoryicon) values('{0}','{1}','{2}')".format(categoryid,subcategoryname,subcategoryicon.name)
    F=open("d:/medassist_ecom/assets/"+subcategoryicon.name,'wb')
    for chunk in subcategoryicon.chunks():
        F.write(chunk)
    F.close()
    CMD.execute(Q)
    DB.commit()
    DB.close()
    return render(request, 'SubcategoryInterface.html',{'message':'Record Submitted Succesfully'})
  except Exception as e:
    print("Error:",e)
    return render(request, 'SubcategoryInterface.html', {'message': 'Fail To Submit Record'})
@xframe_options_exempt
def Display_All_SubCategory(request):
    try:
        admin = request.session['ADMIN']
    except:
        return render(request, 'AdminLogin.html')
    try:
      DB,CMD=pool.ConnectionPooling()
      Q="select S.*,(select C.categoryname from categories C where C.categoryid=S.categoryid) as cname from subcategories S"
      CMD.execute(Q)
      records=CMD.fetchall()
      print('Records:',records)
      DB.close()
      return render(request,'DisplayAllSubcategories.html',{'records': records})
    except Exception as e:
      print('Error:',e)
      return render(request,'DisplayAllSubcategories.html', {'records': None})
@xframe_options_exempt
def Edit_SubCategory(request):
      try:
        DB, CMD = pool.ConnectionPooling()
        print(request.GET)
        categoryid=request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        subcategoryname = request.GET['subcategoryname']


        Q = "update subcategories set subcategoryname='{0}',categoryid='{1}' where subcategoryid='{2}'".format(subcategoryname,categoryid,subcategoryid)
        print(Q)
        CMD.execute(Q)
        DB.commit()
        DB.close()
        return JsonResponse({'result':True},safe=False)
      except Exception as e:
        print("Error:-------------------", e)
        return JsonResponse({'result':False}, safe=False)

@xframe_options_exempt
def Delete_SubCategory(request):
  try:
    DB, CMD = pool.ConnectionPooling()

    subcategoryid = request.GET['subcategoryid']

    Q="delete from subcategories where subcategoryid={0}".format(subcategoryid)
    CMD.execute(Q)
    DB.commit()
    DB.close()
    return JsonResponse({'result': True}, safe=False)
  except Exception as e:
    print("Error:", e)
    return JsonResponse({'result': False}, safe=False)
@xframe_options_exempt
def Edit_SubCategoryIcon(request):
    try:
      DB, CMD = pool.ConnectionPooling()
      subcategoryid = request.POST['subcategoryid']
      subcategoryicon = request.FILES['subcategoryicon']


      Q = "update subcategories set subcategoryicon='{0}' where subcategoryid='{1}'".format(subcategoryicon.name,subcategoryid)
      F = open("d:/medassist_ecom/assets/" + subcategoryicon.name, 'wb')
      for chunk in subcategoryicon.chunks():
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
def Fetch_All_Subcategory_JSON(request):
  try:
    DB, CMD = pool.ConnectionPooling()

    categoryid = request.GET['categoryid']
    # subcategoryid = request.GET['subcategoryid']
    Q = "select * from subcategories where categoryid='{0}'".format(categoryid)
    print(Q)
    CMD.execute(Q)
    records = CMD.fetchall()
    DB.close()

    return JsonResponse({'data': records}, safe=False)

  except Exception as e:
    print("Error:", e)
    return JsonResponse({'data': None}, safe=False)