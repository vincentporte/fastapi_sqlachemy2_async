# Welcome to fastapi_sqlachemy2_async 👋
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000)
![GitHub last commit](https://img.shields.io/github/last-commit/vincentporte/fastapi_sqlachemy2_async)
[![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg)](https://github.com/vincentporte/fastapi_sqlachemy2_async#readme)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/vincentporte/fastapi_sqlachemy2_async/graphs/commit-activity)
[![License: MIT](https://img.shields.io/github/license/vincentporte/fastapi_sqlachemy2_async)](https://github.com/vincentporte/fastapi_sqlachemy2_async/blob/master/LICENSE)
![GitHub language count](https://img.shields.io/github/languages/count/vincentporte/fastapi_sqlachemy2_async)
![GitHub top language](https://img.shields.io/github/languages/top/vincentporte/fastapi_sqlachemy2_async)
![GitHub branch checks state](https://img.shields.io/github/checks-status/vincentporte/fastapi_sqlachemy2_async/main)

> fastapi_sqlachemy2_async, Dockerized Postgres and Poetry

### 🏠 [Homepage](https://github.com/vincentporte/fastapi_sqlachemy2_async#readme)

## Install

### setup env

```sh
poetry install;
cp .env.template .env;
```

### setup DB

```sh
docker-compose up -d;
poetry shell;
alembic upgrade head
```

## Usage

### Spawn in virtualenv

```sh
poetry shell;
```

### Run dev server

```sh
make dev
```

### Run tests

```sh
pytest tests/
```

### Run quality

```sh
make quality
```

## Database Migrations

* init alembic (shuold be done only once)

```sh
alembic init -t async alembic
```

* create migration

```sh
alembic revision -m "create table"
```

* apply migration

```sh
alembic upgrade head
```

## Author

👤 **Vincent Porte**

* Website: [vincentporte.gitlab.io](https://vincentporte.gitlab.io)
* Github: [@vincentporte](https://github.com/vincentporte)
* LinkedIn: [@vincentporte](https://linkedin.com/in/vincentporte)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/vincentporte/fastapi_sqlachemy2_async/issues).

## Show your support

Give a ⭐️ if this project helped you!


## 📝 License

Copyright © 2022 [Vincent Porte](https://github.com/vincentporte).

This project is [MIT](https://github.com/vincentporte/fastapi_sqlachemy2_async/blob/master/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_


### notes
* https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
