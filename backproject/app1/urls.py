from django.urls import path
from .views import (
    RegisterView,
    SpaceView,
    WorkflowView,
    WorkflowStepsAPIView,
    SpaceViewDetails,
    TransactionView,
    TeamView,
    MembershipView,
    TicketView,
    UsersView,
    TaskView,
    SprintView,
    TicketsSprintView
)

app_name = 'app1'

urlpatterns = [
    # Endpoint for user registration
    path('register', RegisterView.as_view()),

    # Endpoint for space-related operations
    path('space', SpaceView.as_view(), name='space'),

    # Endpoint for workflow-related operations
    path('workflow', WorkflowView.as_view(), name='workflow'),

    # Endpoint for retrieving workflow steps
    path('step', WorkflowStepsAPIView.as_view(), name='workflow_steps'),

    # Endpoint for retrieving space details by workflow
    path('steps/<int:id>', SpaceViewDetails.as_view(), name='steps_by_workflow'),

    # Endpoint for transaction-related operations
    path('transaction', TransactionView.as_view(), name='transaction'),

    # Endpoint for team-related operations
    path('team', TeamView.as_view(), name='team'),

    # Endpoint for retrieving user information
    path('users', UsersView.as_view(), name='users'),

    # Endpoint for membership-related operations
    path('member', MembershipView.as_view(), name='member'),

    # Endpoint for ticket-related operations
    path('ticket', TicketView.as_view(), name='ticket'),

    # Endpoint for task-related operations
    path('tasks', TaskView.as_view(), name='tasks'),

    # Endpoint for sprint-related operations
    path('sprint', SprintView.as_view(), name='sprint'),

    # Endpoint for retrieving tickets associated with a sprint
    path('sprint/tickets', TicketsSprintView.as_view(), name='tickets_sprint'),
]
