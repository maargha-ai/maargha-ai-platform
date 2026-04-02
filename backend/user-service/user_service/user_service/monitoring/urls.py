from django.urls import path

from user_service.monitoring.health import (
    health_check_view,
    detailed_health_check,
    get_metrics,
    readiness_check,
    liveness_check,
)

urlpatterns = [
    path("", health_check_view, name="health_check"),
    path("detailed", detailed_health_check, name="health_check_detailed"),
    path("metrics", get_metrics, name="health_metrics"),
    path("readiness", readiness_check, name="health_readiness"),
    path("liveness", liveness_check, name="health_liveness"),
]
