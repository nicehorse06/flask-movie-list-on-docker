# Flask Movie List 部署版本

* 功能為列出我的電影推薦列表，可以連到IMDb查看更多資訊，管理者帳號可以登入做修改
* 有單元測試，測試DB撰寫、頁面新增查改、頁面例外錯誤、flask字定義命令是否成功
* 原始無docker部署的版本：[nicehorse06/flask-movie-blog](https://github.com/nicehorse06/flask-movie-blog)

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

## 部署與開發筆記
如果在雲端服務上，如GCP開80以外的port口，需要新設定一個防火牆規則
* 如0.0.0.0/0的TCP:1337允許
現階段因為設定port為1337，需要在nginx.conf裡面host加上port號
* 如 `proxy_set_header Host $host:1337`
* 這樣flask在轉址時，其host才會為host:1337
現階段部署方式為把專案用git載到VM中，再啟動docker compose指令做部署
* 可再尋找有無更優雅的做法
目前要思考開發時，是否要在docker環境下，還是說循以前的pytohn流做法
要思考什麼時機點才要把docker image上傳到docker hub
