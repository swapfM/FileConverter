from django.urls import path
from . import views

app_name = 'converter'
urlpatterns = [
    path('', views.home, name='home'),
    path('jpgtopdf', views.jpgToPdf),
    path('pdftojpg', views.pdftojpg),
    path('pdftocsv', views.pdftocsv),
    # path('pdf_view', views.pdf_view)
]
