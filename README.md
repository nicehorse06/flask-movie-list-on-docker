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


# Flask gunicorn nginx docker demo

## 參考資料來源
[Dockerizing Flask with Postgres, Gunicorn, and Nginx](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)
* 這篇文章的原始碼：[testdrivenio/flask-on-docker](https://github.com/testdrivenio/flask-on-docker)
* 寫得很棒，任何新的名詞都會額外解釋

## todo
* 開發環境docker啟動後，無法讀到靜態檔案的網址，如http://localhost:5000/static/hello.txt
* 正式環境docker啟動後，無法讀到靜態檔案的網址，如http://localhost:1337/static/hello.txt
* 開發環境docker啟動後，可以上傳media資料，但是無法藉由網址讀取該資料，如http://localhost:5000/uploads/IMAGE_FILE_NAME
* 正式環境docker啟動後，無法上傳也無法讀取資料

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
建立docker image
* docker-compose build
執行container
* docker-compose up -d
建立docker image 並 執行
* docker-compose up -d --build
在運行的container中執行python manage.py create_db命令
* docker-compose exec web python manage.py create_db
在container中執行python manage.py seed_db去建造一個使用者
* docker-compose exec web python manage.py seed_db
建置docker內容，todo功能
* docker volume inspect nginx-gunicorn-flask_postgres_data

開發環境的重啟流程
* docker-compose down -v
* docker-compose up -d --build
* docker-compose exec web python manage.py create_db
* docker-compose exec web python manage.py seed_db
開發環境關閉流程，移除之前建立的containers
* docker-compose down -v

建立生產環境的container
* docker-compose -f docker-compose.prod.yml up -d --build
	* 以下命令查看log
	* docker-compose -f docker-compose.prod.yml logs -f 

正式環境的重啟流程
* docker-compose -f docker-compose.prod.yml down -v
* docker-compose -f docker-compose.prod.yml up -d --build
* docker-compose -f docker-compose.prod.yml exec web python manage.py create_db

正式環境關閉流程
* docker-compose -f docker-compose.prod.yml down -v
