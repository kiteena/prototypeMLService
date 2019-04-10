import requests 
import re
import xml.etree.ElementTree as ET


class Zillow: 
    def __init__(self, zswid): 
        self.zswid = zswid

    def makeRegionAPICall(self): 
        try:
            rZpids = requests.get(f'http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id={self.zswid}&state=wa&city=seattle&childtype=neighborhood')

            if rZpids.status_code == 200:
                return rZpids.text
            else: 
                raise Exception()
        except: 
            print('Failure in api call to get zpids')

        return None

    def makePropertyAPICall(self, zpid): 
        try:
            rPropDetails = requests.get(f'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id={self.zswid}&zpid={zpid}')
            
            if rPropDetails.status_code == 200:
                tree = ET.ElementTree(ET.fromstring(rPropDetails.text))
                root = tree.getroot()
                node = root.find('message/code')
                print(node.text)
                print(rPropDetails.url)
                if node: 
                    if node.text == 500 or node == 502: 
                        return None
                return rPropDetails.text
            else: 
                raise Exception()
            return None

        except: 
            print('Failure in api call to get zpids')
        return None

    def parseGetRegionChildrenResponse(self, src): 
            tree = ET.ElementTree(ET.fromstring(src))
            # tree = ET.parse('zillowAPI/GetRegionChildren.xml')
            root = tree.getroot() 
            f = open("zillowAPI/zpids_seattle.txt", "a")
            for item in root.findall('response/list/region/id'): 
                f.write(re.sub(r'\s+', '', item.text) + '\n')
            f.close()

    def parseGetUpdatedPropertyDetailsResponse(self, src): 
        tree = ET.ElementTree(ET.fromstring(src))
        root = tree.getroot()
        f = open("zillowAPI/zillowData.csv", "a")
        for item in root.findall('response'):
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/zpid', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/address/street', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/address/zipcode', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/address/city', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/address/state', ',')))

            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/address/latitude', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/address/longitude', ',')))
            
            if root.find(item.tag +'/images/image') is None: 
                f.write(',')
            else: 
                for url in root.find(item.tag +'/images/image'):
                    f.write(url.text.strip() + ' ')
                f.write(',')
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/editedFacts/useCode', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/editedFacts/bedrooms', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/editedFacts/bathrooms', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/editedFacts/finishedSqFt', ',')))
            f.write(re.sub(r'\s+', '', self._utilCheckNodes(root, item.tag +'/editedFacts/lotSizeSqFt', ',')))
            # f.write(self._utilCheckNodes(root, item.tag +'/homeDescription', ''))
            f.write('\n')
        f.close()

    def _utilCheckNodes(self, root, path, delim): 
        node = root.find(path)
        if node is not None: 
            return node.text.strip() + delim
        else: 
            return ','


