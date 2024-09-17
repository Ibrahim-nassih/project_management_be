from rest_framework import serializers
from .models import CustomUser, Space, Workflow, Step, Transaction, Team, Membership, Ticket, Sprint

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'firstName', 'lastName', 'is_active', 'keycloak_user_id', 'group_name')
        extra_kwargs = {'password': {'write_only': True}}  # Password field is write-only for security

class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'privacy']  # Serialize space fields

class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ['id', 'name', 'description', 'space']  # Serialize workflow fields

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ('id', 'name', 'workflow', 'order')  # Serialize step fields

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'description', 'workflow', 'from_step', 'to_step', 'created_at']  # Serialize transaction fields

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'user', 'team', 'is_admin']  # Serialize membership fields

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'space']  # Serialize team fields

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'priority', 'ticket_type', 'created_at', 'status', 'assigned_to', 'workflow', 'parent_ticket', 'sprint', 'estimationDurationMinutes']  # Serialize ticket fields

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['id', 'name', 'start_date', 'end_date', 'description', 'workflow']  # Serialize sprint fields
