FROM python:3.6.15-slim-buster

WORKDIR /app
COPY ./ /app
RUN apt update \
  && apt upgrade -y \
  && apt install -y libsm6 libxrender1 libfontconfig1 libice6 libopencv-dev
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
