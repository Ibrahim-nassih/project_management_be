from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .keycloack import Keycloak
from .models import CustomUser,Space,Step,Team,Membership,Ticket,Transaction,Workflow
from .serializers import CustomUserSerializer,SpaceSerializer,WorkflowSerializer,StepSerializer,TransactionSerializer,TeamSerializer
from .serializers import MembershipSerializer,TicketSerializer,SprintSerializer
from .decorator import decorator,keycloak_openid
from django.http import Http404
import jwt
class RegisterView(APIView):
    def post(self, request, format=None):
        # Get the user data from the request
        data = request.data
       # Create the Keycloak API client
        keycloak = Keycloak.kc_admin
        try:
            # Create the user in Keycloak
            payload = {
                'email': data['email'],
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'username': data['username'],
                'enabled': True,
                'credentials': [{'value': data['password'], 'type': 'password'}]
            }
            keycloak_user_id = keycloak.create_user(payload)

            group_name = {'name':data["group_name"]}
            keycloak_group_id = keycloak.create_group(group_name,skip_exists=True)
            if keycloak_group_id is None:
                keycloak_group= keycloak.get_group_by_path(data["group_name"])
                keycloak_group_id=keycloak_group['id']

            keycloak.group_user_add(keycloak_user_id, keycloak_group_id)

            # Create the user in Django database
            user = CustomUser(
                username=data['username'],
                email=data['email'],
                firstName=data['firstName'],
                lastName=data['lastName'],
                group_name=data["group_name"],
                keycloak_user_id=keycloak_user_id,
                is_active=True,
            )
            user.set_password(data['password'])
            user.save()

            # Serialize and return the user data
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Return error response if user creation fails
            return Response(
                {"message": "User creation failed: {}".format(str(e))},
                status=status.HTTP_400_BAD_REQUEST
            )
    #@decorator.requires_token
    def get(self, request):
        space_id = request.GET.get('space')
        team = Team.objects.filter(space_id=space_id).first()
        
        if team:
            user_ids = Membership.objects.filter(team=team).values_list('user_id', flat=True)
            users = CustomUser.objects.exclude(id__in=user_ids)
            
            if not users:
                raise Http404("No users found")
            
            serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            raise Http404("Team not found")

