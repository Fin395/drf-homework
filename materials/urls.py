from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
urlpatterns = [

] + router.urls