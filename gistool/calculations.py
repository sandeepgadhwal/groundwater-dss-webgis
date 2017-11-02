from django.conf import settings
from osgeo import gdal,osr
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import numpy as np
import os
import sys

def to_rgb(bandarray):
    maxvalue = np.amax(bandarray)
    #minvalue = np.amin(bandarray)
    #print("from RGB",maxvalue,minvalue, bandarray)
    bandarray = np.divide(bandarray, maxvalue)
    bandarray = bandarray * 100
    # Colour the red band
    r_ba = bandarray * 1 #intialize new band
    r_ba[(r_ba > 0) & (r_ba < 33)] = 11 #first class
    r_ba[(r_ba > 33) & (r_ba < 50)] = 14 #Second Class
    r_ba[(r_ba > 50) & (r_ba < 66)] = 245 #third class
    r_ba[(r_ba > 66) & (r_ba < 83)] = 230 #fourth class
    r_ba[(r_ba > 83) & (r_ba < 100)] = 194 #fifth class
    # Colour the green band
    g_ba = bandarray * 1
    g_ba[(g_ba > 0) & (g_ba < 33)] = 44 #first class
    g_ba[(g_ba > 33) & (g_ba < 50)] = 196 #Second Class
    g_ba[(g_ba > 50) & (g_ba < 66)] = 215 #third class
    g_ba[(g_ba > 66) & (g_ba < 83)] = 142 #fourth class
    g_ba[(g_ba > 83) & (g_ba < 100)] = 82 #fifth class
    # Colour the blue band
    b_ba = bandarray * 1
    b_ba[(b_ba > 0) & (b_ba < 33)] = 122 #first class
    b_ba[(b_ba > 33) & (b_ba < 50)] = 65 #Second Class
    b_ba[(b_ba > 50) & (b_ba < 66)] = 7 #third class
    b_ba[(b_ba > 66) & (b_ba < 83)] = 28 #fourth class
    b_ba[(b_ba > 83) & (b_ba < 100)] = 60 #fifth class
    #print(maxvalue,minvalue, bandarray, r_ba, g_ba, b_ba)
    return(r_ba, g_ba, b_ba)

def project(inputdsname, rasterxsize, rasterysize, datatype, projection, geotransform):
    inputds = gdal.Open(os.path.join(settings.MEDIA_ROOT,inputdsname))
    outputfilename = inputdsname+'projected.tiff'
    outputfile = os.path.join(settings.MEDIA_ROOT,outputfilename)
    driver= gdal.GetDriverByName('GTiff')
    output = driver.Create(outputfile, rasterxsize, rasterysize, 1, datatype)
    output.SetGeoTransform(geotransform)
    output.SetProjection(projection)
    gdal.ReprojectImage(inputds,output,inputds.GetProjection(),projection,gdalconst.GRA_Bilinear)
    del output
    return outputfilename

