from zillow import Zillow
zswid = open('zillowAPI/zswid.txt').readline()

z = Zillow(zswid)

# call to generate APIs
# res = z.makeRegionAPICall()
# z.parseGetRegionChildrenResponse(res)

# collect data from housedetails api call 
with open('zillowAPI/zpids_seattle.txt') as file: 
    f = open("zillowAPI/zillowDataSeattle.csv", "a")
    f.write('zpid,street,zipcode,city,state,lat,long,urls, useCode,bedrooms,bathrooms,finishedSqFt,lotSizeSqFt,\n')
    f.close()
    zpids = file.readlines()
    for zid in zpids:
        src = z.makePropertyAPICall(zid.strip())
        if src is not None:
            z.parseGetUpdatedPropertyDetailsResponse(src)

# check for valid .csv 
# import pandas as pd
# df = pd.read_csv('zillowAPI/data/zillowData-seattle.csv', delimiter=',')
# print(df.head())