from django.db.models import Q
class SpaceView(APIView):
    #@decorator.requires_token
    def get(self, request):
        # Retrieve all spaces created by the user
        token = request.headers.get('Authorization')
        access_token = token[7:]
        # user_info = keycloak_openid.userinfo(access_token)
        user_info = jwt.decode(access_token, options={"verify_signature": False})
        print(f"token: {user_info['preferred_username']}")
        user = CustomUser.objects.filter(username=user_info['preferred_username']).first()

        # Retrieve spaces created by the user
        user_spaces = Space.objects.filter(created_by=user)

        # Retrieve spaces shared within teams where the user is a member
        team_spaces = Space.objects.filter(team__membership__user=user
        )
        print(SpaceSerializer(team_spaces, many=True).data)
        spaces = user_spaces.union(team_spaces)

        if spaces.count() == 0:
            return Response({'error': 'spaces not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SpaceSerializer(spaces, many=True)
        response = Response(serializer.data)
        return response


    
    # @decorator.requires_token
    def post(self, request):
        print(request.data)
        token = request.headers.get('Authorization')
        access_token = token[7:]
        #user=keycloak_openid.userinfo(access_token)

        user_info = jwt.decode(access_token, options={"verify_signature": False})
        print(f"username: {user_info['preferred_username']}")
        user = CustomUser.objects.filter(username=user_info['preferred_username']).first()
        print(f"user:{user}")
        serializer = SpaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_by'] = user
        space = serializer.save()
        return Response(SpaceSerializer(space).data)


    #@decorator.requires_token
    def get_space(self, space_id):
        try:
            space = Space.objects.get(id=space_id)
            return space
        except Space.DoesNotExist:
            return None

    #@decorator.requires_token
    def put(self, request, space_id):
        # Update a specific space
        space = self.get_space(space_id)
        if space:
            serializer = SpaceSerializer(space, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    #@decorator.requires_token
    def delete(self, request):
        # Delete a specific space
        space_id = request.data.get('id')
        print(space_id)
        space=Space.objects.filter(id=space_id).first()
        if space:
            space.delete()
            print('after',space)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class WorkflowView(APIView):
        # Retrieve all workflow by space
    #@decorator.requires_token
    def get(self, request):
        id = request.headers.get('id')
        workflows = Workflow.objects.filter(space_id=id)
        if len(workflows)==0:
            return Response({'error': 'workflows not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkflowSerializer(workflows, many=True)
        return Response(serializer.data)
    
    #@decorator.requires_token
    def post(self, request):
        serializer = WorkflowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow = serializer.save()
        print(workflow)
        return Response(WorkflowSerializer(workflow).data)
       
    #@decorator.requires_token
    def delete(self, request):
        workflow_id = request.GET.get('id')
        W = Workflow.objects.filter(id=workflow_id).first()
        if not W:
            return Response({'error': 'workflow not found'}, status=404)
        W.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class WorkflowStepsAPIView(APIView):
    #@decorator.requires_token
    def post(self, request):
        print(request.data)
        steps=request.data
        serializer=StepSerializer(data=steps,many=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=201)
    
    #@decorator.requires_token
    def get(self, request):
        workflow_ids = request.GET.get('workflowIds')
        steps = Step.objects.filter(workflow=workflow_ids).order_by('order')  # Order the steps by ID

        if not steps:
            raise Http404

        serializer = StepSerializer(steps, many=True)
        response = Response(serializer.data)
        return response
    #@decorator.requires_token
    def put(self, request):
        from_step = request.data.get('from_step')
        to_step = request.data.get('to_step')
        lead_id = request.data.get('lead')
        step_0 = Step.objects.filter(order=from_step,workflow_id=lead_id).first()
        step_1 = Step.objects.filter(order=to_step,workflow_id=lead_id).first()
        if not step_0 and step_1:
            return Response({'error': 'switch not possible'}, status=404)
        step_1.order = from_step
        step_0.order = to_step
        step_1.save()
        step_0.save()
        steps=Step.objects.filter(workflow_id=lead_id).order_by('order')
        serializer = StepSerializer(steps,many=True)
        return Response(serializer.data)
class SpaceViewDetails(APIView):
    #@decorator.requires_token
    def get(self,request,id):
        stepsworkflow=Step.objects.filter(workflow_id=id).order_by('id')
        print(stepsworkflow)
        if not stepsworkflow:
           raise Http404
        serializer = StepSerializer(stepsworkflow,many=True)
        response = Response(serializer.data)
        return response
    
class TransactionView(APIView):
    #@decorator.requires_token
    def post(self, request):
        transactions=request.data
        serializer=TransactionSerializer(data=transactions,many=True)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data,status=201)
    #@decorator.requires_token
    def get(self,request):
        workflow_ids = request.GET.get('workflowIds')
        transactions = Transaction.objects.filter(workflow=workflow_ids).order_by('id')  # Order the steps by ID

        if not transactions:
            raise Http404

        serializer = TransactionSerializer(transactions, many=True)
        response = Response(serializer.data)
        return response
    #@decorator.requires_token
    def put(self, request):
        transaction_id = request.data.get('id')
        serializer = TransactionSerializer(data=request.data)
        transaction = Transaction.objects.filter(id=transaction_id).first()
        if not transaction:
            return Response({'error': 'Transaction not found'}, status=404)
        if serializer.is_valid():
            serializer.update(transaction, serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #@decorator.requires_token
    def patch(self, request):
        transaction_id = request.data.get('id')
        from_step = request.data.get('from_step')
        to_step = request.data.get('to_step')
        transaction = Transaction.objects.filter(id=transaction_id).first()
        if not transaction:
            return Response({'error': 'Transaction not found'}, status=404)
        transaction.from_step_id = from_step
        transaction.to_step_id = to_step
        transaction.save()
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
        
class TeamView(APIView):
    #@decorator.requires_token
    def post(self, request):
        print(request.data)
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #@decorator.requires_token
    def get(self, request):
        space_id = request.GET.get('space')
        team = Team.objects.filter(space_id=space_id).first()
        if not team:
            raise Http404
        serializer = TeamSerializer(team)
        response = Response(serializer.data)
        return response
class UsersView(APIView):
    #@decorator.requires_token
    def get(self, request):
        space_id = request.GET.get('space')
        id = Team.objects.filter(space_id=space_id).values_list('id', flat=True).first()
        user_ids = Membership.objects.filter(team_id=id).values_list('user_id', flat=True)
        users = CustomUser.objects.filter(id__in=user_ids)
        if not users:
            raise Http404("No users found")
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
class MembershipView(APIView):
    #@decorator.requires_token
    def post(self, request):
        print(request.data)
        serializer = MembershipSerializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #@decorator.requires_token
    def get(self, request):
        id = request.headers.get('id')
        id = Team.objects.filter(space_id=id).values_list('id', flat=True).first()
        user_ids = Membership.objects.filter(team_id=id)
        serializer = MembershipSerializer(user_ids,many=True)
        return Response(serializer.data)
class TicketView(APIView):
    #@decorator.requires_token
    def post(self, request):
        print(request.data)
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #@decorator.requires_token
    def get(self,request):
        workflow_ids = request.GET.get('workflowIds')
        tickets = Ticket.objects.filter(workflow=workflow_ids).order_by('id')  # Order the steps by ID

        if not tickets:
            raise Http404

        serializer = TicketSerializer(tickets, many=True)
        response = Response(serializer.data)
        return response
    #@decorator.requires_token
    def put(self, request):
        ticket_id = request.GET.get('id')
        serializer = TicketSerializer(data=request.data)

        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=404)

        if serializer.is_valid():
            serializer.update(ticket, serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #@decorator.requires_token
    def patch(self, request):
        ticket_id = request.data.get('id')
        to_step = request.data.get('status')

        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=404)

        ticket.status_id = to_step
        ticket.save()

        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    #delete ticket by its id 
    #@decorator.requires_token
    def delete(self, request):
        ticket_id = request.GET.get('id')
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=404)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TaskView(APIView):
    #@decorator.requires_token
    def get(self, request):
        workflow_ids = request.GET.get('workflowIds')
        print(workflow_ids)
        steps = Step.objects.filter(workflow=workflow_ids).order_by('id')  # Order the steps by ID
        if not steps:
            raise Http404
        steps = StepSerializer(steps, many=True)
        transactions = Transaction.objects.filter(workflow=workflow_ids).order_by('id')  # Order the steps by ID
        if not transactions:
            raise Http404
        transactions = TransactionSerializer(transactions, many=True)
        tickets = Ticket.objects.filter(workflow=workflow_ids).order_by('id')  # Order the steps by ID
        if not tickets:
            raise Http404

        tickets = TicketSerializer(tickets, many=True)
        payloaD={
            'tickets':tickets.data,
            'steps':steps.data,
            'transactions':transactions.data
        }
        return Response(payloaD)

class SprintView(APIView):
    #@decorator.requires_token
    def post(self,request):
        print(request.data)
        sprint=request.data
        serializer=SprintSerializer(data=sprint)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class TicketsSprintView(APIView):
    #@decorator.requires_token
    def put(self, request):
        print(request.data)
        sprint = request.data.get('sprint')
        ticket_ids = request.data.get('tickets')
        status = request.data.get('status')
        step=Step.objects.filter(id=status).first()
        # Use __in to filter tickets based on a list of IDs
        tickets = Ticket.objects.filter(id__in=ticket_ids)
        
        for ticket in tickets:
            ticket.status = step
            ticket.sprint = sprint
            ticket.save()
        all_tickets=Ticket.objects.filter(workflow=tickets[0].workflow)
        serializer=TicketSerializer(all_tickets,many=True)
        return Response(serializer.data)