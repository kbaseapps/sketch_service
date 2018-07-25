FROM python:3.7-stretch

# TODO install mash in /usr/bin
# https://github.com/marbl/Mash/releases

WORKDIR /kb/module

# Install pip dependencies
COPY ./requirements.txt /kb/module/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /kb/module
RUN chmod -R a+rw /kb/module
RUN chmod +x /kb/module/entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
CMD []
