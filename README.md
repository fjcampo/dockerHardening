# dockerHardening
This repository contain the files mentioned in the paper: Exploring Solutions for Application Container Security in Common Use Containers 
Written by Frank Campo and Howe Wang

* _dockerWriter.py_ is a Python script proof-of-concept for automating the patching of off-the-shelf (OTS) images from Docker Hub.
  * You must have Docker Desktop and python 3.x.x installed
 
* _patchableAndunpatchableVulns.xlsx_ shows the output of Trivy scans on OTS images when filtering for only vulnerabilities

* _patchablevulns.xlsx_ shows the output of Trivy scans on OTS images when filtering for only vulnerabilities with known fix versions
 
* _hardenedPatachableAndUnpatchableVulns.xlsx_ shows the results of our manual patching attempts of vulnerabilities in the OTS images
