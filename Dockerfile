FROM python:3.7-alpine

ARG DEVELOPMENT

# Install the mash binary
WORKDIR /opt
RUN apk --update add --virtual build-dependencies curl tar && \
    curl -LJO  https://github.com/marbl/Mash/releases/download/v2.0/mash-Linux64-v2.0.tar && \
    tar xvf mash-Linux64-v2.0.tar && \
    rm mash-Linux64-v2.0.tar && \
    ln -s /opt/mash-Linux64-v2.0/mash /usr/bin/mash && \
    apk del build-dependencies

# Install dependencies
WORKDIR /kb/module
COPY requirements.txt /kb/module/requirements.txt
COPY dev-requirements.txt /kb/module/dev-requirements.txt
WORKDIR /kb/module
RUN apk --update add --virtual build-dependencies python-dev build-base && \
    pip install --upgrade pip && \
    pip install --upgrade --no-cache-dir -r requirements.txt && \
    pip install --extra-index-url https://pypi.anaconda.org/kbase/simple \
      kbase-workspace-utils==0.0.11 && \
    if [ "$DEVELOPMENT" ]; then pip install -r dev-requirements.txt; fi && \
    apk del build-dependencies

# Run the server
COPY . /kb/module
COPY .env.example /kb/module/.env
RUN chmod -R a+rw /kb/module
EXPOSE 5000
ENTRYPOINT ["sh", "/kb/module/entrypoint.sh"]
