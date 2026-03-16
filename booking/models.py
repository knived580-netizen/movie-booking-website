import uuid
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField()
    release_date = models.DateField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=150.00)
    gst_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=18.00)

    def __str__(self):
        return self.title

class Theatre(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    show_time = models.TimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.theatre.name} at {self.show_time}"

class Booking(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    seat_number = models.CharField(max_length=255)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.ticket_id} - Seat {self.seat_number}"