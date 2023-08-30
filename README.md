## Django_ORM_pratice_project


이 프로젝트는 장고 ORM을 공부하기 위해 만든 개인 프로젝트

적당한 더미데이터와 적당한 모델들을 만들어놓고 

쿼리셋 수행 결과를 기록해놓음

---
### [PyCon2020 발표자료PDF 다운로드 바로가기](https://github.com/KimSoungRyoul/PyCon2020-DjangoORM/issues/7)
<img alt="aaa" src="https://github.com/KimSoungRyoul/PyCon2020-DjangoORM/assets/24240623/525a1040-48a7-449a-b312-ac56ab5e59d9" width="40%" height="10%">



### [[YouTube] Django ORM (QuerySet)구조와 원리 그리고 최적화전략 - PyCon Korea 2020](https://www.youtube.com/watch?v=EZgLfDrUlrk)
<img alt="aabba" src="https://github.com/KimSoungRyoul/PyConKR2020-DjangoORM/assets/24240623/78ee7ceb-88ca-44c3-be76-e2565f632685" width="50%" height="10%">




---

### 이 Repo 관련 자료는 한빛미디어 [백엔드 개발자를 위한 핸즈온 장고] 책의 초안으로 활용되었고 더 쉽게 정리해서 출간했습니다. [2023-06]
* ### [django-backend-starter](https://github.com/KimSoungRyoul/django-backend-starter) Repo에서 Django ORM 뿐만 아니라 전체적인 내용을 체계적으로 관리해보려합니다.
<img src="https://github.com/KimSoungRyoul/Django_ORM_pratice_project/assets/24240623/c4df85f5-92ac-4d78-bbbd-fea7de72aea4" width="20%" height="10%">


---


#### QuerySet과 SQL 매칭 결과 (Postgresql 기준이지만 기초적인 SQL문법수행이라 다른DB들과 결과는 동일)
* 굳이 이 프로젝트를 clone 안해도 issue창에 내용들을 정리해놔서 충분히 도움이 될거라 생각됩니다.

https://github.com/KimSoungRyoul/Django_ORM_pratice_project/issues
https://github.com/KimSoungRyoul/Django_ORM_pratice_project/blob/master/orm_practice_app/queryset_pratice.py  (쿼리셋 연습장)


### Quick Start (이 프로젝트 써보기) 

1. `git clone git@github.com:KimSoungRyoul/Django_ORM_pratice_project.git`
2. `pip install -r requirements.txt`
3. `docker-compose up -d`  // 커맨드 수행시 port: 5439로 postgres가 열립니다. local에 postgres설치되어있다면 스킵하도됨 
4. `python manage.py migrate`
5. `python manage.py bulk_create` // DB에 적당히 더미데이터 생성합니다.
6. `python manage.py shell_plus` // 쉘플러스 접속해서 자기가 원하는QuerySet을 실행해봅니다 (jupiter도 좋고 shell_plus도 좋고!)



### queryset 관련 도움이 되는 글들

* [Django ORM CookBook 전체적인 QuerySet 사용법을 설명하는 책입니다](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/)  


* [Django에서는 QuerySet이 당신을 만듭니다 (1)](https://medium.com/deliverytechkorea/django-queryset-1-14b0cc715eb7)

* [Django에서는 QuerySet이 당신을 만듭니다 (2)](https://medium.com/deliverytechkorea/django%EC%97%90%EC%84%9C%EB%8A%94-queryset%EC%9D%B4-%EB%8B%B9%EC%8B%A0%EC%9D%84-%EB%A7%8C%EB%93%AD%EB%8B%88%EB%8B%A4-2-5f6f8c6cd7e3)



