import docker
import os
import subprocess
import json

def main():

    imageToBuild = input("Please enter the name of the image you want to build/harden\n(e.g., node:latest)\n")
    imagename = imageToBuild + "-hardened"

    #1 run trivy scan initially
    trivyresults = runTrivyScan(imageToBuild)

    #2 fill dockerfile with fixes based on OS type
    createDockerfile(imageToBuild, trivyresults)

    #3 build image
    buildImage(imagename)

    #4 rerun trivy on image
    runTrivyScan(imagename)

    quit()

def runTrivyScan(image):
    trivycommand = "docker run -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/Library/Caches:/root/.cache/ aquasec/trivy:latest -f json -q image --ignore-unfixed --scanners vuln " + image

    process = subprocess.Popen(trivycommand, stdout=subprocess.PIPE, shell=True)
    print(f"Running Trivy scan on {image}")
    (output, err) = process.communicate()  
    p_status = process.wait()

    outputjson = json.loads(output.decode("utf-8"))

    if err is None:
        print("Command output: ", outputjson["Results"])
        return outputjson["Results"]
    else:
        print("ERROR: " + err.decode("utf-8"))
        quit(1)

def createDockerfile(imageToBuild, trivyresults):
    print("Creating Dockerfile for hardened image")

    vulns = set()

    for object in trivyresults:
        if "Vulnerabilities" in object:
            for vuln in object["Vulnerabilities"]:
                vulns.add(vuln["PkgName"])
    
    file = open("./dockerbuild/Dockerfile", "w")
    file.write(f"FROM {imageToBuild}\n\n")

    imageOS = trivyresults[0]["Type"]
    if imageOS == 'debian' or imageOS == 'ubuntu':
        cmd = "apt-get -y install"
        file.write("RUN apt update\n")
    elif imageOS == 'alpine':
        cmd = "apk upgrade"
        file.write("RUN apk update\n")
    elif imageOS == 'oracle':
        cmd = "yum install"
        file.write("RUN yum update\n")
    else:
        raise Exception("not a recognized OS type")

    for vuln in vulns:
        file.write(f"RUN {cmd} {vuln}\n")

    file.close()

def buildImage(imagename):
    print("Building hardened image")
    client = docker.from_env()

    client.images.build(
        path = "./",
        dockerfile = "./dockerbuild/Dockerfile", 
        tag = imagename)


if __name__ == "__main__":
    main()
