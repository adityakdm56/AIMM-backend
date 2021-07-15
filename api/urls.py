from django.urls import path, include
from .views import *

app_name = "api"

urlpatterns = [

    # ************************************MANAS*************************

    path('users/', api_users_all, name="All_Users"),
    path('depts/', api_depts_all, name="All_Depts"),
    path('login/', api_login, name="User_Login"),
    path('user_queries/<int:pk>/', api_userQueries, name="User_Queries"),
    path('deleteEquipment/<slug:pk>/',
         api_delEquipment, name="Delete_Equipment"),
    path('modifyEquipment/<slug:pk>/',
         api_modifyEquipment, name="Modify_Equipment"),
    path('get_staff_requests/<int:pk>/',
         api_get_staff_requests, name="Staff_Requests"),
    path('get_teams/', api_get_teams, name="Team_List"),
    # to add .....
    path('add_department/', api_add_department, name="Add_Department"),
    path('get_ticket_details/<int:pk>/',
         api_get_ticket_details, name="Get_Details_Of_Request"),
    path('get_user_tasks/<int:pk>/', api_user_tasks,
         name="Tasks_Assigned_To_User"),
    path('start_maintenance/<int:pk>/', api_start_maintenance,
         name="Start_Maintenance"),
    path('complete_maintenance/<int:pk>/', api_complete_maintenance,
         name="Complete_Maintenance"),
    path('get_profile/<int:pk>/', api_get_profile,
         name="Get_Profile"),
    path('change_password/<int:pk>/', api_change_password,
         name="Change_Password"),
    path('forward_request/<int:pk>/', api_forward_request,
         name="Forward_Request"),

    # **************************ADITYA*******************************

    path('equipment/', api_equipments_details, name="Equip_details"),
    path('dept_equipments/', api_dept_equipments, name="dept_Equip_details"),
    path('dept_maintenance/', api_dept_maintenance,
         name="dept_maintenance_details"),
    path('dept_maintenance_ongoing/', api_dept_maintenance_details,
         name="dept_maintenance_details_forstatus"),
    path('dept_maintenance_count/', api_dept_maintenance_count,
         name="dept_maintenance_details_statuscount"),
    path('all_dept_maintenance_count/', api_all_dept_maintenance_count,
         name="all_dept_maintenance_details_statuscount"),
    path('user_information/<slug:pk>/',
         api_users_details, name="show users details"),
    path('create_team/', api_create_team, name="create_new_team"),
    path('allocate_technician/', api_allocate_request, name="allocate_technician"),


    # ***************************AJAY***************************

    path('maintenance/add/', api_raise_maintenance_ticket,
         name="raise_maintenance_request"),
    path('equipment/add/', api_add_equipment, name="add equipment"),
    path('signup/', api_signup_request, name="sign_request"),
    path('signup/approve/<int:pk>/', api_signup_approve, name="sign_approve"),
    path('signup/reject/<int:pk>/', api_signup_reject, name="sign_reject"),
    path('maintenance/current/<slug:val>/',
         api_current_maintenance_tickets, name="current_maintenance"),
    path('maintenance/<slug:val>/', api_equip_maintenance_details,
         name="equip_maintenance_details"),
]
