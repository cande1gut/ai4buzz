#FROM python:3.9
#FROM nvidia/cuda:11.0-base
#FROM nvidia/cuda:11.4.3-base-ubuntu20.04
#FROM nvidia/cuda:11.4.3-devel-ubuntu20.04
FROM nvidia/cuda:11.4.3-cudnn8-devel-ubuntu20.04
ENV TZ=America/New_York

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY ./api /app/api

COPY ./object_detection /app/object_detection

# RUN apt clean
RUN apt update
RUN apt-get -y install tesseract-ocr libgl1 python3-pip python3-dev libpq-dev
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade --no-cache-dir -r /app/api/requirements.txt

#CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
