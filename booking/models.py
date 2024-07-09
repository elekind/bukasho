from django.db import models
from django.db.models import Q, F
import uuid

class Movie(models.Model):
    title = models.CharField(max_length=64, unique=True)
    #duration = models.IntegerField()

    def __str__(self):
        return f"{self.title}"

class ID(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique = True)

    def __str__(self):
        return f"ID- {self.uid}"

class Hall(models.Model): #Add many-many seat to hall instead
    number = models.IntegerField(unique=True) #change it to primary key?

    def __str__(self):
        return f"Hall {self.number}"
    
    class Meta:
        constraints = [
            models.CheckConstraint (check = Q(number__gt=0), name = 'hall greater than 0')
            ]

class Seat(models.Model):
    #check manytomany
    hallno = models.ForeignKey(Hall, to_field='number', on_delete=models.CASCADE)
    number = models.IntegerField()
    row = models.CharField(max_length=1)  #use choices

    def __str__(self):
        return f"Seat {self.row}{self.number}, {self.hallno}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hallno', 'number', 'row'], name='seat in a hall'),
            models.CheckConstraint (check = Q(number__gt=0), name = 'seatnumber greater than 0')
        ]

class Show(models.Model): #show means duration for which a hall is blocked. Does movie matter?
    hall = models.ForeignKey(Hall, to_field='number', on_delete=models.CASCADE) #check many-to-many here
    movie = models.ForeignKey(Movie, to_field='title', on_delete=models.CASCADE, blank=True, null = True)
    start = models.DateTimeField()
    stop = models.DateTimeField()

    def __str__(self): #change str to be clearer
        return f"{self.movie}, {self.hall} on {self.start.strftime('%a %d/%b/%y, %I:%M%p')}"
    
    class Meta():
        constraints = [
            models.CheckConstraint (check = Q(stop__gt=F('start')), name = 'stop greater than start'),
            #models.CheckConstraint (check= models.Show.objects.all(), name='show clash in the same hall'),
            #models.UniqueConstraint(fields=['hall'], condition=(~Q(Show_start__range=(F('start'), F('stop') ), name='show clash in the same hall')
        ]

    #start be greater than end edn before start
    #override save and use range

class Booking(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE) #many-many here? How will UniqueConstraint work?
    booking_id = models.ForeignKey(ID, to_field='uid', on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    class Meta():
        constraints = [
            models.UniqueConstraint(fields=['show', 'seat'], name='seat clash in the same show')
        ]

    def __str__(self):
        return f"{self.seat} in {self.show}. {self.booking_id}"    

#redo many-many relations