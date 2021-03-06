from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from goods.models import GoodsSKU
from django_redis import get_redis_connection
# Create your views here.
from utils.mixin import LoginRequiredMixin
class CartAddView(View):
    def post(self,request):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'res':0,'errmst':'请先登录'})

        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        if not all([sku_id,count]):
            return  JsonResponse({'res':1,'errmsg':'数据不完整'})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res':2,'errmsg':'商品数目出错'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res':3,'errmsg':'商品不存在'})

        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id

        cart_count = conn.hget(cart_key,sku_id)
        if cart_count:
            count += int(cart_count)

        if count > sku.stock:
            return JsonResponse({'res':4,'errmsg':'商品库存不足'})


        conn.hset(cart_key,sku_id,count)


        total_count = conn.hlen(cart_key)


        return JsonResponse({'res':5,'total_count':total_count,'message':'添加成功'})

class CartInfoView(LoginRequiredMixin, View):
    '''购物车页面显示'''
    def get(self, request):
        '''显示'''
        # 获取登录的用户
        user = request.user
        # 获取用户购物车中商品的信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        # {'商品id':商品数量, ...}
        cart_dict = conn.hgetall(cart_key)

        skus = []
        # 保存用户购物车中商品的总数目和总价格
        total_count = 0
        total_price = 0
        # 遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 计算商品的小计
            amount = sku.price*int(count)
            # 动态给sku对象增加一个属性amount, 保存商品的小计
            sku.amount = amount
            # 动态给sku对象增加一个属性count, 保存购物车中对应商品的数量
            sku.count = int(count)
            # 添加
            skus.append(sku)

            # 累加计算商品的总数目和总价格
            total_count += int(count)
            total_price += amount

        # 组织上下文
        context = {'total_count':total_count,
                   'total_price':total_price,
                   'skus':skus}

        # 使用模板
        return render(request, 'cart.html', context)

# 更新购物车记录
# 采用ajax post请求
# 前端需要传递的参数:商品id(sku_id) 更新的商品数量(count)
# /cart/update
class CartUpdadeView(View):
    def post(self,request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res':0,'errmst':'请先登录'})

        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        conn=get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        if count > sku.stock:
            return JsonResponse({'res':4,'errmsg':'商品库存不足'})

        conn.hset(cart_key, sku_id, count)

        total_count = conn.hlen(cart_key)

        return JsonResponse({'res':5,'total_count':total_count,'message':'添加成功'})


class CartDeleteView(View):
    def post(self,request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res':0,'errmsg':'请先登录'})

        sku_id = request.POST.get('sku_id')

        if not sku_id:
            return JsonResponse({'res':1,'errmsg':'无效商品id'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res':2,'errmsg':'商品不存在'})

        conn = get_redis_connection('default')
        cart_key = 'car_%d'%user.id

        conn.hdel(cart_key,sku_id)

        total_count = conn.hlen(cart_key)



        return JsonResponse({'res':3,'total_count':total_count,'message':' 删除成功'})












