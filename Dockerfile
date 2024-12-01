FROM python

WORKDIR /src

ENV TERM=xterm

COPY requirements.txt ./

COPY /src ./

RUN pip install -r requirements.txt