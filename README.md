# Dockerizing Flask with Postgres, Gunicorn, and Nginx

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx).

## Want to use this project?

### Development

Uses the default Flask development server.

1. Rename *.env.dev-sample* to *.env.dev*.
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:5000](http://localhost:5000). The "web" folder is mounted into the container and your code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.

## 參考資料來源
[Dockerizing Flask with Postgres, Gunicorn, and Nginx](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)
* 這篇文章的原始碼：[testdrivenio/flask-on-docker](https://github.com/testdrivenio/flask-on-docker)
* 寫得很棒，任何新的名詞都會額外解釋

## 檔案功用
docker-compose.yml
* 開發時使用，用flask 內建 server起開發網頁
docker-compose.prod.yml
* 生產環境用，使用如WSGI服務當作server
Dockerfile.prod
* 用到了[multi-stage build](https://docs.docker.com/develop/develop-images/multistage-build/)的功能
* flake8 的載入先行註解，因為會報錯

## 指令記錄
### docker compose
建置docker內容，todo功能
* docker volume inspect nginx-gunicorn-flask_postgres_data

#### 開發環境
##### 重啟指令，建立新的containers
docker-compose up -d --build
* build為建立container，docker-compose build
* up -d為背景執行container，docker-compose up -d
##### 關閉指令，移除之前建立的containers
docker-compose down -v
##### 在container中下建立admin的指令
docker-compose exec web python manage.py admin

#### 正式環境
##### 重啟指令，建立新的containers
docker-compose -f docker-compose.prod.yml up -d --build

##### 關閉指令，移除之前建立的containers
docker-compose -f docker-compose.prod.yml down -v

##### 在container中下建立admin的指令
docker-compose exec web python manage.py admin

##### 查看log
docker-compose -f docker-compose.prod.yml logs -f 
