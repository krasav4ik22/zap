import requests


ids = []
array = []
har_array = {}


servername = "localhost"
port = "8080"
url_id = "http://"+servername+":"+port+"/JSON/alert/view/alertsByRisk/?url=&recurse="
url_source_id="http://"+servername+":"+port+"/JSON/alert/view/alert/"
url_har="http://"+servername+":"+port+"/OTHER/exim/other/exportHarById/"


# Возьмём нужные id
response = requests.get(url_id)
content = response.json()

# многоуровневый прасинг
for lvl in content["alertsByRisk"]:
    for x in lvl:
        try:
            for lvl2 in lvl[x]:
                for lvl3 in lvl2:
                    for lvl4 in lvl2[lvl3]:
                        ids.append(lvl4["id"])
                    
        except:
            pass 




"id","sourceid","messageId", "method","description","url","param","risk","alert","alertRef","method"



# для нашего удобства будем подтягивать по каждому id инфмормацию, а не сразу по всем
for id in ids:
    content = requests.get(url_source_id,params={"id":id}).json()["alert"]
    sourceid = content["sourceid"]
    method = content["method"]
    description = content["description"]
    url = content["url"]
    param = content["param"]
    risk = content["risk"]
    alert = content["alert"]
    alertRef = content["alertRef"]
    method = content["method"]
    messageId = content["messageId"]

    array.append({"id":id,"sourceid":sourceid,"messageId":messageId, "method":method,"description":description,"url":url,"param":param,"risk":risk,"alert":alert,"alertRef":alertRef,"method":method})

    # TODO запрос в бд на наличие false-positive записи
    # место для будущего запроса в бд


    # место для будущего запроса в бд

    # если не нашли запись в бд возьмём и сохраним har
    har = requests.get(url_har,params={"ids":sourceid}).json()['log']['entries'][0]["request"]
    har_array[id] = har

# array - массив с уязвимостями для базы данных

# har_array - массив с request запросами в json, где первый параметр - id, который был в начале

print("Массив с уязвимостями: ")
print(array)
print()
print("Массив с har: ")
print(har_array)


# Пример вывода

# Массив с уязвимостями: 
# [{'id': '0', 'sourceid': '1', 'messageId': '177', 'method': 'GET', 'description': 'SQL injection may be possible.', 'url': 'https://0ae900380394fd51839b14e3000900d8.web-security-academy.net/product?productId=18', 'param': 'productId', 'risk': 'High', 'alert': 'SQL-инъекция - Oracle  - Time Based', 'alertRef': '40021'}]

# Массив с har:
# {'0': {'method': 'GET', 'url': 'https://0ae900380394fd51839b14e3000900d8.web-security-academy.net/product?productId=6', 'httpVersion': 'HTTP/1.1', 'cookies': [], 'headers': [{'name': 'host', 'value': '0ae900380394fd51839b14e3000900d8.web-security-academy.net'}, {'name': 'user-agent', 'value': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'}, {'name': 'pragma', 'value': 'no-cache'}, {'name': 'cache-control', 'value': 'no-cache'}], 'queryString': [{'name': 'productId', 'value': '6'}], 'postData': {'mimeType': '', 'params': [], 'text': ''}, 'headersSize': 304, 'bodySize': 0}}