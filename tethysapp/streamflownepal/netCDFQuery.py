
import netCDF4
import numpy
import datetime
t1=datetime.datetime.now()
ncFullPath = '/home/suman/192.168.11.242 user Suman/Qout_era5_t640_24hr_19790101to20191231.nc'
# ncFullPath = '/zData/temps/south_asia-geoglows/Qout_era5_t640_24hr_19790101to20191231.nc'
nc_fid = netCDF4.Dataset(ncFullPath, 'r')
lis_var = nc_fid.variables
Comid=5084007
rividAll = nc_fid.variables['rivid'][:]
time = nc_fid.variables['time'][:]
t2=datetime.datetime.now()
getDifference = numpy.abs(rividAll - Comid)
absRiverId = numpy.abs(getDifference - Comid)
comid_idx = (absRiverId.argmin())
listNew=[]
DateList=[]
timeNew=numpy.array_split(time,40)
for timestep, v in enumerate(time):
    nc_arr = nc_fid.variables['Qout'][timestep,comid_idx]
    listNew.append(float(nc_arr))
    dt = netCDF4.num2date(lis_var['time'][timestep], units=lis_var['time'].units, calendar=lis_var['time'].calendar)
    dt_str=dt.strftime("%Y-%m-%d %H:%M:%S")
    DateList.append(dt_str)
print(listNew)
print(DateList)
nc_fid.close()
t3=datetime.datetime.now()
print('t2-t1',t2-t1)
print('t3-t2',t3-t2)
print('t3-t1',t3-t1)
