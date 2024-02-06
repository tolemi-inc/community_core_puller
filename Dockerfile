#CONTAINER TEMPLATE
FROM python:3.9-slim-bookworm

RUN echo $PATH

WORKDIR /opt/community_core_puller

#install requirements
COPY requirements.txt /opt/community_core_puller
RUN pip install -r requirements.txt

# copy the script
COPY community_core_puller /opt/community_core_puller/

# add the script callers to path
ENV PATH="/opt/community_core_puller/bin:$PATH"