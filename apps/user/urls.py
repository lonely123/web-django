from django.urls import path
from django.conf.urls import url
from django.urls import path
from user.views import RegisterView,ActiveView,LoginView,LogoutView,UserOrderView,UserInfoView,AddressView


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'), # 注册
    path('active/<token>', ActiveView.as_view(), name='active'), # 用户激活

    path('login/', LoginView.as_view(), name='login'), # 登录
    path('logout/', LogoutView.as_view(), name='logout'), # 注销登录

    path('', UserInfoView.as_view(), name='user'), # 用户中心-信息页
    path('order/<int:page>', UserOrderView.as_view(), name='order'), # 用户中心-订单页
    path('address/', AddressView.as_view(), name='address'), # 用户中心-地址页


]
