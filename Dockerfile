FROM python

WORKDIR /task_manager

ENV TERM=xterm

COPY requirements.txt ./

COPY /task_manager ./

RUN pip install -r requirements.txt