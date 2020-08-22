## Django_ORM_pratice_project


이 프로젝트는 장고 ORM을 공부하기 위해 만든 개인 프로젝트

적당한 더미데이터와 적당한 모델들을 만들어놓고 

쿼리셋 수행 결과를 기록해놓음



#### QuerySet과 SQL 매칭 결과 (Postgresql 기준이지만 기초적인 SQL문법수행이라 다른DB들과 결과는 동일)
* 굳이 이 프로젝트를 clone 안해도 이 파일만 봐도 django QuerySet을 이해하는데 충분히 도움이 될거라 생각됩니다.

https://github.com/KimSoungRyoul/Django_ORM_pratice_project/blob/master/orm_practice_app/queryset_pratice.py


### Quick Start (이 프로젝트 써보기) 

1. `git clone git@github.com:KimSoungRyoul/Django_ORM_pratice_project.git`
2. `pip install -r requirements.txt`
3. `docker-compose up -d`  // 커맨드 수행시 port: 5439로 postgres가 열립니다. local에 postgres설치되어있다면 스킵하도됨 
4. `python manage.py migrate`
5. `python manage.py bulk_create` // DB에 적당히 더미데이터 생성합니다.
6. `python manage.py shell_plus` // 쉘플러스 접속해서 자기가 원하는QuerySet을 실행해봅니다 (jupiter도 좋고 shell_plus도 좋고!)
