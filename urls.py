"""majorproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import Category_Controller
from . import Subcategory_Controller
from . import Brand_Controller
from . import Product_Controller
from . import Admin_Controller
from . import User_Interface
urlpatterns = [
    path('admin/', admin.site.urls),
    path('categoryinterface/',Category_Controller.Category_Interface),
    path('submitcategory',Category_Controller.Submit_Category),
    path('displayallcategories/',Category_Controller.Display_All_Category),
    path('editcategory/',Category_Controller.Edit_Category),
    path('deletecategory/',Category_Controller.Delete_Category),
    path('editcategoryicon',Category_Controller.Edit_CategoryIcon),
    path('fetch_all_category_json',Category_Controller.Fetch_All_Category_JSON),
    path('subcategoryinterface/', Subcategory_Controller.SubCategory_Interface),
    path('submitsubcategory',Subcategory_Controller.Submit_SubCategory),
    path('displayallsubcategories/',Subcategory_Controller.Display_All_SubCategory),
    path('editsubcategory/',Subcategory_Controller.Edit_SubCategory),
    path('deletesubcategory/',Subcategory_Controller.Delete_SubCategory),
    path('editsubcategoryicon',Subcategory_Controller.Edit_SubCategoryIcon),
    path('brandinterface/', Brand_Controller.Brand_Interface),
    path('submitbrand', Brand_Controller.Submit_Brand),
    path('displaybrands/', Brand_Controller.Display_All_Brands),
    path('editbrands/',Brand_Controller.Edit_Brand),
    path('deletebrands/',Brand_Controller.Delete_Brands),
    path('editbrandicon', Brand_Controller.Edit_logo),
    path('fetch_all_brand_json/',Brand_Controller.Fetch_All_Brand_Json),
    path('fetch_all_subcategory_json/',Subcategory_Controller.Fetch_All_Subcategory_JSON),
    path('productinterface/', Product_Controller.Product_Interface),
    path('submitproduct', Product_Controller.Submit_Product),
    path('displayproducts/', Product_Controller.Display_All_Products),
    path('editproducts/', Product_Controller.Edit_Products),
    path('deleteproducts/',Product_Controller.Delete_Products),
    path('editproducticon', Product_Controller.Edit_ProductIcon),
    path('imagesinterface',Product_Controller.Images_Interface),
    path('fetch_all_products_json/',Product_Controller.Fetch_All_Product_Json),
    path('submitimage',Product_Controller.Add_Picture),
    path('adminlogin/',Admin_Controller.Admin_Login),
    path('checkadminlogin',Admin_Controller.Check_Admin_Login),
    path('adminlogout/', Admin_Controller.Admin_Logout),
    path('home/', User_Interface.Index),
    path('fetch_all_user_category/', User_Interface.Fetch_All_Category_JSON),
    path('fetch_all_products/',User_Interface.Fetch_All_Products),
    path('fetch_all_subcategory/',User_Interface.Fetch_All_SubCategory_JSON),
    path('buy_products/',User_Interface.Products_Buy),
    path('add_to_cart',User_Interface.Add_To_Cart),
    path('fetch_cart/',User_Interface.Fetch_Cart),
    path('remove_from_cart/',User_Interface.RemoveFromCart),
    path('shop_cart/',User_Interface.Shopping_Cart),
    path('check_user_mobileno/',User_Interface.CheckUserMobileno),
    path('insert_user/',User_Interface.InsertUser),
    path('check_user_mobileno_for_address/',User_Interface.CheckUserMobilenoForAddress),
    path('insert_user_address/',User_Interface.InsertUserAddress),
]