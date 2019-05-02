FROM python:3.6

ARG project_dir=/projects/

ADD ./requirements.txt $project_dir
ADD ./.env $project_dir

WORKDIR $project_dir
CMD mkdir src

RUN pip install -r requirements.txt