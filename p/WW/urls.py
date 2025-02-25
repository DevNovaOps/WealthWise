from django.urls import path  
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('i1.html/',views.i1, name='i1'),
    path('i1.html/add-income/', views.add_income, name='add_income'),
    path('i1.html/add-expense/', views.add_expense, name='add_expense'),
    path('G.html/',views.G, name='G'),
]
