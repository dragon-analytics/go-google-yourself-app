FROM r-base:latest

MAINTAINER Alfredo Méndez <actuario.alfredo.mb@gmail.com>

ENV REFRESHED_AT 2017-045-21

RUN apt-get update

RUN apt-get -y install python

RUN apt-get -y install python-pip

# RUN apt-get -y install git-core
# git clone https://github.com/adfmb/vis4googleT.git
# RUN apt-get -y install nano


## Requerimientos
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

##### La parte de R


RUN apt-get update && apt-get install -y \
    sudo \
    gdebi-core \
    pandoc \
    pandoc-citeproc \
    libcurl4-gnutls-dev \
    libcairo2-dev/unstable \
    libxt-dev \
    libssl-dev \
    unzip

# Download and install shiny server
RUN wget --no-verbose https://s3.amazonaws.com/rstudio-shiny-server-os-build/ubuntu-12.04/x86_64/VERSION -O "version.txt" && \
    VERSION=$(cat version.txt)  && \
    wget --no-verbose "https://s3.amazonaws.com/rstudio-shiny-server-os-build/ubuntu-12.04/x86_64/shiny-server-$VERSION-amd64.deb" -O ss-latest.deb && \
    gdebi -n ss-latest.deb && \
    rm -f version.txt ss-latest.deb

RUN apt-get install -y libcurl4-openssl-dev


RUN R -e "install.packages(c('shiny','shinydashboard','RCurl','ggplot2','rmarkdown'), repos='http://cran.rstudio.com/')"

COPY shiny-server.conf  /etc/shiny-server/shiny-server.conf
COPY /app /srv/shiny-server/

EXPOSE 3838

COPY shiny-server.sh /usr/bin/shiny-server.sh

CMD ["/usr/bin/shiny-server.sh"]



