from django.conf import settings
from osgeo import gdal,osr
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import numpy as np
import os
import sys

def toraster(bandarray):
    pass

def project(inputdsname, rasterxsize, rasterysize, datatype, projection, geotransform, srs):
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

def calculate(timenow, DW, DF_name, RW, RF_name, AW, AF_name, SW, SF_name, TW, TF_name, IW, IF_name, CW, CF_name, UW, UF_name):
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
    else:
        try:
            RF_name = project(RF_name, rasterxsize, rasterysize, datatype, projection, geotransform, srs)
            RF_ds = gdal.Open(os.path.join(settings.MEDIA_ROOT, RF_name))
            RF_ba = BandReadAsArray(RF_ds.GetRasterBand(1))
        except:
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

    CALC_ba = DF_ba*DW + RF_ba*RW + AF_ba*AW + SF_ba*SW + TF_ba*TW + IF_ba*IW + CF_ba*CW + UF_ba*UW
    #CALC_ba =  np.sum([DF_ba*DW], [RF_ba*RW], [AF_ba*AW], [SF_ba*SW], [TF_ba*TW], [IF_ba*IW], [CF_ba*CW], [UF_ba*UW])
    #CALC_ba = np.add(DF_ba, RF_ba)
    #print(CALC_ba)

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
    render_ds.GetRasterBand(1).WriteArray(CALC_ba)
    render_ds.GetRasterBand(2).WriteArray(CALC_ba)
    render_ds.GetRasterBand(3).WriteArray(CALC_ba)
    render_ds.GetRasterBand(4).WriteArray(trsp_ba)
    render_ds.SetGeoTransform(geotransform)
    render_ds.SetProjection(projection)
    #render_ds.SetProjection(srs)


    pngdriver = gdal.GetDriverByName('PNG')
    png_ds_name = timenow+'-render'+'.png'
    png_ds = pngdriver.CreateCopy(os.path.join(settings.MEDIA_ROOT,png_ds_name), render_ds, 0)
    CopyDatasetInfo(DF_ds,png_ds)

    return (os.path.join(settings.MEDIA_URL, output_ds_name), os.path.join(settings.MEDIA_URL, render_ds_name), os.path.join(settings.MEDIA_URL,png_ds_name), minx, miny, maxx, maxy)
