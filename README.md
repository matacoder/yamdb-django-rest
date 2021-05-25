#Yandex Movie Database REST API (YaMDB)
<img src="https://raw.githubusercontent.com/matacoder/matacoder/main/yamdb2.png">

[![DJANGO REST workflow](https://github.com/matacoder/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)](https://github.com/matacoder/yamdb_final/actions/workflows/yamdb_workflow.yaml)

## Project is live
You can access it at [https://rest.matakov.com](https://rest.matakov.com)

## Description

This is a database of different types of objects with genres, reviews and comments to review.

Documentation is available here: [https://rest.matakov.com/#section/Opisanie](https://rest.matakov.com/#section/Opisanie)

- Api ROOT: [https://rest.matakov.com/api/v1/](https://rest.matakov.com/api/v1/)
- Api Genres [https://rest.matakov.com/api/v1/genres/](https://rest.matakov.com/api/v1/genres/). Can be accessed by anonymous user.

## Authentication

- Used [JWT authentication](https://rest.matakov.com/#section/Algoritm-registracii-polzovatelej)

## User Roles:

- Anonymous
- Authenticated
- Moderator
- Administrator
- Django Administrator

## Models

- Reviews
- Comments
- Users (Abstract User)
- Categories
- Genres
- Titles
