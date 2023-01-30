FROM alpine

WORKDIR /

RUN apk update
RUN apk add nano git
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add build-base linux-headers
RUN apk add --no-cache py3-pip

# Create a group and user
RUN addgroup -S cine && adduser -D -S mvpk -G cine
# use the new user
USER mvpk

RUN apk add vlc

RUN python --version

WORKDIR /movie_picker
COPY . .

#WORKDIR /
RUN python3 -m venv venv

WORKDIR /movie_picker
RUN . venv/bin/activate

RUN pip install -r requirements.txt

EXPOSE 52001
ENTRYPOINT ["./hello.py"]

# - - TO build
# cd repos
# git clone https://github.com/UnacceptableBehaviour/movie_picker
# cd movie_picker
# docker build . -t moviepicker

# - - 1st run container with 
# docker run \
# -e FLASK_DEBUG=1 -e TEMPLATES_AUTO_RELOAD=1 -e FLASK_APP=hello.py \
# --name mvpicker --rm \
# -p 52001:52001 \
# moviepicker

# stop / start container (after first run)
# docker start mvpicker
# docker stop mvpicker

# view site @ http://127.0.0.1:52001/ or http://127.0.0.1:52001/slider_tests



# TODO - issur with --mount ?? 
# docker run \
# -e FLASK_ENV=development -e FLASK_APP=hello.py \
# --name mvpicker \
# -p 52001:52001 \
# --mount type=bind,source="demoVidLib",target="demoVidLib" \
# moviepicker
#
# docker: Error response from daemon: invalid mount config for type "bind": invalid mount path: 'demoVidLib' mount path must be absolute.

