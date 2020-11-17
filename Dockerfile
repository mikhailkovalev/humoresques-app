FROM python:3.6-slim
RUN mkdir /humoresques-app \
  && mkdir /humoresques-app/dis_test \
  && mkdir /humoresques-app/humoresques
COPY manage.py \
     project_conf.yaml \
     requirements.txt \

     # fixme: bad practic
     db.sqlite3 \

     # destination in container
     /humoresques-app/
COPY dis_test/* /humoresques-app/dis_test/
COPY humoresques/* /humoresques-app/humoresques/
RUN pip install -r /humoresques-app/requirements.txt
WORKDIR /humoresques-app/
