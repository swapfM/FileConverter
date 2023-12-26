from django.http import HttpResponse
from django.shortcuts import render, redirect
import img2pdf
# import pandas as pd
import string
import random
import os
from pdf2image import convert_from_path
import shutil
# import tabula


# Create your views here.
def home(request):
    return render(request, 'index.html')


# def pdf_view(request):
#     with open('./convertor/sample_10.pdf', 'r') as pdf:
#         response = HttpResponse(pdf.read(), content_type='application/pdf')
#         response['Content-Disposition'] = 'inline'
#         return response


def jpgToPdf(request):
    # img2pdf pip

    if request.method == "POST":
        # creating random folder name for each user
        shutil.rmtree('./convertor/static/uploaded_files/jpg2pdf/', ignore_errors=True, onerror=None)
        res = ''.join(random.choice(string.ascii_lowercase) for x in range(10))

        path_to_upload = os.path.join('./convertor/static/uploaded_files/jpg2pdf', str(res))
        os.makedirs(path_to_upload)
        files = request.FILES

        for file in files.getlist('files'):
            file_name = os.path.splitext(file.name)[0]
            file_name = "/" + file_name
            with open(path_to_upload + file_name + ".pdf", "wb") as f:
                f.write(img2pdf.convert(file, rotation=img2pdf.Rotation.ifvalid))

        createZip(path_to_upload)

        return render(request, 'jpgtopdf.html', {'url': str(res)})
    return render(request, 'jpgtopdf.html')


def pdftojpg(request):
    # pdf2image

    if request.method == "POST":
        shutil.rmtree('./convertor/static/uploaded_files/pdf2jpg/', ignore_errors=True, onerror=None)
        # creating random folder name for each user
        res = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        path_to_upload = os.path.join('./convertor/static/uploaded_files/pdf2jpg', str(res))
        os.makedirs(path_to_upload)
        file = request.FILES

        file_name = str(file['files']).split(".")[0]

        file_name = "/" + file_name

        with open(path_to_upload + file_name + ".pdf", "wb+") as f:
            for chunk in file['files'].chunks():
                f.write(chunk)

        images = convert_from_path(path_to_upload + file_name + ".pdf", 500)
        for i in range(len(images)):
            images[i].save(path_to_upload + file_name + str(i + 1) + '.jpg', 'JPEG')

        os.remove(path_to_upload + file_name + ".pdf")
        createZip(path_to_upload)

        return render(request, 'pdftojpg.html', {'url': str(res)})
    return render(request, 'pdftojpg.html')


def pdftocsv(request):
    if request.method == "POST":
        shutil.rmtree('./convertor/static/uploaded_files/docx2pdf/', ignore_errors=True, onerror=None)

        res = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        path_to_upload = os.path.join('./convertor/static/uploaded_files/docx2pdf', str(res))
        os.makedirs(path_to_upload)
        file = request.FILES

        file_name = str(file['files']).split(".")[0]

        file_name = "/" + file_name

        with open(path_to_upload + file_name + ".docx", "wb+") as f:
            for chunk in file['files'].chunks():
                f.write(chunk)
        name = path_to_upload + file_name
        # tabula.convert_into(name + ".pdf", name + ".csv", output_format="csv", pages="all")

    # Convert a folder of DOCX files to PDF

    return render(request, 'pdftocsv.html')


def createZip(arg):
    shutil.make_archive(arg, 'zip', arg)
    shutil.rmtree(arg, ignore_errors=True)
