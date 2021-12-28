import requests, ast, json #, decimal
import datetime as dt
from datetime import timedelta
runDate = dt.datetime.now().date() - timedelta(days=0)
from django.http import JsonResponse
from .config import APIHost,AuthorizationToken


def get_returnPeriod_data(comid):
    request_params = dict(comid=comid, cty = 'nepal')
    request_headers = dict(Authorization=AuthorizationToken)
    res = requests.get(APIHost+'/apps/apicenter/ECMWFapi/getreturnPeriodECMWF', params=request_params, headers=request_headers)
    data = json.loads(res.text)
    for key, value in data.items():
        if key == 'max':
            return_max = value
        if key == 'twenty':
            return_20 = value
        if key == 'ten':
            return_10 = value
        if key == 'two':
            return_2 = value
        if key == 'five':
            return_5 = value
        if key == 'fifty':
            return_50 = value
    return return_max, return_2, return_10, return_20, return_5, return_50

def get_historic_data(comid):
    hdates = []
    hvalues= []
    request_params = dict(comid=comid, cty = 'nepal')
    request_headers = dict(Authorization=AuthorizationToken)
    res = requests.get(APIHost+'/apps/apicenter/ECMWFapi/getHistoricECMWF', params=request_params,headers=request_headers)
    data = json.loads(res.text)
    for key, value in data.items():
        if key == 'hdates':
            hdates = value
        if key == 'hvalues':
            hvalues = value
    return hdates, hvalues, hdates[0], hdates[-1]

def get_flow_duration_curve(comid):
    request_params = dict(comid=comid, cty = 'nepal')
    request_headers = dict(Authorization=AuthorizationToken)
    res = requests.get(APIHost+'/apps/apicenter/ECMWFapi/getFlowDurationCurveECMWF', params=request_params,headers=request_headers)
    data = json.loads(res.text)
    for key, value in data.items():
        if key == 'prob':
            prob = value
        if key == 'sorted_daily_avg1':
            sorted_daily_avg1 = value
    return prob, sorted_daily_avg1

def getForecastData(comid):
    request_params = dict(comid=comid, cty = 'nepal')
    request_headers = dict(Authorization=AuthorizationToken)
    res = requests.get(APIHost+'/apps/apicenter/ECMWFapi/getForecastECMWF', params=request_params, headers=request_headers)
    data = json.loads(res.text)
    for key, value in data.items():
        if key == 'dates':
            dates = value
        if key == 'max_values':
            max_values = value
        if key == 'mean_values':
            mean_values = value
        if key == 'min_values':
            min_values = value
        if key == 'std_dev_lower_values':
            std_dev_lower_values = value
        if key == 'std_dev_upper_values':
            std_dev_upper_values = value
        if key == 'hres_values':
            hres_values = value
        if key == 'hres_dates':
            hres_dates = value
        if key == 'runDate':
            runDate = value

    return_obj = {}
    # Get Historic data
    hdate, hval,datetime_start,datetime_end = get_historic_data(comid)

    #Get Return Period
    return_max, return_2, return_10, return_20, return_5, return_50 = get_returnPeriod_data(comid)

    # Get flow duration
    prob, sorted_daily_avg = get_flow_duration_curve(comid)


    return_obj["dates"] = (dates)
    return_obj["hres_dates"] = (hres_dates)
    return_obj["mean_values"] = (mean_values)
    return_obj["hres_values"] = (hres_values)
    return_obj["min_values"] = (min_values)
    return_obj["max_values"] = (max_values)
    # return_obj["std_dev_lower_values"] = (std_dev_lower_values)
    return_obj["std_dev_upper_values"] = (std_dev_upper_values)
    return_obj["success"] = "success"
    return_obj["runDate"] = (runDate)
    return_obj["range"] =  max(min_values) + max(min_values) / 5

    #Historic data
    return_obj["hdate"] = (hdate)
    return_obj["hval"] = (hval)

    #Return Period
    return_obj["return_max"] = return_max
    return_obj["return_2"] = return_2
    return_obj["return_10"] = return_10
    return_obj["return_20"] = return_20
    return_obj["return_5"] = return_5
    return_obj["return_50"] = return_50
    return_obj["datetime_start"] = (datetime_start)
    return_obj["datetime_end"] = (datetime_end)

    #Flow-Duration
    return_obj["prob"] = (prob)
    return_obj["sorted_daily_avg"] = (sorted_daily_avg)

    #Download data
    # return JsonResponse(return_obj)
    return return_obj

