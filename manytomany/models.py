from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.TextField()


class Patient(models.Model):
    name = models.TextField()
    # 이거 하고 migrate는 안했어 테이블이 변한건 아니라는거지. 
    doctors = models.ManyToManyField(Doctor,
                        # through='Reservation', # 중개모델(Reservation) 없이 하기위해 지움
                        related_name='patients') # 닥터가 patient를 찾을 때 patients라는 이름으로 참조하겠다. 충돌방지를 위한 것이다!
                                                 # 하나의 class 를 여러번 참조할 때 ~_set 사용시 충돌이 생길 수가 있는 것을 방지.


# 위의 둘을 묶기 위한 예약 테이블이 필요하겠지
# class Reservation(models.Model):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

#     def __str__(self): # 출력했을 때 보기 좋게 하기 위해서
#         return f'{self.pk} 예약: {self.doctor.name}의 환자 {self.patient.name}'

