# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .render_pdf.htmltopdf import pdf_generator
import urllib
import re
import os
import codecs
import timeit

ACCOUNT = ''
PASSWORD = ''

def hello_world(request):
    return HttpResponse("Hello World!")


def create_report(request):
    if 'p' in request.GET:

        start = timeit.default_timer()
        regex_http = re.compile("(?<=:\/\/).*")
        url = str(request.GET['p'])
        url_decode = urllib.parse.unquote(url)
        print(url_decode)
        index = re.search(regex_http, url_decode).start()
        output_url = '{}{}:{}@{}&embed=true'.format(url_decode[:index], ACCOUNT, PASSWORD, url_decode[index:])
        pdf_name = pdf_generator(output_url)
        if pdf_name == 'Failed':
            return HttpResponse('Create PDF Failed! Please try again later.')
        with codecs.open(pdf_name, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment;filename={}'.format(pdf_name)

        os.remove(pdf_name)

        stop = timeit.default_timer()
        print('Time: ', stop - start)
        return response
        #return HttpResponse()
        #pdf.output('report_{}.pdf'.format(id_generator()), 'F')
        #return HttpResponse(output_url)
    else:
        return HttpResponse('wrong path!')
