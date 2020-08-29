from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    # HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    ProfileDetailView,
    # RequestRefundView
)
from django.contrib.auth.views import LoginView
from core import views

app_name = 'core'

urlpatterns = [
    # path('', index.views, name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('sellers/', views.sellers_signup, name='sellers-signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/create-prod', views.item_create_view, name='item-create-view'),
    path('', views.search_lunnex, name='search-lunnex'),
    path('search/', views.results, name='results'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('payment-options/', views.payment_option, name='payment_option'),
    path('payment/stripe/', PaymentView.as_view(), name='payment'),
    path('payment/paystack/', views.paystack, name='payment-paystack'),
    path('process/', views.payment_process, name="process"),
    path('done/', views.payment_done, name="done"),
    path('canceled', views.payment_canceled, name='canceled')
    # path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]