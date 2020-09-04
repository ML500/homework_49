from django.urls import path, include
from webapp.views.goal_views import GoalCreateView, GoalView, GoalUpdateView, GoalDeleteView
from webapp.views.project_views import IndexView, ProjectView, \
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView, \
    project_mass_action_view

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('project/', include([
        path('<int:pk>/', ProjectView.as_view(), name='project_view'),
        path('add/', ProjectCreateView.as_view(), name='project_create'),
        path('<int:pk>/update/', ProjectUpdateView.as_view(),
             name='project_update'),
        path('<int:pk>/delete/', ProjectDeleteView.as_view(),
             name='project_delete'),
        path('mass-action/', project_mass_action_view, name='project_mass_action'),
        path('<int:pk>/goals/add', GoalCreateView.as_view(),
             name='goal_add'),
    ])),

    path('goal/<int:pk>/', GoalView.as_view(), name='goal_view'),
    path('goal/<int:pk>/update/', GoalUpdateView.as_view(),
         name='goal_update'),
    path('goal/<int:pk>/delete/', GoalDeleteView.as_view(),
         name='goal_delete'),
]
