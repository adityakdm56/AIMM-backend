from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *
import random   
import datetime
from django.core.mail import send_mail, send_mass_mail
# from rest_framework.decorators import parser_classes

# RETURNS ALL USERS AND THEIR DETAILS
@api_view(['GET'])
def api_users_all(request):
    try:
        user = User.objects.all()
        if not user:
            return Response({'code': 4}, status=status.HTTP_404_NOT_FOUND)
    except user.DoesNotExists:
        return Response({'code': 4}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, many=True)
        dicto = {'code': 2, 'data': serializer.data}
        return Response(dicto)

# RETURNS ALL DEPARTMENTS AND TEHIR PRIMARY KEYS
@api_view(['GET'])
def api_depts_all(request):
    try:
        dept = Department.objects.all()
        if not dept:
            return Response({"code": 4, "data": "No Deta"}, status=status.HTTP_404_NOT_FOUND)
    except dept.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DepartmentWithUsersSerializer(dept, many=True)
        dicto = {'code': 2, 'data': serializer.data}
        return Response(dicto)

# CHECKS USER CREDENTIALS AND RETURNS STATUS AND ALL DETIALS OF THAT USER
@api_view(['POST'])
def api_login(request):
    if request.method == "POST":
        username = request.data['username']
        password = request.data['password']
        designation = request.data['designation']

        try:
            user = User.objects.get(
                email=username, password=password, designation=designation)
            serializer = UserSerializer(user)
            return Response({"code": 2, "data": serializer.data})
        except Exception as e:
            return Response({"code": 4, "data": "Unauthorized Access"}, status=status.HTTP_401_UNAUTHORIZED)


