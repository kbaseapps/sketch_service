FROM python:3.7-slim-stretch

ARG DEVELOPMENT

# Install the mash binary
WORKDIR /opt
RUN apt-get update && apt-get install -y curl && \
    curl -LJO  https://github.com/marbl/Mash/releases/download/v2.0/mash-Linux64-v2.0.tar && \
    tar xvf mash-Linux64-v2.0.tar && \
    rm mash-Linux64-v2.0.tar && \
    ln -s /opt/mash-Linux64-v2.0/mash /usr/bin/mash && \
    apt-get remove -y curl && apt-get autoremove -y && \
    /usr/bin/mash

# Install dependencies
WORKDIR /kb/module
COPY requirements.txt /kb/module/requirements.txt
COPY dev-requirements.txt /kb/module/dev-requirements.txt
WORKDIR /kb/module
RUN pip install --upgrade pip && \
    pip install pandas==0.24.1 && \
    pip install --upgrade -r requirements.txt \
      kbase-workspace-client==0.2.1 && \
    pip install --extra-index-url https://pypi.anaconda.org/kbase/simple \
      kbase_cache_client==0.0.2 && \
    if [ "$DEVELOPMENT" ]; then pip install -r dev-requirements.txt; fi

# Run the server
COPY . /kb/module
COPY .env.example /kb/module/.env
RUN chmod -R a+rw /kb/module
EXPOSE 5000
ENTRYPOINT ["sh", "/kb/module/entrypoint.sh"]
