FROM python:3
WORKDIR /app/
COPY ./* /app/
RUN ls -l
RUN echo "dockerfile!"