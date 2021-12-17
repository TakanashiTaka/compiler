FROM python:3
WORKDIR /app/
RUN mkdir myCompiler
COPY myCompiler/* /myCompiler/