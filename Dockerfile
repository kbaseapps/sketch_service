FROM python:3.7-stretch

WORKDIR /opt

RUN curl -LJO  https://github.com/marbl/Mash/releases/download/v2.0/mash-Linux64-v2.0.tar \
    && tar xvf mash-Linux64-v2.0.tar \
    && rm mash-Linux64-v2.0.tar \
    && ln -s /opt/mash-Linux64-v2.0/mash /usr/bin/mash

WORKDIR /kb/module

# Install pip dependencies
COPY ./requirements.txt /kb/module/requirements.txt
RUN pip install --upgrade pip -r requirements.txt && \
    pip install --extra-index-url https://pypi.anaconda.org/kbase/simple \
        kbase-workspace-utils==0.0.5

COPY . /kb/module
RUN chmod -R a+rw /kb/module
RUN chmod +x /kb/module/entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
CMD []
