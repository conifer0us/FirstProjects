from urllib import response
import requests

api_key = "RDZMUENDYlg2bFJabVFRUzl1OTdzQ3FQMkVGMjpmNnB1OHUwNmJndDlzYjlmdDY3eWU="
headers = {}
headers["Authorization"] = api_key
response = requests.get("http://api.horseapi.com/races/FG/%s" % input("Race Number: "), headers=headers)
jsonData = response.json()

print("\n")
for otherelement in jsonData: 
    if not hasattr(jsonData[otherelement], "__iter__") or isinstance(jsonData[otherelement], str):
        print("%s : %s" % (otherelement, jsonData[otherelement]))

print("\n")
for element in jsonData["runners"]:
    for key in element: 
        print("%s : %s" % (key, element[key]))
    print("\n")