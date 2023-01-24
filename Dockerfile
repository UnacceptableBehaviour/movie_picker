FROM alpine

WORKDIR /

RUN apk update
RUN apk add nano git
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add build-base linux-headers
RUN apk add --no-cache py3-pip

RUN python --version

WORKDIR /movie_picker
COPY . .

RUN python -m venv venv

RUN . venv/bin/activate

RUN pip install -r requirements.txt

EXPOSE 52001
ENTRYPOINT ["./hello.py"]

# build
# cd repos
# git clone https://github.com/UnacceptableBehaviour/movie_picker
# cd movie_picker
# docker build . -t moviepicker

# run with (network not quite right yet)
# docker run \
# -e FLASK_ENV=development -e FLASK_APP=hello.py \
# --name mvpicker \
# --network=host \
# -p52001:52001 \
# --mount type=bind,source="demoVidLib",target=demoVidLib \
# moviepicker
