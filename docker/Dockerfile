FROM ubuntu:18.04

RUN apt-get update && apt-get install -y vim wget curl git tcsh

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh -O ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p /miniconda
ENV PATH="/miniconda/bin:$PATH"

# get env file seperately so it doesn't reinstall every time
COPY ./env.yaml /pecgs-druggability/env.yaml
RUN conda env create --file /pecgs-druggability/env.yaml 

COPY . /pecgs-druggability

ENV PATH="/miniconda/envs/druggability/bin:/miniconda/bin"

CMD /bin/bash
#ENTRYPOINT ["/bin/bash", "-c"]
