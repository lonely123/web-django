from django.urls import path
from cart.views import CartAddView,CartUpdadeView,CartDeleteView,CartInfoView
urlpatterns = [
    path('add/',CartAddView.as_view(),name='add'),
    path('update/',CartUpdadeView.as_view(),name='update'),
    path('delete/',CartDeleteView.as_view(),name='delete'),
    path('', CartInfoView.as_view(), name='show'),

]