def calculatedr(timenow, DW, DF_name, RW, RF_name, AW, AF_name, SW, SF_name, TW, TF_name, IW, IF_name, CW, CF_name, UW, UF_name):

    divisor = 7;
    #read datasets
    DF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT,DF_name))

    #get information first file
    projection = DF_ds.GetProjection()
    srs = osr.SpatialReference(wkt=projection)
    #print(srs)
    geotransform = DF_ds.GetGeoTransform()
    rasterxsize = DF_ds.RasterXSize
    rasterysize = DF_ds.RasterYSize
    minx = geotransform[0]
    maxy = geotransform[3]
    maxx = minx + geotransform[1] * DF_ds.RasterXSize
    miny = maxy + geotransform[5] * DF_ds.RasterYSize
    DF_bd = DF_ds.GetRasterBand(1)
    datatype = DF_bd.DataType
    DF_ba = BandReadAsArray(DF_bd)
    #print(DF_ba)

    #trsp_ba = DF_ba*1
    DF_ba[DF_ba < 0] = 0
    #trsp_ba[trsp_ba < 254] = 1
    #trsp_ba[trsp_ba > 254] = 0
    #trsp_ba = trsp_ba*255

    # get array for each raster file
    if RF_name == 'blank':
        RF_ba = DF_ba*0
        divisor = divisor-1;
    else:
        try:
            RF_name = project(RF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            RF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, RF_name))
            RF_ba = BandReadAsArray(RF_ds.GetRasterBand(1))
            RF_ba[RF_ba < 0] = 0
        except:
            #print('rf blank expect')
            RF_ba = DF_ba*0
            divisor = divisor-1;

    if AF_name == 'blank':
        AF_ba = DF_ba*0
        divisor = divisor-1;

    else:
        try:
            AF_name = project(AF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            AF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, AF_name))
            AF_ba = BandReadAsArray(AF_ds.GetRasterBand(1))
            AF_ba[AF_ba < 0] = 0
        except:
            AF_ba = DF_ba*0
            divisor = divisor-1;

    if SF_name == 'blank':
        SF_ba = DF_ba*0
        divisor = divisor-1;
    else:
        try:
            SF_name = project(SF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            SF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, SF_name))
            SF_ba = BandReadAsArray(SF_ds.GetRasterBand(1))
            SF_ba[SF_ba < 0] = 0
        except:
            SF_ba = DF_ba*0
            divisor = divisor-1;

    if TF_name == 'blank':
        TF_ba = DF_ba*0
        divisor = divisor-1;
    else:
        try:
            TF_name = project(TF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            TF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, TF_name))
            TF_ba = BandReadAsArray(TF_ds.GetRasterBand(1))
            TF_ba[TF_ba < 0] = 0
        except:
            TF_ba = DF_ba*0
            divisor = divisor-1;

    if IF_name == 'blank':
        IF_ba = DF_ba*0
        divisor = divisor-1;
    else:
        try:
            IF_name = project(IF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            IF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, IF_name))
            IF_ba = BandReadAsArray(IF_ds.GetRasterBand(1))
            IF_ba[IF_ba < 0] = 0
        except:
            IF_ba = DF_ba*0
            divisor = divisor-1;

    if CF_name == 'blank':
        CF_ba = DF_ba*0
        divisor = divisor-1;
    else:
        try:
            CF_name = project(CF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            CF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, CF_name))
            CF_ba = BandReadAsArray(CF_ds.GetRasterBand(1))
            CF_ba[CF_ba < 0] = 0
        except:
            CF_ba = DF_ba*0
            divisor = divisor-1;

    if UF_name == 'blank':
        UF_ba = DF_ba*0
        #divisor = divisor-1;
    else:
        try:
            UF_name = project(UF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            UF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, UF_name))
            UF_ba = BandReadAsArray(UF_ds.GetRasterBand(1))
            UF_ba[UF_ba < 0] = 0
        except:
            UF_ba = DF_ba*0
            #divisor = divisor-1;
    #CALCULATE ALL VALUES
    CALC_ba = DF_ba * DW + RF_ba * RW + AF_ba * AW + SF_ba * SW + TF_ba * TW + IF_ba * IW + CF_ba*CW #+ UF_ba*UW
    #CALC_ba = np.divide(CALC_ba, divisor)

    #CONVERT TO rgb
    colour_ba = to_rgb(CALC_ba)
    r_ba = colour_ba[0]
    g_ba = colour_ba[1]
    b_ba = colour_ba[2]
    #GET TRANSPARENCY LAYER
    trsp_ba = r_ba*r_ba*r_ba
    trsp_ba[trsp_ba > 0] = 1
    trsp_ba = trsp_ba*255

    outdriver = gdal.GetDriverByName('GTiff')
    output_ds_name = timenow+'-output'+'.tiff'
    print("File processed by Gdal GEOTIFF saved by name"+output_ds_name)
    output_ds = outdriver.Create(os.path.join(settings.MEDIA_ROOT,output_ds_name), rasterxsize, rasterysize, 1, datatype)
    CopyDatasetInfo(DF_ds,output_ds)
    output_bd = output_ds.GetRasterBand(1)
    BandWriteArray(output_bd, CALC_ba)
    #print(DF_ba)
    #print(CALC_ba)
    #DF_ds = None
    #del output_ds

    renderdriver = gdal.GetDriverByName('GTiff')
    render_ds_name = timenow+'-render'+'.tiff'
    options = ['PHOTOMETRIC=RGB', 'PROFILE=GeoTIFF']
    #print(renderdriver)
    #print(datatype)
    render_ds = renderdriver.Create(os.path.join(settings.MEDIA_ROOT,render_ds_name), rasterxsize, rasterysize, 4, gdal.GDT_Int32)
    CopyDatasetInfo(DF_ds,render_ds)
    render_ds.GetRasterBand(1).WriteArray(r_ba)
    render_ds.GetRasterBand(2).WriteArray(g_ba)
    render_ds.GetRasterBand(3).WriteArray(b_ba)
    render_ds.GetRasterBand(4).WriteArray(trsp_ba)
    render_ds.SetGeoTransform(geotransform)
    render_ds.SetProjection(projection)
    #render_ds.SetProjection(srs)


    pngdriver = gdal.GetDriverByName('PNG')
    png_ds_name = timenow+'-render'+'.png'
    png_ds = pngdriver.CreateCopy(os.path.join(settings.MEDIA_ROOT,png_ds_name), render_ds, 0)
    CopyDatasetInfo(DF_ds,png_ds)

    return (os.path.join(settings.MEDIA_URL, output_ds_name), os.path.join(settings.MEDIA_URL, render_ds_name), os.path.join(settings.MEDIA_URL,png_ds_name), minx, miny, maxx, maxy)

