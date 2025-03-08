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
    path('G.html/', views.g1, name='g1'),
    path('m_g/<int:goal_id>/', views.m_g, name='m_g'),
    path('de_g/<int:goal_id>/', views.d_g, name='d_g'),
    path('b1.html/', views.b1, name='b1'),
    path('b1.html/add-bill/', views.add_bill, name='add_bill'),
    path('delete_bill/<int:bill_id>/', views.delete_bill, name='delete_bill'), 
    path('mark_bill/<int:bill_id>/', views.mark_bill, name="mark_bill"),
    path('check_goal_progress/', views.check_goal_progress, name='check_goal_progress'),
    path('report.html/',views.report, name='report'),
    path('FAQ.html/',views.faq, name='faq'),
    path('privacy.html/',views.privacy, name='privacy'),
    path('security.html/',views.security, name='security'),
    path('terms.html/',views.terms, name='terms'), 
    path('support.html/',views.support,name='support'),
    
]
