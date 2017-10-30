from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from gistool.calculations import calculate
import datetime
# Create your views here.

def index(request):
    if request.method == 'POST':
        #get time for storing files IST
        timenow = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d-%H-%M-%S')

        #get filestorage of local system
        fs = FileSystemStorage()

        #get wieghtage from the form
        indicators = ['DW', 'RW', 'AW', 'SW', 'TW', 'IW', 'CW', 'UW']
        for x in indicators:
            try:
                globals()[x] = int(request.POST[x])
                print(x+" = "+globals()[x])
            except:
                globals()[x] = 1
                print("NO Wieghtage given for "+x+" Assigned default = 1")

        # get files from the form
        indicatorfiles = ['DF', 'RF', 'AF', 'SF', 'TF', 'IF', 'CF', 'UF']
        for x in indicatorfiles:
            xname = x+"_name"
            try:
                globals()[x] = request.FILES[x]
                globals()[xname] = timenow+'-input-'+'-'+x+'-'+globals()[x].name
                fs.save(globals()[xname], globals()[x])
                print (x+" File saved by name "+globals()[xname])
            except:
                globals()[xname] = 'blank'
                print("No file uploaded for "+x+" Will ignore in calculations")

        #get it processd by gdal
        response = calculate(timenow, DW, DF_name, RW, RF_name, AW, AF_name, SW, SF_name, TW, TF_name, IW, IF_name, CW, CF_name, UW, UF_name)
        output = response[0]
        rendered = response[1]
        png = response[2]
        minx = response[3]
        miny = response[4]
        maxx = response[5]
        maxy = response[6]
        #processedfile = 'output'+timenow+'.png'
        #fs = FileSystemStorage()
        #processedfile = fs.save(processedfile, processed)
        #processed_file_url = fs.url(processedfile)
        return render(request, 'gistool/index.html', {
            'output_file_url': output,
            'rendered_file_url': rendered,
            'png_file_url': png,
            'minx' : minx,
            'miny' : miny,
            'maxx' : maxx,
            'maxy' : maxy
        })

    return render(request, 'gistool/index.html')
