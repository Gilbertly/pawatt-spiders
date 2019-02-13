build:
  docker build -t pawatt:latest .

start:
  docker run -ti -v "$$PWD":/pawatt pawatt /bin/bash
