from django.urls import path, include
from .views import HomeView, DashBordView, PersonalUserDashBordView, InfluenceUserDashBordView

urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('dashbord', DashBordView.as_view(),name='dashbord'),
    path('dashbord/<str:username>', PersonalUserDashBordView.as_view(),name='dashbord'),
    path('dashbord/<str:username>/personal', PersonalUserDashBordView.as_view(),name='personal'),
    path('dashbord/<str:username>/influence', InfluenceUserDashBordView.as_view(),name='influence'),

]
