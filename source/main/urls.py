"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from webapp.views.goal_views import GoalCreateView, GoalView, GoalUpdateView, GoalDeleteView
from webapp.views.project_views import IndexView, ProjectView, \
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView, \
    project_mass_action_view  # , GoalCreateView, GoalUpdateView, GoalDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('project/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('project/add/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(),
         name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(),
         name='project_delete'),
    path('project/mass-action/', project_mass_action_view, name='project_mass_action'),


    path('goal/<int:pk>/', GoalView.as_view(), name='goal_view'),
    path('project/<int:pk>/goals/add', GoalCreateView.as_view(),
         name='goal_add'),
    path('project/<int:pk>/goals/update/', GoalUpdateView.as_view(),
         name='goal_update'),
    path('project/<int:pk>/goal/delete/', GoalDeleteView.as_view(),
         name='goal_delete'),

]