# API TO RETURN ALL THE QUERIES RAISED BY A PERTICULART USER
# the slug here is users primary key which we will keep in async
@api_view(['GET'])
def api_userQueries(request, pk):
    if request.method == "GET":
        try:
            ticket = MaintenanceTicket.objects.filter(raised_by=pk)
            # print(ticket)

            if not ticket:
                return Response({"code": 4, "data": "No data"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MaintenanceTicketSerializer(ticket, many=True)
            return Response({"code": 2, "data": serializer.data})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "ex": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# API TO MODIFY EQUIPMENT
@api_view(['PUT'])
def api_modifyEquipment(request, pk):
    if request.method == "PUT":
        try:
            equipment = Equipment.objects.get(serial_no=pk)
            # GET ALL REQUEST FIELDS
            name = request.data['name']
            desc = request.data['description']
            priority = request.data['priority']
            location = request.data['location']
            maintenance_latency = request.data['maintenance_latency']

            # FOR EMPTY QUERYSE5T
            #name, description, priority,location, installation_date ,maintainance_letency
            if not equipment:
                return Response({"code": 4, "data": "No such Equipment"}, status=status.HTTP_400_BAD_REQUEST)

            # EMPTY VALIDATION
            if name and desc and priority and location and maintenance_latency:
                serializer = EquipmentModificationSerializer(
                    equipment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"code": 2, "data": "Equipment Updated"})
                else:
                    raise Exception("Invalid data")
            else:
                # sdf
                raise Exception("No Fields can be left Blank")

        except Exception as e:
            return Response({"code": 4, "data": "exc: "+str(e)}, status=status.HTTP_400_BAD_REQUEST)

# API TO DELETE AN EQUIPMENT FROM SYSTEM
@api_view(['DELETE'])
def api_delEquipment(request, pk):
    if request.method == "DELETE":
        try:
            equipment = Equipment.objects.filter(serial_no=pk)
            # FOR EMPTY QUERYSE5T
            if not equipment:
                return Response({"code": 4, "data": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
            equipment.delete()
            return Response({"code": 2, "data": "Equipment Deleted"})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_get_staff_requests(request, pk):
    if request.method == "GET":
        try:
            requests = UserRequest.objects.filter(department=pk, status="raised")
            # print(pk)
            # FOR EMPTY QUERYSE5T
            if not requests:
                return Response({"code": 4, "data": "No data"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserRequestSerializer(requests, many=True)
            return Response({"code": 2, "data": serializer.data})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "exc": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# api to return anmes of all teams
# should also return all details of a team
@api_view(['GET'])
def api_get_teams(request):
    if request.method == "GET":
        try:
            teams = Team.objects.all()
            urr = User.objects.none()
            for team in teams:
                # print(team.head)
                urr |= User.objects.filter(pk=team.head)
                # print(usr.name)

            if not teams:
                return Response({"code": 4, "data": "No data"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TeamSerializer(teams, many=True)
            # serializerUser = UserSerializer(urr, many=True)
            return Response({"code": 2, "data": serializer.data})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "exc": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_add_department(request):
    if request.method == "POST":
        try:
            dept = Department(
                name=request.data['name'], head=request.data['head'])
            dept.save()
            return Response({"code": 2, "data": "Department added Successfully"})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "exc": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# API TO RETURN DETAILS FOR A PERTICULAR TICKET
@api_view(['GET'])
def api_get_ticket_details(request, pk):
    if request.method == "GET":
        try:
            ticket = MaintenanceTicket.objects.get(pk=pk)

            if not ticket:
                return Response({"code": 4, "data": "No data"}, status=status.HTTP_404_NOT_FOUND)

            serializer = MaintenanceTicketSerializer(ticket)
            return Response({"code": 2, "data": serializer.data})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "exc": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# API TO RETURN MAINTENANCE TASK ASSIGNED TO A PERTICULAR USER
@api_view(['GET'])
def api_user_tasks(request, pk):
    if request.method == "GET":
        try:
            ticket = MaintenanceTicket.objects.filter(
                technician_assigned=pk, status='pending')
            # print(pk)
            if not ticket:
                return Response({"code": 4, "data": "No data"}, status=status.HTTP_404_NOT_FOUND)

            serializer = MaintenanceTicketSerializer(ticket, many=True)
            return Response({"code": 2, "data": serializer.data})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "exc": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# API TO UPDATE STATUS OF MAINTENANCE TICKET TO PENDING
@api_view(['PUT'])
def api_start_maintenance(request, pk):
    if request.method == "PUT":
        try:
            ticket = MaintenanceTicket.objects.get(pk=pk)
            if not ticket:
                return Response({"code": 4, "data": "No such Equipment"}, status=status.HTTP_400_BAD_REQUEST)
            ticket.status = "pending"
            ticket.save()
            return Response({"code": 2, "data": "Update Success"})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "exc": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# API TO UPDATE STATUS OF MAINTENANCE TICKET TO COMPLETED
# WE NEED TO HANDLE THE MULTIPLE COORDINATOR ISSUE HERE
@api_view(['POST'])
def api_complete_maintenance(request, pk):
    if request.method == "POST":
        try:
            uid = request.data['user_id']
            ticket = MaintenanceTicket.objects.get(pk=pk)
            if not ticket:
                return Response({"code": 4, "data": "No such Equipment"}, status=status.HTTP_400_BAD_REQUEST)

            # get techs id and remove it from the tech_assigned by .remove and set it to tech_completed and if count=0 then change status
            ticket.technician_assigned.remove(uid)
            ticket.technician_completed.add(uid)
            techCount = ticket.technician_assigned.count()
            print(techCount)
            if techCount == 0:
                ticket.status = "completed"
                ticket.save()
                return Response({"code": 2, "data": "Update Success : Maintenance completed"})
            return Response({"code": 2, "data": "Update Success"})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "exc": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_get_profile(request, pk):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=pk)

            if not user:
                return Response({"code": 4, "data": "No data"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response({"code": 2, "data": serializer.data})
        except Exception as e:
            return Response({"code": 4, "data": "Bad Request", "ex": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_change_password(request, pk):
    if request.method == "POST":
        try:
            user = User.objects.get(pk = pk, password = request.data['old_password'])
            if not user:
                return Response({"code": 4, "data": "No data"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if request.data['new_password']:
                    user.password = request.data['new_password']
                    user.save()
                    return Response({"code": 2, "data": "Password Updated Successfully"})
            return Response({"code": 4, "data": "No data"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"code": 4, "data": "No data","Exc":str(e) }, status=status.HTTP_404_NOT_FOUND)

# API TO ADD A NEW DEPARTMENT TO REQUEST
@api_view(['POST'])
def api_forward_request(request,pk):
    if request.method=="POST":
        try:
            teamId = request.data['team_id']
            ticket = MaintenanceTicket.objects.get(pk = pk)
            team = Team.objects.get(pk=teamId)
            # ifTeam = MaintenanceTicket.objects.get(pk = pk,teams = team)
            
            if not ticket:
                return Response({"code": 4, "data": "No such Ticket"}, status=status.HTTP_404_NOT_FOUND)
            
            if not team:
                return Response({"code": 4, "data": "No such team"}, status=status.HTTP_404_NOT_FOUND)
            
            # To check if the team is already part of the ticket
            # if not ifTeam:
                # return Response({"code": 4, "data": "No such dept in query"}, status=status.HTTP_404_NOT_FOUND)
            
            ticket.teams.add(team)

            ticket.save()

            return Response({"code":2,"data":"Request has been forwarded"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": 4, "data": "No data","Exc":str(e) }, status=status.HTTP_404_NOT_FOUND)



# --------------------------------ADITYA----------------------

@api_view(['POST'])
def api_equipments_details(request):
    if request.method == 'POST':
        equip_id= request.data['equipment_id']
        print(equip_id)
        try:
            equip = Equipment.objects.get(serial_no=equip_id)
            if not equip:
                raise Exception("NOT FOUND")
            serializer = EquipmentSerializer(equip)
            dicto= {'code':2,'data' : serializer.data}
            return Response(dicto)
        except Exception as ex:
            return Response({'code':4},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def api_dept_equipments(request):
    if request.method == 'POST':

        try:
            dept_id = request.data['dept_id']
            print(dept_id)
            equipment = Equipment.objects.filter(department=dept_id)
            if not equipment:
                raise Exception("not found")
            serializer = EquipmentSerializer(equipment,many=True)
            dicto= {'code':2,'data' : serializer.data}
            return Response(dicto)
        except Exception as ex:
            return Response({'code':4},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def api_dept_maintenance(request):
    if request.method == 'POST':
        dept_id = request.data['dept_id']
        print(dept_id)
        try:
            equipments = Equipment.objects.filter(department=dept_id)
            #maintenance = MaintenanceTicket.objects.filter(equipment= equipments)
            if not equipments:
                raise Exception("not found")
            serializer = EquipmentMaintenanceSerializer(equipments,many=True)
            dicto= {'code':2,'data' : serializer.data}
            return Response(dicto)
        except Exception as ex:
            return Response({'code':4},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def api_dept_maintenance_details(request):
    if request.method == 'POST':
        dept_id = request.data['dept_id']

        try:
            maintenances=MaintenanceTicket.objects.none()

            for i in MaintenanceTicket.objects.all():
                print(i.equipment.department.id)
                if (i.status != "completed"):
                    equipments = Equipment.objects.filter(serial_no=i.equipment.serial_no, department=dept_id)
                    if equipments:
                        maintenances |= MaintenanceTicket.objects.filter(pk=i.id)
            print(maintenances)
            if not maintenances:
                raise Exception("no maintenance ticket")
            serializer = MaintenanceSerializer(maintenances,many=True)
            dicto= {'code':2,'data' : serializer.data}
            return Response(dicto)

        except Exception as ex:
            return Response({'code':4},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def api_dept_maintenance_count(request):
    if request.method == 'POST':
        dept_id = request.data['dept_id']

        try:

            equipments = Equipment.objects.none()
            countraised = 0
            countpending = 0
            countcompletd = 0
            for i in MaintenanceTicket.objects.all():
                if (i.status=="completed"):
                    equipments = Equipment.objects.filter(serial_no=i.equipment.serial_no, department=dept_id)
                    if equipments:
                        countcompletd += 1

                elif(i.status=="pending"):
                    equipments = Equipment.objects.filter(serial_no=i.equipment.serial_no, department=dept_id)
                    if equipments:
                        countpending += 1

                elif(i.status == "raised"):
                    equipments = Equipment.objects.filter(serial_no=i.equipment.serial_no, department=dept_id)
                    if equipments:
                        countraised += 1


            dicto = {'code': 2, 'data': {'count raised': countraised, 'count pending': countpending,
                                         'count completed': countcompletd}}
            return Response(dicto)
        except Exception as ex:
            return Response({'code': 4}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def api_all_dept_maintenance_count(request):
    if request.method == 'GET':
        try:
            equipments = Equipment.objects.none()
            countraised = 0
            countpending = 0
            countcompletd = 0
            for i in MaintenanceTicket.objects.all():
                if (i.status=="completed"):
                    equipments = Equipment.objects.filter(serial_no=i.equipment.serial_no)
                    if equipments:
                        countcompletd += 1

                elif(i.status=="pending"):
                    equipments = Equipment.objects.filter(serial_no=i.equipment.serial_no)
                    if equipments:
                        countpending += 1

                elif(i.status == "raised"):
                    equipments = Equipment.objects.filter(serial_no=i.equipment.serial_no)
                    if equipments:
                        countraised += 1


            dicto = {'code': 2, 'data': {'count raised': countraised, 'count pending': countpending,
                                         'count completed': countcompletd}}
            return Response(dicto)
        except Exception as ex:
            return Response({'code': 4}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def api_users_details(request,pk):
    try:
        users= User.objects.none()
        print(pk)
        for user in User.objects.all():
            if(user.name.upper().find(pk.upper())!=-1):
                users |= User.objects.filter(pk=user.id)

        if not users:
            raise Exception("user not found")


        serializer = UserSerializer(users, many=True)
        dicto = {'code': 2, 'data': serializer.data}
        return Response(dicto)
    except Exception as ex:
        return Response({'code': 4}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def api_create_team(request):
    if request.method == 'POST':
        try:
            team_name = request.data['team_name']
            team_leader = request.data['team_leader']
            team_members = request.data['team_members']
            print(team_name)
            print(team_leader)
            print(team_members)
            team_members.append(team_leader)
            print(team_members)
            t=Team(name=team_name,head=team_leader)
            t.save()
            print(t)
            for user in User.objects.all():
                users = User.objects.filter(pk=user.id,id__in=team_members)
                print(users)
                if users:
                    users.update(team=t)
                    User.objects.filter(pk=user.id, id__in=team_members).update(designation="MC")
                    User.objects.filter(pk=user.id and team_leader).update(designation="MTL")

            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            dicto = {'code': 2, 'data': serializer.data}
            return Response(dicto)

        except Exception as ex:
            return Response({'code': 4,'error':ex}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def api_allocate_request(request):
     if request.method == 'POST':
        if 1:
        #try:
            req_id = request.data['req_id']
            person_id = request.data['person_id']

            maintenance = MaintenanceTicket.objects.get(id=req_id)
            print(maintenance)
            print(person_id)
            if not maintenance:
                raise Exception("no ticket found")

            maintenance.technician_assigned.add(*person_id)
            print(maintenance)
            serializer = MaintenanceSerializer(maintenance)
            dicto = {'code': 2, 'data': serializer.data}
            return Response(dicto)

        #except Exception as ex:
            return Response({'code': 4,'error':ex}, status=status.HTTP_404_NOT_FOUND)



# ****************************AJAY*******************************


@api_view(['POST'])
def api_raise_maintenance_ticket(request):

    if request.method == 'POST':

        try:
            equipment = Equipment.objects.get(
                serial_no=request.data['equipment'])
            
            team_list = request.data['teams']
            teams = []
            for team in team_list:
                t = Team.objects.get(pk=team)
                teams.append(t)

            ticket = MaintenanceTicket(
                description=request.data['description'], equipment=equipment, raised_by=request.data['raised_by'])
            ticket.save()
            ticket.teams.set(teams)
            
            return Response({'code': 2, 'message': 'ticket issued successfully'})

        except equipment.DoesNotExist:
            return Response({"code": 4, "errors": str(e)})


@api_view(['POST'])
def api_add_equipment(request):

    if request.method == 'POST':
        try:
            now = datetime.datetime.now()
            now = str(now)
            serial_no = "S"+now[2:4]+now[5:7]+now[8:10]+now[11:13]+now[14:16]+now[17:19] 
            
            request.data['serial_no'] = serial_no
            print(request.data)
            serializer = EquipmentSerializerAJ(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'code': 2, 'data': serializer.data})
            return Response({'code': 4, 'message': serializer.errors})
        except Exception as e:
            return Response({'code': 4, 'error': str(e)})


@api_view(['POST'])
def api_signup_request(request):
    if request.method == 'POST':
        try:
            dept = Department.objects.get(pk=request.data['department'])
            userRequest = UserRequest(
                name=request.data['name'], email=request.data['email'], designation=request.data['designation'], department=dept)
            userRequest.save()
            return Response({'code': 2})
        except Exception as e:
            return Response({'code': 4, 'error': str(e)})


@api_view(['GET'])
def api_signup_approve(request, pk):
    if request.method == 'GET':
        try:
            userRequest = UserRequest.objects.get(pk=pk)
            userRequest.status = "approved"
            userRequest.save()

            digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            password = ""
            length = 8
            for i in range(0, length):
                password = password + random.choice(digits)

            user = User(name=userRequest.name, email=userRequest.email, password=password,
                        department=userRequest.department, designation=userRequest.designation)
            user.save()
            send_mail(
                subject='Sign In to Your AIMM account',
                message="Hello "+user.name+",<br> Your request for signing in as maintenance team member at Chatrapati Shivaji Maharaj International Airport has been approved. Your temporary password is <b>"+ password + "</b><br> Change it as soon as you login.",
                html_message="Hello "+user.name+",<br> Your request for signing in as maintenance team member at Chatrapati Shivaji Maharaj International Airport has been approved.<br><h3> Your temporary password is <b>"+ password + "</b></h3><br> <h2>Change it as soon as you login.</h2>",
                from_email="ajaydkadam99@gmail.com",
                recipient_list=[user.email],
                fail_silently=False
            )
            serializer = UserSerializer(user)
            return Response({"code": 2, "data": serializer.data})

        except Exception as e:
            return Response({'code': 4, 'error': str(e)})

@api_view(['GET'])
def api_signup_reject(request, pk):
    if request.method == 'GET':
        try:
            userRequest = UserRequest.objects.get(pk=pk)
            userRequest.status = "rejected"
            userRequest.save()

            send_mail(
                subject='Sign In to Your AIMM account',
                message="Hello "+userRequest.name+",<br> Your request for signing in as maintenance team member at Airport Inventory Management System has been rejected.<br> Contact your administrator if you want to get it approved.",
                html_message="Hello "+userRequest.name+",<br> Your request for signing in as maintenance team member at Airport Inventory Management System has been rejected.<br> <h2>Contact your administrator if you want to get it approved.</h2>",
                from_email="ajaydkadam99@gmail.com",
                recipient_list=[userRequest.email],
                fail_silently=False
            )
            return Response({"code": 2, "data": "User Request deleted successfully"})

        except Exception as e:
            return Response({'code': 4, 'error': str(e)})


@api_view(['GET'])
def api_current_maintenance_tickets(request, val):
    if request.method == 'GET':
        try:
            today = date.today()
            ticket = MaintenanceTicket.objects.filter(equipment=val, issue_date=today)
            for item in ticket:
                print(item.id)
            serializer = MaintenanceTicketSerializer(ticket, many=True)
            return Response({"code": 2, "data":serializer.data })
        except Exception as e:
            return Response({'code': 4, 'error': str(e)})



@api_view(['GET'])
def api_equip_maintenance_details(request,val):
    if request.method == 'GET':
        try:
            tickets = MaintenanceTicket.objects.filter(equipment=val)
            if not tickets:
                raise Exception("not found")
            serializer = MaintenanceTicketSerializer(tickets,many=True)
            dicto= {'code':2,'data' : serializer.data}
            return Response(dicto)
        except Exception as ex:
            return Response({"code":4,"exc:":str(ex)},status=status.HTTP_404_NOT_FOUND)
