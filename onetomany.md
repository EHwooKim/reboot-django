# 01. 1:N

```python
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.TextField()

class Article(models.Model):
    title = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
User 2명, Article 2개, Comment 4개

u1 = User.objects.create(username='Kim')
u2 = User.objects.create(username='Lee')

a1 = Article.objects.create(title='1글', user=u1)
a2 = Article.objects.create(title='2글', user=u2)
a3 = Article.objects.create(title='3글', user=u2)
a4 = Article.objects.create(title='4글', user=u2)

c1 = Comment.objects.create(content='1글1댓', article=a1, user=u2)
c2 = Comment.objects.create(content='1글2댓', article=a1, user=u2)
c3 = Comment.objects.create(content='2글1댓', article=a2, user=u1)
c4 = Comment.objects.create(content='4글1댓', article=a4, user=u1)
c5 = Comment.objects.create(content='3글1댓', article=a3, user=u2)
c6 = Comment.objects.create(content='3글2댓', article=a3, user=u1)
```

1. 모든 댓글 출력

   ```python
   Comment.objects.all()
   ```

2. 1번 사람(`u1`)이 작성한 모든 게시글

   ```python
   Article.objects.filter(user_id=1)
   
   u1.article_set.all()  #!!! 나는 위에거로 했는데 이게 더 좋은 거다!!!
   ```

3. 2번 댓글(`c2`)을 작성한 사람

   ```python
   c2.user
   ```

4. 3번글(`a3`)을 작성한 사람의 이름

   ```python
   a3.user.username
   ```

5. 2번글(`a2`)을 작성한 사람이 작성한 댓글들

   ```python
   a2.user.comment_set.all()
   ```

6. 1번 글(`a1`)에 작성된 댓글 중에 첫번째를 작성한 사람의 이름

   ```python
   a1.comment_set.get(id=1).user.username
   a1.comment_set.all()[0].user.username # !!! 나는 위에거로 했는데 이거로 하자 !!!
   ```

7. 1번 사람(`u1`)이 작성한 첫번째 게시글의 1, 2 번째 댓글

   ```python
   u1.article_set.all()[0].comment_set.all()[0:2]
   ```

8. 1번 사람(`u1`)이 작성한 게시글을 제목 내림차순으로 정렬

   ```python
   u1.article_set.order_by('-title')
   ```



# 02. M:N Many to many

## 1. 중개 모델 ( Reservation 모델같이 중간에서 중개하는 모델)

```python
class Doctor(models.Model):
    name = models.TextField()


class Patient(models.Model):
    name = models.TextField()


# 위의 둘을 묶기 위한 예약 테이블이 필요하겠지
class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
```

1. 예약 만들기

   ```python
   d1 = Doctor.objects.create(name='kim')
   p1 = Patient.objects.create(name='taewoo')
   Reservation.objects.create(doctor=d1, patient=p1)
   ```

2. 1번 환자의 예약 목록

   ```python
   p1.reservation_set.all()
   ```

3. 1번 의사의 예약 목록

   ```python
   d1.reservation_set.all()
   ```

4. 1번 의사의 환자목록

   * 지금 상태에서 바로 의사가 해당하는 환자들로 접근을 할수는 없다 => **반복문** 써서 출력하는 방법뿐..

   ```python
   for r in d1.reservation_set.all():
   	print(r.patient)
   ```



## 2. 중개 모델 (ManytoManyField)

> 의사 -> 환자들 / 환자 -> 의사들로 접근을 하기 위해서는 `ManyToManyField`를 사용한다.
>
> `Reservation` 모델을 활용하려면 `through` 옵션을 사용한다.
>
> `through` 옵션이 없으면, 기본적으로 `앱이름_patient_doctor`라는 이름의 테이블을 생성한다.

```python
# 여기까지 해놓고 보니 위처럼 반복문하는게 불편해

class Doctor(models.Model):
    name = models.TextField()


class Patient(models.Model):
    name = models.TextField()
    doctors = models.ManyToManyField(Doctor, through='Reservation') # <= 추가

class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
```

* 위와 같이 manytomany 옵션 추가 후 `makemigrations`, `migrate` 할 필요 없다!
* 즉, 데이터베이스는 전혀 변경되는 것이 없다.

> 이렇게 바꿨어, 아까랑 다른게 뭐야? Patient에 doctor가 생겼고
>
> d1.doctor보니 뭐가 생겼어. `p1.doctor.all()` 하면 환자1의 의사들을 볼 수 있다.
>
> 반대로 doctor가 patient 부르는것은 `d1.patient_set.all()`로 가능하다. 게시글과 댓글에서 역참조하는거랑 비슷한거야

1. 1번 의사의 예약 목록

   ```python
   d1.reservation_set.all()
   ```

2. 1번 의사의 환자 목록

   * `Doctor`는 `Patient`의 역참조이므로, naming convention에 따라 아래와 같이 접근

   ```python
   d1.patient_set.all()
   ```

3. 1번 환자의 의사 목록

   * `Patient`는 `Doctor`는 직접 참조(`doctors`) 하므로, 아래와 같이 접근

   ```python
   p1.doctor.all()
   ```
   

* 이렇게 하고나니 patient_set도 그냥 patients로 접근하고싶어 그래서 나온게  아래 것



### 2.1 `related_name` 옵션

```python
from django.db import models

class Doctor(models.Model):
    name = models.TextField()

class Patient(models.Model):
    name = models.TextField()
    doctors = models.ManyToManyField(Doctor,
                        through='Reservation',
                        related_name='patients')
    
class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
```

* 역참조시 `realted_name` 옵션으로 직접 설정할 수 있다.
  * 설정하지 않으면 기본적으로 `Model명_set`으로 된다.
* 반드시 설정할 필요는 없지만, 필수적인 상황이 발생할 수 있다.
  * 예) `User` - `Article`
* 따라서, `ManyToManyField`를 쓸 때에는 항상 `related_name`을 설정하고, 모델의 복수형으로 표기하자.

1. 1번 의사의 환자 목록

   ```python
   d1.patients.all()
   ```



## 3. 중개모델 없이 작성

```python
from django.db import models

class Doctor(models.Model):
    name = models.TextField()


class Patient(models.Model):
    name = models.TextField()
    doctors = models.ManyToManyField(Doctor, related_name='patients')
    
# 중개모델인 Reservation이 필요없다.
```

* `앱이름_patient_doctors`로 테이블이 자동으로 생성된다.
* 둘 사이의 **별도의 컬럼이 필요없는 경우**는 위와 같이 작성한다
* 만약, 예약시 추가정보(예-시간, 담당자...)를 담기 위해서라면 반드시 중개 모델이 필요하다!

1. 예약 생성

   ``` python
   d2 = doctor.objects.create(name='kim')
   p2 = Patient.objects.create(name='kim')
   
   d2.patients.add(p2)
   ```

2. 예약 삭제

   ```python
   d2.patients.remove(p5)
   ```






* 서로 찾을 때

  * 1:1에서는  `.profile`, `.user`(단수형)으로 찾고
  * 1:N에서는 `.article_set.all()`, `.user`으로 찾고
  * M:N에서는 `.patients.all()`, `doctors.all()` (복수형)으로 찾는다. <= 이건 내가 따로 설정해줄게있지

  

