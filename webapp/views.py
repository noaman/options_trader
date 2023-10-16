from django.http.response import HttpResponse, JsonResponse 
from django.http import HttpResponseRedirect 
from django.shortcuts import render , redirect

from django.urls import reverse

from django.views.decorators.http import require_GET
from webapp.utils.opstrascraper import OpstraScraper

from webapp.utils.apimanager import ApiManager

from webapp.utils.optionscron import OptionsCron

import pandas as pd


apimgr = ApiManager()

def refresh_json(request):
    opCron = OptionsCron()
    opCron.fetchTrendLyneHeatMap()
    opCron.fetchTrendScreeners()
    return HttpResponseRedirect(reverse('Index'))
    
def getFuturesOptionsMR(request):
    opstraObj = OpstraScraper()
    opstraObj.writeFuturesData()
    opstraObj.writeOptionsData()
    
    return redirect('/df')  


def load20DFuturesBU(request):
    data = {}
    return render(request , "opstraanalysis.html" , data)
    
def gen20DFuturesBU(request):
    sym_list = ""
    if request.method == 'POST':
        # Get the input field's value by its name attribute
        sym_list = request.POST['symbol_list']

    print (sym_list)
    
    opstraObj = OpstraScraper()
    opstraObj.writeAnalysisData(sym_list)
    return HttpResponseRedirect(reverse('Index'))
    
    
def showDataframe(request):
    df_list = apimgr.getbuiltupDF()
    
    ''' # Convert the HTML table back to a DataFrame
    new_df_list = pd.read_html(df_list["df_master"].__str__())

    # Select the DataFrame from the list (use [0] if there's only one table)
    master_df = new_df_list[0]

    master_df.to_excel("Output/master_ranking.xlsx")
 '''

    
    return render(request,"df.html",{"dflist":df_list}) 

def showScreener(request,scrip=''):    
    # screenerdata=tl_scraper.getTrendLyneOptionScreenrs(scrip)

    # data={"data":screenerdata}
    screenerdata = apimgr.getScreenerDF(scrip)
    heatmapdata=apimgr.getHeatMapDF('')
    lotsize =0 
    stepsize=0
    for dt in heatmapdata["data"]:
        if(dt["code"]==scrip):
            lotsize = dt["lotsize"]
            stepsize = dt["contract_step"]

    return render(request,"screener.html",{"screenerdata":screenerdata,"scrip":scrip,"heatmapdata":heatmapdata,"lotsize":lotsize,"stepsize":stepsize}) 

def showHeatmap(request,sort=''):
    data_to_send=apimgr.getHeatMapDF(sort)
    data={"heatmapdf":data_to_send}
    return render(request,"heatmap.html",data) 


def showDashboard(request):
    
    data_to_send=apimgr.getIndustryHeatMap()
    return render(request,"index.html",data_to_send) 



def showTop20(request):
    price_longbuild=apimgr.getHeatMapDF("price_longbuild")
    oi_longbuild=apimgr.getHeatMapDF("oi_longbuild")
    price_shortbuild=apimgr.getHeatMapDF("price_shortbuild")
    oi_shortbuild=apimgr.getHeatMapDF("oi_shortbuild")

    buildups=[price_longbuild,oi_longbuild,price_shortbuild,oi_shortbuild]
    displays=["PRICE LONG BUILD UP","OI LONG BUILD UP","PRICE SHORT BUILD UP","OI SHORT BUILD UP"]
    
    data_to_send = {"data":buildups,"displays":displays}
    return render(request,"top20.html",data_to_send) 

