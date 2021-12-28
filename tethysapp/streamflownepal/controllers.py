from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from tethys_sdk.gizmos import Button
import decimal, csv, simplejson
from .chartUtils import getForecastData, get_forecastpercent
import requests, psycopg2
from datetime import timedelta
import datetime as dt
from .config import APIHost,AuthorizationToken,initilizationData
#@login_required()

def check_for_decimals(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def getGeoJson():
    request_params = dict(cty='nepal')
    request_headers = dict(Authorization=AuthorizationToken)
    res = requests.get(APIHost+'/apps/apicenter/api/getFeaturesECMWF', params=request_params, headers=request_headers)
    return(res.text)

def chart(request):
    return_obj = {}
    try:
        comid =int(request.GET.get('stID'))
    except:
        comid = 58807
    return_obj = getForecastData(comid)
    # return JsonResponse(return_obj)
    return_obj = simplejson.dumps(return_obj, ignore_nan=True)
    return HttpResponse(return_obj, content_type= 'application/json')

def forecastpercent(request):
    if request.is_ajax() and request.method == 'GET':
        comid = request.GET.get('comid')
        return JsonResponse(get_forecastpercent(comid))

def index(request):
    context = initilizationData
    return render(request, 'streamflownepal/main.html', context)

def getForecastCSV(request):
    comid = request.GET.get('comid')
    cty = request.GET.get('cty')
    runDate = request.GET.get('forecastDate')

    if runDate is None:
        runDate = dt.datetime.now().date() - timedelta(days=1)

    conn = psycopg2.connect(host="192.168.10.35", database="servirFlood_ECMWF_HKH", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = "SELECT forecastdate, high_res, maxval, meanval, minval FROM public.forecast" + str(
        cty) + " where comid =" + str(comid) + " order by forecastdate"

    cur.execute(query)
    rows = cur.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="forecastData_' + str(comid) + '.csv"'
    header = ['Dates', 'hres', 'max', 'mean', 'min']
    writer = csv.writer(response)
    writer.writerow(header)

    for row in rows:
        hres_dates = (str(dt.datetime.strftime(row[0], '%Y-%m-%d %H:%M:%S')))
        # dates.append(str(dt.datetime.strftime(row[0],'%Y-%m-%d %H:%M:%S')))
        max_values = (float(row[2]))
        mean_values = (float(row[3]))
        min_values = (float(row[4]))
        # std_dev_lower_values = (row[5])
        # std_dev_upper_values = (row[6])
        hres_values = (row[1])
        writer.writerow(
            [hres_dates, hres_values, max_values, mean_values, min_values])
    conn.close()
    return response

def getHistoricCSV(request):
    comid = request.GET.get('comid')
    cty = request.GET.get('cty')

    conn = psycopg2.connect(host="192.168.10.35", database="servirFlood_ECMWF_HKH", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = "select historydate, historyvalue from history" + str(cty) + " where comid = " + str(
        comid) + " order by historydate"
    cur.execute(query)
    rows = cur.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historicData_' + str(comid) + '.csv"'
    header = ['Dates', 'Values']
    writer = csv.writer(response)
    writer.writerow(header)
    for row in rows:
        mydate = str(dt.datetime.strftime(row[0], '%Y-%m-%d %H:%M:%S'))
        writer.writerow([mydate, row[1]])
    conn.close()
    return response