def get_forecastpercent(comid):
    ens = ''

    request_params = dict(cty='nepal', comid=comid)
    request_headers = dict(Authorization=AuthorizationToken)  # SERVIR
    rpall = requests.get(APIHost+'/apps/apicenter/ECMWFapi/getreturnPeriodECMWF/',
                         params=request_params, headers=request_headers)

    request_params = dict(cty='nepal', comid=comid)
    request_headers = dict(Authorization=AuthorizationToken)
    ens = requests.get(APIHost+'/apps/apicenter/ECMWFapi/getEnsembleCSVECMWF/', params=request_params,
                       headers=request_headers)

    dicts = ens.content.splitlines()
    dictstr = []
    # a = str(rpall.content, "utf-8")
    aa = rpall.content.decode('utf8').replace("'", '"')
    rpdict = ast.literal_eval(aa)
    # rpdict.pop('max', None)

    rivperc = {}
    riverpercent = {}
    rivpercorder = {}

    for q in rpdict:
        rivperc[q] = {}
        riverpercent[q] = {}

    dictlen = len(dicts)
    for i in range(1, dictlen):
        # b = str(dicts[i], "utf-8")
        b = dicts[i].decode('utf8').replace("'", '"')
        dictstr.append(b.split(","))
        # dictstr.append(dicts[i].split(","))

    for rps in rivperc:
        rp = float(rpdict[rps])
        for b in dictstr:
            date = b[0][:10]
            if date not in rivperc[rps]:
                rivperc[rps][date] = []
            length = len(b)
            for x in range(1, length):
                flow = float(b[x])
                if x not in rivperc[rps][date] and flow > rp:
                    rivperc[rps][date].append(x)
        for e in rivperc[rps]:
            riverpercent[rps][e] = float(len(rivperc[rps][e])) / 51.0 * 100

    for keyss in rivperc:
        data = riverpercent[keyss]
        ordered_data = sorted(
            data.items(), key=lambda x: dt.datetime.strptime(x[0], '%Y-%m-%d'))
        rivpercorder[keyss] = ordered_data

    rivdates = []
    rivperctwo = []
    rivpercfive = []
    rivpercten = []
    rivperctwenty = []
    rivpercfifty = []
    rivpercmax = []

    for a in rivpercorder['two']:
        rivdates.append(a[0])
        rivperctwo.append(a[1])

    for d in rivpercorder['five']:
        rivpercfive.append(d[1])

    for s in rivpercorder['ten']:
        rivpercten.append(s[1])

    for d in rivpercorder['twenty']:
        rivperctwenty.append(d[1])

    for d in rivpercorder['fifty']:
        rivpercfifty.append(d[1])

    for d in rivpercorder['max']:
        rivpercmax.append(d[1])

    formatteddates = [str(elem)[-4:] for elem in rivdates]
    formattedtwo = ["%.0f" % elem for elem in rivperctwo]
    formattedfive = ["%.0f" % elem for elem in rivpercfive]
    formattedten = ["%.0f" % elem for elem in rivpercten]
    formattedtwenty = ["%.0f" % elem for elem in rivperctwenty]
    formattedfifty = ["%.0f" % elem for elem in rivpercfifty]
    formattedmax = ["%.0f" % elem for elem in rivpercmax]

    formatteddates = formatteddates[:len(formatteddates) - 5]
    formattedtwo = formattedtwo[:len(formattedtwo) - 5]
    formattedfive = formattedfive[:len(formattedfive) - 5]
    formattedten = formattedten[:len(formattedten) - 5]
    formattedtwenty = formattedtwenty[:len(formattedtwenty) - 5]
    formattedfifty = formattedtwenty[:len(formattedfifty) - 5]
    formattedmax = formattedtwenty[:len(formattedmax) - 5]

    dataformatted = {'percdates': formatteddates, 'two': formattedtwo, 'five': formattedfive, 'ten': formattedten,
                     'twenty': formattedtwenty, 'fifty': formattedfifty, 'max': formattedmax}

    return dataformatted


