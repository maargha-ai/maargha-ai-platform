from django.urls import path

from user_service.user_service.monitoring import health

urlpatterns = [
    path("", health.health_check, name="health_check"),
    path("detailed", health.detailed_health_check, name="health_check_detailed"),
    path("metrics", health.get_metrics, name="health_metrics"),
    path("readiness", health.readiness_check, name="health_readiness"),
    path("liveness", health.liveness_check, name="health_liveness"),
]
