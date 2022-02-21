# Demo Docker with _GRASS_,_R_ and _JupyterLab_

This repository has been created by [Taïs Grippa](https://tgrippa.github.io/) and contains the material for a demonstration on how to use Docker for running Geospatial analysis using GRASS GIS and R with Jupyter Notebooks.


## Instructions
### Requirements
- You need to have Docker installed on the host computer (for most of you, it will be your own computer, but it could be a server machine for example). Ensure Docker is installed by typing ``` bash docker --version ``` in your terminal. If the version is not displayed, please install Docker according to [the official help](https://docs.docker.com/get-docker/).
- You need to have Git/github installed (not mandatory if you use direct download from Github website). 

### Open a terminal window and navigate to a directory where you will work.

### Download the "NorthCarolina" dataset for this demo
```
# Create a GRASSDATA folder and enter it. 
mkdir GRASSDATA
cd GRASSDATA
# Download from the GRASS GIS website
wget https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip
# Unzip in the same folder
unzip nc_basic_spm_grass7.zip
# Remove zip file. 
rm nc_basic_spm_grass7.zip
# Change directory
cd ..
```

### Clone this repository
Clone this repository on your computer using the following git command or using the direct download [link](https://github.com/tgrippa/Demo_Docker_GRASS_R/archive/refs/heads/main.zip).
```
# Clone repository
git clone https://github.com/tgrippa/Demo_Docker_GRASS_R.git
```

### Build the Docker image
Now it is time to build the Docker image you will use for running the code.
Be patient, the building may take a while but it is just needed once.
The image will be named "demo_image" and the version tag will be "grass786", because of the version of GRASS GIS 7.8.6 which will come with.
```
# Change directory
cd Demo_Docker_GRASS_R/
# Build the Docker image based on the Dockerfile
docker build -t demo_image:grass786 .
# Change directory
cd ..
```

### Run a new Docker instance (a container) based on this image
Run a new docker instance based on the demo_image:grass786 image. After executing the docker command,
you should have a Jupyter lab server running in the Docker instance.
Click the IP address of the service and a new tab will appear in your web browser.
```
# Run a new Docker container named "test_container"
docker run -p 8888:8888 -v ${PWD}/Demo_Docker_GRASS_R:/home/demo_user/Workshop -v ${PWD}/DockerResults:/home/demo_user/output_container -v ${PWD}/GRASSDATA:/home/demo_user/GRASSDATA -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --name test_container demo_image:grass786
```

### Launch the Graphical User Interface of GRASS running in the container
Launch GRASS GIS graphical user interface **in another terminal**. Be careful this not work if you are in root mode.
```
# Open a bash terminal on the running instance named "test_container"
docker exec -it test_container bash
test_container@CONTENER_ID:~$ grass -gui

```

### Bash shell with root (sudo) privilege in the container
If you need a root access to the running instance, use the following command. Be careful you would not be able to launch the GUI properly when you are in root. 
```
# If you need to use the bash with root privilege (sudo)
docker exec --user="root" -it test_container bash

```