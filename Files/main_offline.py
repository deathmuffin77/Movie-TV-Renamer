import requests
import os
import http.client
from pathlib import Path
import json

def fileNameDecoder(fileName): 
    imdbID=""
    sNum=""
    epNum=""
    for char in fileName:
     if char=="-":
      break
     imdbID=imdbID+char
    for char in range(len(fileName)):
     if char<=9:
      continue
     if (fileName[char]=="." and fileName[char+1]=="S"): # Season# Grabber
      sNum=fileName[char+2]
      if fileName[char+3].isdigit()==True:
       sNum=sNum+fileName[char+3]
     if (fileName[char]=="." and fileName[char+1]=="E"): # Episode# Grabber
      epNum=fileName[char+2]
      if fileName[char+3].isdigit()==True:
       epNum=epNum+fileName[char+3]     
      
    return imdbID,sNum,epNum

   
def createJSON(TVID,season): #checks if show's season JSON exists, if doesn't pulls from API, returns JSON path
   fileName=TVID+"season"+season+".json"

   episodeJSONpath=(Path("/Users/Ian/Desktop/Title Grabber/Logs/"+fileName))
   print(episodeJSONpath)
   if episodeJSONpath.is_file():
        print("Exists")
        useAPI= False
        return episodeJSONpath
   else:
        useAPI= True
   if useAPI==True:
        conn = http.client.HTTPSConnection("imdb255.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': "cd36dda17amshc34d5f089f9ff6ep1bb94ejsn5c13b289d19a",
            'x-rapidapi-host': "imdb255.p.rapidapi.com"
        }

        conn.request("GET", "/title/episodes?title_id=tt"+TVID+"&season="+season, headers=headers)

        res = conn.getresponse()
        data = res.read()
        
        with open(f'C:/Users/Ian/Desktop/Title Grabber/Logs/{fileName}', 'w') as f:
                    f.write(data.decode("utf-8"))
        return episodeJSONpath

def getEpisodeTitle(episodeJSONpath, episode): #queries JSON file for episode title and returns it
    
    with open(episodeJSONpath, 'r') as f:
        d = json.load(f)
    results=d["results"]
    #return d["results"][int(episode)-1]["title"]
    for e in range(len(results)):
     if results[e]["episode"]==int(episode):
        return (results[e]["title"])
    
fileName="16098700-fire-country-2022.S2.E10.1080p"
imdbID, sNum, epNum = fileNameDecoder(fileName)
print(getEpisodeTitle(createJSON(imdbID,sNum), epNum))