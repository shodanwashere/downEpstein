#!/usr/bin/env python3
import requests
import argparse
import os
from tqdm import tqdm

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

def download_files(args):
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
