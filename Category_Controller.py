from django.shortcuts import render
from . import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def Category_Interface(request):
  try:
    admin = request.session['ADMIN']
    return render(request,'CategoryInterface.html')
  except:
    return render(request,'AdminLogin.html')
@xframe_options_exempt
def Submit_Category(request):
  try:
    DB,CMD=pool.ConnectionPooling()
    categoryname=request.POST['categoryname']
    categoryicon=request.FILES['categoryicon']
    Q="insert into categories(categoryname,categoryicon)values('{0}','{1}')".format(categoryname,categoryicon)
    F=open("d:/medassist_ecom/assets/"+categoryicon.name,'wb')
    for chunk in categoryicon.chunks():
        F.write(chunk)
    F.close()
    CMD.execute(Q)
    DB.commit()
    DB.close()
    return render(request, 'CategoryInterface.html',{'message':'Record Submitted Succesfully'})
  except Exception as e:
    print("Error:",e)
    return render(request, 'CategoryInterface.html', {'message': 'Fail To Submit Record'})

@xframe_options_exempt
def Display_All_Category(request):
    try:
        admin = request.session['ADMIN']
    except:
        return render(request, 'AdminLogin.html')
    try:
      DB,CMD=pool.ConnectionPooling()
      Q="select * from categories"
      CMD.execute(Q)
      records=CMD.fetchall()
      print('Records:',records)
      DB.close()
      return render(request,'DisplayAllCategories.html',{'records': records})
    except Exception as e:
      print('Error:',e)
      return render(request,'DisplayAllCategories.html', {'records': None})
@xframe_options_exempt
def Edit_Category(request):
      try:
        DB, CMD = pool.ConnectionPooling()
        categoryname = request.GET['categoryname']
        categoryid = request.GET['categoryid']

        Q = "update categories set categoryname='{0}' where categoryid={1}".format(categoryname, categoryid)
        CMD.execute(Q)
        DB.commit()
        DB.close()
        return JsonResponse({'result':True},safe=False)
      except Exception as e:
        print("Error:", e)
        return JsonResponse({'result':False}, safe=False)

@xframe_options_exempt
def Delete_Category(request):
  try:
    DB, CMD = pool.ConnectionPooling()

    categoryid = request.GET['categoryid']

    Q="delete from categories where categoryid={0}".format(categoryid)
    CMD.execute(Q)
    DB.commit()
    DB.close()
    return JsonResponse({'result': True}, safe=False)
  except Exception as e:
    print("Error:", e)
    return JsonResponse({'result': False}, safe=False)
@xframe_options_exempt
def Edit_CategoryIcon(request):
    try:
      DB, CMD = pool.ConnectionPooling()
      categoryid = request.POST['categoryid']
      categoryicon = request.FILES['categoryicon']


      Q = "update categories set categoryicon='{0}' where categoryid={1}".format(categoryicon.name,categoryid)
      F = open("d:/medassist_ecom/assets/" + categoryicon.name, 'wb')
      for chunk in categoryicon.chunks():
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
def Fetch_All_Category_JSON(request):
  try:
    DB, CMD = pool.ConnectionPooling()
    Q = "select * from categories"
    CMD.execute(Q)
    records = CMD.fetchall()
    print('RECORDS:', records)
    DB.close()
    return JsonResponse({'data': records}, safe=False)
  except Exception as e:
    print('Error:', e)
    return render(request, 'DisplayAllCategories.html', {{'data': None}})