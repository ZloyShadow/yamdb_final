from django.urls import include, path

app_name = 'api'


urlpatterns = [
    path('v1/', include('api.api_v1.urls')),
]
