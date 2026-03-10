#!/usr/bin/env python3
import requests
import argparse
import os
from tqdm import tqdm
import threading
import time

def banner(arguments):
    banner = """
     __   __                ___  __   __  ___  ___        
    |  \\ /  \\ |  | |\\ |    |__  |__) /__`  |  |__  | |\\ | 
    |__/ \\__/ |/\\| | \\|    |___ |    .__/  |  |___ | | \\| 
                                                          
    """
    print(banner)
    print("============================================================")
    print(":: Arguments")
    print(":: Starting ID   : "+str(arguments.startingID))
    print(":: Ending ID     : "+str(arguments.endingID))
    print(":: Downloading to: "+str(arguments.downloadPath))
    if arguments.verbose:
        print(":: Verbose Mode ON")
    print("============================================================")

def configure_directories(downloadPath, verbosity):
    if not os.path.exists(downloadPath):
        if verbosity:
            print(":: "+downloadPath+" does not exist. Creating...")
        os.makedirs(downloadPath)

    if not os.path.exists(os.path.join(downloadPath,'IMAGES')):
        if verbosity:
            print(":: "+os.path.join(downloadPath,'IMAGES')+" does not exist. Creating...")
        os.makedirs(os.path.join(downloadPath,'IMAGES'))

    if not os.path.exists(os.path.join(downloadPath,'VIDEOS')):
        if verbosity:
            print(":: "+os.path.join(downloadPath,'VIDEOS'))
        os.makedirs(os.path.join(downloadPath,'VIDEOS'))
    if verbosity:
        print(":: File system ready.")

def download_files_single(args):
    startingID = int(args.startingID)
    endingID = int(args.endingID)
    dataSetNumber = args.dataSetNumber
    downloadPathBase = args.downloadPath
    downloadPathImages = os.path.join(downloadPathBase,'IMAGES')
    downloadPathVideos = os.path.join(downloadPathBase,'VIDEOS')
    verbosity = args.verbose
    numberOfFiles = (endingID - startingID) + 1
    if verbosity:
        print(":: Downloading "+str(numberOfFiles)+" files to "+downloadPathBase)
    currentID = startingID
    possibleExtensionsImages = [".pdf"]
    possibleExtensionsVideos = [".mp4", ".m4a", ".mov"]
    possibleExtensions = possibleExtensionsImages + possibleExtensionsVideos
    s = requests.Session()
    s.headers.update({
            "Cookie": "justiceGovAgeVerified=True",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })
    for i in tqdm(range(numberOfFiles)):
        downloaded = False
        for e in possibleExtensions:
            if downloaded:
                break
            filename = f'EFTA{currentID:08d}{e}'
            url = 'https://www.justice.gov/epstein/files/DataSet%20'+dataSetNumber+'/'+filename
            r = s.get(url)
            if r.status_code == 200:
                savePath = ""
                if e in possibleExtensionsImages:
                    savePath = os.path.join(downloadPathImages,filename)
                elif e in possibleExtensionsVideos:
                    savePath = os.path.join(downloadPathVideos,filename)
                else:
                    savePath = os.path.join(downloadPath,filename)
                with open(savePath,'wb') as fd:
                    fd.write(r.content)
                downloaded = True
                if verbosity:
                    print(":: Downloaded "+filename)
        currentID += 1

def download_files_mt(args, t, fdown, tf):
    startingID = int(args.startingID) + t
    endingID = int(args.endingID)
    threadc = int(args.threads)
    dataSetNumber = args.dataSetNumber
    downloadPathBase = args.downloadPath
    downloadPathImages = os.path.join(downloadPathBase,'IMAGES')
    downloadPathVideos = os.path.join(downloadPathBase,'VIDEOS')
    verbosity = args.verbose
    currentID = startingID
    possibleExtensionsImages = [".pdf"]
    possibleExtensionsVideos = [".mp4", ".m4a", ".mov"]
    possibleExtensions = possibleExtensionsImages + possibleExtensionsVideos
    numberOfFiles = endingID - startingID
    if verbosity:
        print(f'[{t}] Thread started')
    s = requests.Session()
    s.headers.update({
            "Cookie": "justiceGovAgeVerified=True",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })
    for i in range(0, numberOfFiles, threadc):
        print(f'[{t}] === {currentID} ===')
        downloaded = False
        for e in possibleExtensions:
            time.sleep(threadc)
            if downloaded:
                break
            filename = f'EFTA{currentID:08d}{e}'
            url = 'https://www.justice.gov/epstein/files/DataSet%20'+dataSetNumber+'/'+filename
            r = s.get(url)
            if r.status_code == 200:
                savePath = ""
                if e in possibleExtensionsImages:
                    savePath = os.path.join(downloadPathImages,filename)
                elif e in possibleExtensionsVideos:
                    savePath = os.path.join(downloadPathVideos,filename)
                else:
                    savePath = os.path.join(downloadPath,filename)
                with open(savePath,'wb') as fd:
                    fd.write(r.content)
                downloaded = True
                fdown += 1
                if verbosity:
                    print(f'[{t}] Downloaded {filename} :: ({fdown}/{tf})')
        currentID += threadc


def main():
    parser = argparse.ArgumentParser(
        prog='downEpstein',
        description='Downloads files from the Epstein Library DataSets',
        epilog='shodan - 2026 - THEY LIKE TO PUSH THE WEAK AROUND'
    )

    parser.add_argument('dataSetNumber',help="Number of data set")
    parser.add_argument('startingID',help="ID of the first file in the set")
    parser.add_argument('endingID',help="ID of the last file in the set")
    parser.add_argument('downloadPath',help="Path to which files should be downloaded")
    parser.add_argument('-v','--verbose',action='store_true',help="Activate verbose mode")
    parser.add_argument('-t','--threads',const=0,help="Number of worker threads to spawn (default 0)", type=int, nargs='?')

    args = parser.parse_args()
    threadc = int(args.threads)
    banner(args)
    configure_directories(args.downloadPath, args.verbose)
    if threadc > 0:
        filesDownloaded = 0
        totalFiles = int(args.endingID) - int(args.startingID) + 1
        threads = []
        for i in range(threadc):
            t = threading.Thread(target=download_files_mt,args=(args,i,filesDownloaded,totalFiles))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    else:
        download_files_single(args)

if __name__=='__main__':
    main()

