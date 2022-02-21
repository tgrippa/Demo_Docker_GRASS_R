### DESCRIPTION of DOCKERFILE 
## Base image: Ubuntu Focal (20.04); 
## Softwares: Python3, Jupyter Lab, R, GRASS GIS  

# Use ubuntu:focal as base image 
FROM ubuntu:focal

LABEL maintainer="tais.grippa@ulb.be"

ARG DEBIAN_FRONTEND=noninteractive

# Add user
RUN useradd -ms /bin/bash demo_user

# Update & upgrade system
RUN apt-get -y update && \
    apt-get -y upgrade
RUN apt-get install -y --no-install-recommends apt-utils wget dbus

# Setup locales
RUN apt-get install -y locales
RUN echo LANG="en_US.UTF-8" > /etc/default/locale
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install Python, Numpy, Scipy, Pandas, Rpy2 and Jupyter(lab)
RUN apt-get install -y --no-install-recommends \
        python3 \
        python3-numpy \
        python3-scipy \
        python3-pandas \
        python3-rpy2 \
        python3-pip \
        jupyter
RUN pip install jupyterlab
ENV JUPYTER_ENABLE_LAB=yes
ENV PATH="$HOME/.local/bin:$PATH"

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

# Install R software ('dev' package to allow compilation of Rpackages to be installed such as randomForest)
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/" | tee -a /etc/apt/sources.list
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
RUN apt-get update
RUN apt-get install -y --no-install-recommends r-base-dev

# Install GRASS GIS
# A compiling environment is needed to install GRASS extensions, 
# along with GRASS development files
RUN apt-get install -y --fix-missing \
        wget \
        software-properties-common \
        build-essential
RUN add-apt-repository -y ppa:ubuntugis/ppa && \
    apt-get -y update
RUN apt-get -y install \
        grass=7.8.6-1~focal1 \
        grass-doc \
        grass-dev \
        grass-dev-doc \
        grass-gui

# Reduce image size
RUN apt-get autoremove -y && \
    apt-get clean -y
	
# Install all R packages required for GRASS' v.class.mlR
RUN R -e "install.packages('doParallel',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('caret',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('e1071',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('data.table',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('kernlab',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('randomForest',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('ranger',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('dplyr',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('rpart',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('xgboost',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('plyr',dependencies=TRUE, repos='http://cran.rstudio.com/')"
	
USER demo_user
WORKDIR /home/demo_user

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
