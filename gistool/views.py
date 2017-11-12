from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from gistool.calculations import calculatedr,calculatega
import datetime
# Create your views here.

def index(request):
    if request.method == 'POST':
        #print(request.POST.get)
        #get time for storing files IST
        timenow = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d-%H-%M-%S')

        #get filestorage of local system
        fs = FileSystemStorage()
        outputdr = ''
        rendereddr = ''
        pngdr = ''
        minxdr = ''
        minydr = ''
        maxxdr = ''
        maxydr = ''
        outputga = ''
        renderedga = ''
        pngga = ''
        minxga = ''
        minyga = ''
        maxxga = ''
        maxyga = ''
        try :
            if request.POST.get('drasticanalysis') == '1' :
                print('Doing DRASTIC-U Analysis')
                #get wieghtage from the form
                indicators = ['DW', 'RW', 'AW', 'SW', 'TW', 'IW', 'CW', 'UW']
                for x in indicators:
                    try:
                        globals()[x] = int(request.POST[x])
                        print(x+" = "+str(globals()[x]))
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
                responsedr = calculatedr(timenow, DW, DF_name, RW, RF_name, AW, AF_name, SW, SF_name, TW, TF_name, IW, IF_name, CW, CF_name, UW, UF_name)
                outputdr = responsedr[0]
                rendereddr = responsedr[1]
                pngdr = responsedr[2]
                minxdr = responsedr[3]
                minydr = responsedr[4]
                maxxdr = responsedr[5]
                maxydr = responsedr[6]
            else:
                print('Not Doing DRASTIC-U Analysis - Not checked by user')
        except Exception as e:
            print('Not Doing DRASTIC-U Analysis - internal error',e)

        try:
            if request.POST.get('galditanalysis') == '1' :
                print('Doing GALDIT-U Analysis')
                #get wieghtage from the form
                indicators = ['GW', 'HW', 'GTW', 'GDW', 'IW', 'TW', 'UW']
                for x in indicators:
                    try:
                        globals()[x] = int(request.POST[x])
                        print(x+" = "+globals()[x])
                    except:
                        globals()[x] = 1
                        print("NO Wieghtage given for "+x+" Assigned default = 1")

                # get files from the form
                indicatorfiles = ['GF', 'HF', 'GTF', 'GDF', 'IF', 'TF', 'UF']
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
                responsega = calculatega(timenow, GW, GF_name, HW, HF_name, GTW, GTF_name, DW, DF_name, IW, IF_name, TW, TF_name, UW, UF_name)
                outputga = responsega[0]
                renderedga = responsega[1]
                pngga = responsega[2]
                minxga = responsega[3]
                minyga = responsega[4]
                maxxga = responsega[5]
                maxyga = responsega[6]
            else:
                print('Not Doing GALDIT-U Analysis - Not checked by user')
        except Exception as e:
            print('Not Doing GALDIT-U Analysis - internal error',e)

        return render(request, 'gistool/index.html', {
            'outputdr_file_url': outputdr,
            'rendereddr_file_url': rendereddr,
            'pngdr_file_url': pngdr,
            'minxdr' : minxdr,
            'minydr' : minydr,
            'maxxdr' : maxxdr,
            'maxydr' : maxydr,
            'outputga_file_url': outputga,
            'renderedga_file_url': renderedga,
            'pngga_file_url': pngga,
            'minxga' : minxga,
            'minyga' : minyga,
            'maxxga' : maxxga,
            'maxyga' : maxyga
        })

    return render(request, 'gistool/index.html')
