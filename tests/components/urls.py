from django.urls import path

# REMOVED: Component.as_view() - View extension removed
# from tests.components.multi_file.multi_file import MultFileComponent
# from tests.components.single_file import SingleFileComponent

urlpatterns = [
    # REMOVED: Component views
    # path("single/", SingleFileComponent.as_view(), name="single"),
    # path("multi/", MultFileComponent.as_view(), name="multi"),
]
