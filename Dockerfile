FROM node:14-bullseye-slim AS webpack
WORKDIR /webpack
COPY package.json ./package-lock.json ./webpack.config.js ./
RUN npm i
COPY ./assets ./assets
RUN npm run build

FROM python:3.9.9-bullseye AS python_main
ENV PYTHONUNBUFFERED=1
WORKDIR /code
EXPOSE 8000
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY --from=webpack /webpack/static ./static
COPY ./manage.py ./
COPY ./project ./project
COPY ./bookmarker ./bookmarker
CMD python3 manage.py runserver
