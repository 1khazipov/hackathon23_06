"""
URL configuration for djangoHackathon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from myapp import views
#
# urlpatterns = [
#     path('get/', views.download_side_effect, name="get_data")
# ]
urlpatterns = [
    path('get/', views.get_data, name='get_data'),
    path('get/<slug:id>/', views.download_side_effect)
]
