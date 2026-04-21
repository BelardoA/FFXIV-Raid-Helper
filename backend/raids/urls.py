from django.urls import path

from . import views

urlpatterns = [
    # Raid tiers
    path("raids/", views.RaidTierListView.as_view(), name="raid-list"),
    path("raids/<slug:slug>/", views.RaidTierDetailView.as_view(), name="raid-detail"),
    # Fights
    path("fights/", views.FightListView.as_view(), name="fight-list"),
    path("fights/<slug:slug>/", views.FightDetailView.as_view(), name="fight-detail"),
    path(
        "fights/<slug:slug>/drill/",
        views.FightDrillPlanView.as_view(),
        name="fight-drill-plan",
    ),
    # Mechanics
    path("mechanics/", views.MechanicListView.as_view(), name="mechanic-list"),
    path("mechanics/<int:pk>/", views.MechanicDetailView.as_view(), name="mechanic-detail"),
    # Simulation
    path("simulate-step/", views.SimulateStepView.as_view(), name="simulate-step"),
    # Sessions
    path(
        "sessions/<str:session_key>/stats/",
        views.SessionStatsView.as_view(),
        name="session-stats",
    ),
]
