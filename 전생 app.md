# 전생 app

* 무연님은 전생에 선생님이었습니다.

1. Form : 이름을 받아서

2. 직업 랜덤 추출

   ```python
   pip install faker
   from faker import Faker
   fake = Faker('ko_KR')
   fake.job()
   ```

   

3. 결과를 출력

   1. DB에 등록된 이름이 있으면, 해당 하는 결과 출력
   2. 이름이 없으면 새롭게 DB를 추가하고, 결과 출력