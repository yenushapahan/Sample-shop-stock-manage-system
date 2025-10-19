import json

from numpy import printoptions
class DATABASE:
    def createTable(self,fileName):
        web = open(f'{fileName}.json','a')

        web1 = open(f'{fileName}.json','r')
        if(web1 != ''):
            web.write('[]')
            web1.close()
        web.close()
    
    def insertData(self,fileName,content):
        #getting index
        indexId = self.gettingIndex(fileName)

        web1 = open(f'{fileName}.json','r')
        
        web1 = str(web1.read())[:-1] + '\n' + ",{" + '\n' + f'"{indexId}"' + f":{json.dumps(content,indent=len(content))}" + '\n' + " }" + '\n' +"]"

        web2 = open(f"{fileName}.json",'w')
        web2.write(web1)

        web2.close()
    
    def insertData2(self,fileName,content):
        #getting index
        indexId = self.gettingIndex(fileName)

        web1 = open(f'{fileName}.json','r')
        
        web1 = str(web1.read())[:-1] + '\n' + f",{json.dumps(content,indent=len(content))}]"

        web2 = open(f"{fileName}.json",'w')
        web2.write(web1)

        web2.close()

    
    def readData(self,fileName):
        
        web = open(f'{fileName}.json','r')
        
        data = json.loads(web.read())

        if not data:
            data = []

        return data

    def searchData(self,fileName,keyOfDict,valueOfDict):
        web = open(f'{fileName}.json','r')
        #dataset = json.dumps(web.read())

        data = json.loads(web.read())

        #count = [orderId for orderId in data if(orderId["orderId"] == 1)]
        results = [item for item in data if (item[f"{keyOfDict}"] == f"{valueOfDict}")]


        return results
    
    def gettingIndex(self,fileName):
        web = open(f'{fileName}.json','r')
        return len(json.load(web)) + 1

    def updateData(self,fileName,indexId,updatedContend):
        web = open(f"{fileName}.json",'r')

        data = json.loads(web.read())

        #print(data[indexId - 1])
        data[indexId - 1] = updatedContend

        #rewrite updated conted on database
        web1 = open(f"{fileName}.json","w")

        web1.write(json.dumps(data,indent=len(updatedContend)))

        web1.close()

        pass

    def deleteData(self,fileName,indexId):
        web = open(f"{fileName}.json",'r')

        data = json.loads(web.read())

        #data.pop(indexId - 1)

        #rewrite updated conted on database
        web1 = open(f"{fileName}.json","w")

        web1.write(json.dumps(data,indent=len(data.pop(indexId - 1))))

        web1.close()

    def findUniqItems(self, fileName, keyOfDict):
        dataset = self.readData(fileName)

        uniqItems = set()  # Use a set directly

        for entry in dataset:
            item = entry[keyOfDict].lower()  # Fix the typo
            uniqItems.add(item)  # Use set.add() instead of checking with 'not in'

        return uniqItems
    
    def selectItems(self, fileName, keyOfDict, keyOfValue, condition):
        dataset = self.readData(fileName)

        items = []

        for item in dataset:
            if eval(f"{item[keyOfValue]} {condition}"):  # Dynamically evaluate condition
                items.append(item[keyOfDict])

        return items
    
