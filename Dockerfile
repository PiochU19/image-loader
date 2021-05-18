###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.5-alpine as builder

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install Pillow dependencies
RUN apk --no-cache add jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
        harfbuzz-dev \
        fribidi-dev
RUN apk add libpng-dev tiff-dev libjpeg gcc libgcc musl-dev
RUN apk add jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# lint
RUN pip install --upgrade pip
COPY . .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/backend/wheels -r requirements.txt

##############
# PRODUCTION #
##############

# pull official base image
FROM python:3.9.5-alpine

# create directory for the image user
RUN mkdir -p /home/image

# create the image user
RUN addgroup -S image && adduser -S image -G image

# create the appropriate directories
ENV HOME=/home/image
ENV IMAGE_HOME=/home/image/backend
RUN mkdir $IMAGE_HOME
RUN mkdir $IMAGE_HOME/media
RUN mkdir $IMAGE_HOME/static
WORKDIR $IMAGE_HOME

# install Pillow dependencies
RUN apk --no-cache add jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
        harfbuzz-dev \
        fribidi-dev
RUN apk add libpng-dev tiff-dev libjpeg gcc libgcc musl-dev
RUN apk add jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN pip install Pillow

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/backend/wheels /wheels
COPY --from=builder /usr/src/backend/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh $IMAGE_HOME

# copy project
COPY . $IMAGE_HOME

# chown all the files to the image user
RUN chown -R image:image $IMAGE_HOME

# change to the image user
USER image

# run entrypoint.sh
ENTRYPOINT ["/home/image/backend/entrypoint.sh"]