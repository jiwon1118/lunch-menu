# lunch-menu
- [x] 팀원들의 점심 메뉴를 수집
- [x] 분석
- [ ] 알람 (입력하지 않은 사람들에게)
- [ ] CSV to DB

## READY
###  Install DB with Docker
```bash
$ sudo docker run --name local-postgres \
-e POSTGRES_USER=sunsin \
-e POSTGRES_PASSWORD=mysecretpassword \
-e POSTGRES_DB=sunsindb \
-p 5432:5432 \
-d postgres:15.10
```

### Create  Table
- postgres

```sql
CREATE TABLE public.lunch_menu (
	id serial NOT NULL,
	menu_name text NOT NULL,
	member_name text NOT NULL,
	dt date NOT NULL,
	CONSTRAINT lunch_menu_pk PRIMARY KEY (id)
);

ALTER TABLE lunch_menu
ADD CONSTRAINT unique_member_dt UNIQUE (member_name, dt)

INSERT INTO member(name)
VALUES
('TOM'),
('cho'),
('hyun'),
('JERRY'),
('SEO'),
('jiwon'),
('jacob'),
('heejin'),
('lucas'),
('nuni')
;

SELECT jsonb_object_agg(name, id) 
FROM (
	select name, id from member order by id
) temp;


```
## DEV
- DB
```bash
$ sudo docker ps -a
$ sudo docker start local-postgres
$ sudo docker stop local-postgres

# Into CONTAINER 
$ sudo docker exec -it local-postgres bash
```

- RUN
```bash
# 디지 정보에 맞춰 수정
cp env.dummy .env

# 서버 시작
streamlit run App.py
```
