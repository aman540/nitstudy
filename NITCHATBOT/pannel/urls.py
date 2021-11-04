from django.urls import path
from pannel import views

urlpatterns = [
    path('', views.index,name="home"),
    path('room_i/<str:pk>/',views.room,name="room"),
    path('create_room',views.Create_room,name="create-room"),
    path('update_room/<str:pk>/',views.UpdateRoom,name="update-room"),
    path('delete_room/<str:pk>/',views.DeleteRoom,name="delete-room"),
    path('profile/<str:pk>/',views.userProfile,name="user-profile"),

    path('login/',views.LoginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('register/',views.RegisterUser,name='register'),

    path('delete_message/<str:pk>/',views.DeleteMessage,name="delete-message"),

    path('update_user/',views.Update_profile,name='update_user'),
    
    path('topics/',views.topics,name='topics'),
    path('activity/',views.activity,name='activity'),
]
