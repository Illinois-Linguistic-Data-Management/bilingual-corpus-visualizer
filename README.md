# Bilingual Corpus Visualizer

This project project provides a Web based interface for exploring and visualizing bilingual corpora that have been transcribed in the CHAT format. Check out the demo at http://146.190.141.184:3000/

## How it works

The backend server has a copy of the corpus in the folder `backend/transcriptions` and reads all `.cha` files in folders named `backend/transcriptions/Tagged Transcriptions (group xxx)` where xxx is the group code.
The backend serves several web APIs for Part-of-Speech tagging and generation of data visualization images. It is written in Python with FastAPI and Matplotlib.

The frontend is a simple ReactJS application with web interfaces for taking either words as input for part of speech tagging to send to the `/words` endpoint of the backend or filter parameters for the `/viz_xxx` endpoints of the backend for visualization generation.

## Deployment

First, you must specify which public IP address the backend will be hosted on. Please change the variables `REACT_APP_BACKEND_HOST` in `frontend/.env` and `HOST_IP` in `backend/Dockerfile`. If you are running everything locally, you can leave it as is.

To deploy everything at once, simply run `docker compose up --build`. This of course requires a running installation of [Docker](https://www.docker.com/).

To deploy the frontend and backend separately, see their respective READMEs.