# downEpstein
a downloader for the Epstein Files.

heavily inspired on and works off of the work from Surebob's [epstein-files-downloader](https://github.com/Surebob/epstein-files-downloader).
this piggybacks directly off of requests without the necessity of aria2c and downloads not only the PDF files but also any videos in the datasets.
Currently known video extensions are `.mp4`, `.mov` and `.m4a`. If you know any other extensions, open an issue on this repository so it can be added.

---
# Installation
```bash
$ git clone https://github.com/shodanwashere/downEpstein.git
$ cd downEpstein
$ python3 -m venv ./env
$ source ./env/bin/activate
$ pip3 install -r requirements
$ chmod +x ./downEpstein.py
```

# Usage
```bash
$ source ./env/bin/activate
$ ./downEpstein.py <dataSetNumber> <startingID> <endingID> <outputPath> [-v|--verbose]
```
Arguments:
- `dataSetNumber` : number of the dataset you're downloading files from.
- `startingID` : ID number of the first file you want to download from.
- `endingID`: ID number of the last file you want to download.
- `outputPath`: Where the files should be downloaded to. I recommend getting an external drive for this.
- `-v` `--verbose` : (Optional) Turn on verbose mode.

# My Final Message.
I love my family. I love my wife.
I am mentally stable and do not have suicidal ideation.
If I ever disappear during this pivotal historical moment,
I was not taken by my own hand.
They're the ones who fear your resistance.