def calculatega(timenow, DW, DF_name, RW, RF_name, AW, AF_name, SW, SF_name, TW, TF_name, IW, IF_name, CW, CF_name, UW, UF_name):
    #print(os.path.join(settings.MEDIA_ROOT, DF_name))
    #print(receivedfiles)
    #read datasets
    DF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT,DF_name))
    #RF_in_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT,RF_name))

    #get information first file
    projection = DF_ds.GetProjection()
    srs = osr.SpatialReference(wkt=projection)
    #print(srs)
    geotransform = DF_ds.GetGeoTransform()
    rasterxsize = DF_ds.RasterXSize
    rasterysize = DF_ds.RasterYSize
    minx = geotransform[0]
    maxy = geotransform[3]
    maxx = minx + geotransform[1] * DF_ds.RasterXSize
    miny = maxy + geotransform[5] * DF_ds.RasterYSize
    DF_bd = DF_ds.GetRasterBand(1)
    datatype = DF_bd.DataType
    DF_ba = BandReadAsArray(DF_bd)
    #print(DF_ba)
    trsp_ba = DF_ba*1
    #print(trsp_ba)
    DF_ba[DF_ba>254]=0
    #print(DF_ba)
    #print(trsp_ba)
    trsp_ba[trsp_ba < 254] = 1
    trsp_ba[trsp_ba > 254] = 0
    trsp_ba = trsp_ba*255
    #print(trsp_ba)
    #trsp_ba[trsp_ba>-1]=255
    #print(trsp_ba)
    #trsp_ba[trsp_ba<-1]=0
    #print(trsp_ba)

    # get array for each raster file
    if RF_name == 'blank':
        RF_ba = DF_ba*0
        print('rf blank if')
    else:
        try:
            RF_name = project(RF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            RF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, RF_name))
            RF_ba = BandReadAsArray(RF_ds.GetRasterBand(1))
        except:
            print('rf blank expect')
            RF_ba = DF_ba*0

    if AF_name == 'blank':
        AF_ba = DF_ba*0
    else:
        try:
            AF_name = project(AF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            AF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, AF_name))
            AF_ba = BandReadAsArray(AF_ds.GetRasterBand(1))
        except:
            AF_ba = DF_ba*0

    if SF_name == 'blank':
        SF_ba = DF_ba*0
    else:
        try:
            SF_name = project(SF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            SF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, SF_name))
            SF_ba = BandReadAsArray(SF_ds.GetRasterBand(1))
        except:
            SF_ba = DF_ba*0
    if TF_name == 'blank':
        TF_ba = DF_ba*0
    else:
        try:
            TF_name = project(TF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            TF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, TF_name))
            TF_ba = BandReadAsArray(TF_ds.GetRasterBand(1))
        except:
            TF_ba = DF_ba*0

    if IF_name == 'blank':
        IF_ba = DF_ba*0
    else:
        try:
            IF_name = project(IF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            IF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, IF_name))
            TF_ba = BandReadAsArray(IF_ds.GetRasterBand(1))
        except:
            IF_ba = DF_ba*0

    if CF_name == 'blank':
        CF_ba = DF_ba*0
    else:
        try:
            CF_name = project(CF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            CF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, CF_name))
            CF_ba = BandReadAsArray(CF_ds.GetRasterBand(1))
        except:
            CF_ba = DF_ba*0

    if UF_name == 'blank':
        UF_ba = DF_ba*0
    else:
        try:
            UF_name = project(UF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
            UF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, UF_name))
            UF_ba = BandReadAsArray(UF_ds.GetRasterBand(1))
        except:
            UF_ba = DF_ba*0
    #correctify all files and Read them
    ''''
    RF_name = project(RF_name, rasterxsize, rasterysize, datatype, projection, geotransform)
    RF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, RF_name))
    '''

    '''
    outputfile = os.path.join(settings.MEDIA_ROOT,RF_name)+'projected.tiff'
    driver= gdal.GetDriverByName('GTiff')
    output = driver.Create(outputfile,DF_ds.RasterXSize,DF_ds.RasterYSize,1,DF_bd.DataType)
    output.SetGeoTransform(geoTransform)
    output.SetProjection(projection)
    gdal.ReprojectImage(RF_ds,output,RF_ds.GetProjection(),projection,gdalconst.GRA_Bilinear)
    del output
    '''
    '''
    RF_bd = RF_ds.GetRasterBand(1)

    DF_ba = BandReadAsArray(DF_bd)
    RF_ba = BandReadAsArray(RF_bd)
    '''

    '''
    print(BandReadAsArray(DF_bd).shape)
    print("zzzzzzzz this is DF ")
    print(BandReadAsArray(RF_bd).shape)
    print("zzzzzzzz this is RF ")
    '''

    CALC_ba = (DF_ba * DW + RF_ba * RW + AF_ba * AW + SF_ba * SW + TF_ba * TW + IF_ba * IW + CF_ba*CW )/7
    #print(CALC_ba)
    print(DF_ba)
    print(RF_ba)
    colour_ba = to_rgb(CALC_ba)
    print(CALC_ba)
    r_ba = colour_ba[0]
    g_ba = colour_ba[1]
    b_ba = colour_ba[2]

    outdriver = gdal.GetDriverByName('GTiff')
    output_ds_name = timenow+'-output'+'.tiff'
    print("File processed by Gdal GEOTIFF saved by name"+output_ds_name)
    output_ds = outdriver.Create(os.path.join(settings.MEDIA_ROOT,output_ds_name), rasterxsize, rasterysize, 1, datatype)
    CopyDatasetInfo(DF_ds,output_ds)
    output_bd = output_ds.GetRasterBand(1)
    BandWriteArray(output_bd, CALC_ba)
    #print(DF_ba)
    #print(CALC_ba)
    #DF_ds = None
    #del output_ds

    renderdriver = gdal.GetDriverByName('GTiff')
    render_ds_name = timenow+'-render'+'.tiff'
    options = ['PHOTOMETRIC=RGB', 'PROFILE=GeoTIFF']
    #print(renderdriver)
    #print(datatype)
    render_ds = renderdriver.Create(os.path.join(settings.MEDIA_ROOT,render_ds_name), rasterxsize, rasterysize, 4, gdal.GDT_Int32)
    CopyDatasetInfo(DF_ds,render_ds)
    render_ds.GetRasterBand(1).WriteArray(r_ba)
    render_ds.GetRasterBand(2).WriteArray(g_ba)
    render_ds.GetRasterBand(3).WriteArray(b_ba)
    render_ds.GetRasterBand(4).WriteArray(trsp_ba)
    render_ds.SetGeoTransform(geotransform)
    render_ds.SetProjection(projection)
    #render_ds.SetProjection(srs)


    pngdriver = gdal.GetDriverByName('PNG')
    png_ds_name = timenow+'-render'+'.png'
    png_ds = pngdriver.CreateCopy(os.path.join(settings.MEDIA_ROOT,png_ds_name), render_ds, 0)
    CopyDatasetInfo(DF_ds,png_ds)

    return (os.path.join(settings.MEDIA_URL, output_ds_name), os.path.join(settings.MEDIA_URL, render_ds_name), os.path.join(settings.MEDIA_URL,png_ds_name), minx, miny, maxx, maxy)
