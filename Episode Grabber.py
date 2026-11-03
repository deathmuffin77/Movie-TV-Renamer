'''

            Given movie/tv episode file,(ex. 12590266-cyberpunk-edgerunners-2022.S2.E8.1080p
            or 10377864-beware-boiuna-2026) returns cleaned up file name with episode title
            (ex. "Cyberpunk Edgerunners (2022) S2 Ep8 Heart / Shinzô" or "Beware Boiuna (2026)")

'''
import requests
import os
import http.client
from pathlib import Path
import json

def fileNameDecoder(fileName): #returns IMDB ID, Season num, Episode num
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
   
   if episodeJSONpath.is_file():
        print("JSON Exists...")
        print(episodeJSONpath)
        useAPI= False
        return episodeJSONpath
   else:
        useAPI= True
   if useAPI:
        print("Creating JSON File...")
        conn = http.client.HTTPSConnection("imdb255.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': "APIKEY",
            'x-rapidapi-host': "imdb255.p.rapidapi.com"
        }

        conn.request("GET", "/title/episodes?title_id=tt"+TVID+"&season="+season, headers=headers)

        res = conn.getresponse()
        data = res.read()
        
        with open(f'C:/Users/Ian/Desktop/Title Grabber/Logs/{fileName}', 'w') as f:
                    f.write(data.decode("utf-8"))
        print(episodeJSONpath)
        return episodeJSONpath

def checkIfShow (fileName):  #checks if TV show or movie, show=True
    for char in range(len(fileName)):
     if char<=9:
      continue
     if (fileName[char]=="." and fileName[char+1]=="S"):
        return True

def getEpisodeTitle(episodeJSONpath, episode): #queries JSON file for episode title and returns it
    
    with open(episodeJSONpath, 'r') as f:
        d = json.load(f)
    #title=d["results"][int(episode)-1]["title"]
    results = d["results"]
    for e in range(len(results)):
     if results[e]["episode"]==int(episode):
        return (results[e]["title"])
    return title

def movieRename(fileName): #renames movie files
    newNameList=[]
    year=""
    for char in range(len(fileName)):
      if(char<=8 and fileName[char].isalnum()==True):
        continue
      if fileName[char].isalpha():
        if fileName[char-1].isalpha():
            newNameList.append(fileName[char]) 
        else:
            newNameList.append(fileName[char].upper())
      elif fileName[char]=="-":
        newNameList.append(" ")
      elif fileName[char+4] =="[":
        year="("+fileName[char:char+4]+")"
        break
      elif fileName[char].isdigit():
        newNameList.append(fileName[char])
    newName="".join(newNameList)+year
    return newName

def tvRename(fileName, episodeTitle): #renames TV files
    newNameList=[]
    newNameList2=[]
    year=""
    yearFloat=True
    for char in range(len(fileName)):
      if(char<=9):
        if fileName[char+1].isalpha()==False:
         continue
      if fileName[char].isalpha() and yearFloat==True:
        if fileName[char-1].isalpha():
          newNameList.append(fileName[char]) 
        else:
          newNameList.append(fileName[char].upper())
      elif fileName[char]=="-":
        newNameList.append(" ")
      elif fileName[char+4] =="." and fileName[char+5] =="S":
        year="("+fileName[char:char+4]+")"
        yearFloat=False
        newNameList2.append("S"+fileName[char+6])
        if fileName[char+7].isdigit():
         newNameList2.append(fileName[char+7])
      elif (fileName[char]=="." and fileName[char+1]=="E"): # Episode# Grabber
         newNameList2.append(" Ep"+fileName[char+2])
         if fileName[char+3].isdigit()==True:
          newNameList2.append(fileName[char+3])            
         break
        
      elif fileName[char].isdigit() and yearFloat==True:
        newNameList.append(fileName[char])
    episodeTitle1=""
    for i in range(len(episodeTitle)):
     if episodeTitle[i]!="/":
        episodeTitle1=episodeTitle1+episodeTitle[i]
        
    newName="".join(newNameList)+year+" "+"".join(newNameList2)+" "+episodeTitle1
    print(newName)
    return (newName)


def main():
    folderpath=Path(f'C:/Users/Ian/Desktop/Title Grabber/Renamer/')
    for file in folderpath.iterdir():
        print(file.stem)
    for file in folderpath.iterdir():
        fileName=file.stem
        imdbID, sNum, epNum = fileNameDecoder(fileName)
        if checkIfShow(fileName):
         array=tvRename(fileName, getEpisodeTitle(createJSON(imdbID,sNum), epNum))
         file.rename(Path(file.parent, f"{array}{file.suffix}"))
        else:
         array=movieRename(fileName)
         file.rename(Path(file.parent, f"{array}{file.suffix}"))
    for file in folderpath.iterdir():
     print(file.stem)
    
main()
'''
'''