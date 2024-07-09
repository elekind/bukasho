from django.shortcuts import render
from booking.models import Show, Seat, ID, Booking
from django.db.models import Q, F
from django.http import HttpResponse

# Create your views here.

def main(request): 
    qs = Show.objects.values('movie').distinct().order_by('movie')
    movies = [[movie['movie'].rstrip(), movie['movie'].lower().rstrip().replace(' ', '-')] for movie in qs]
    #use trim. use replace on qs.
    return render(request, "booking/main.html", {"movies": movies})

def shows(request, movie):
   dict = {}
   for row in Show.objects.values():
      dict[row['movie_id'].lower().rstrip().replace(' ', '-')] = row['movie_id']
   showtimes = Show.objects.filter(movie__title__contains=dict[movie]).order_by('start')
   return render(request, "booking/shows.html", {"showtimes": showtimes})

def seats(request, shownum):
    seats = Seat.objects.filter(hallno__show__id =shownum).order_by('row','number').values('row','number', 'id')
    seats_b = Seat.objects.filter(booking__show__id =shownum).order_by('row','number').values('id')
    seats_booked = [i['id'] for i in seats_b]
    if request.method == "POST":
        sb = [int(i) for i in (request.POST.getlist('seat'))]
        if (sb != []):
            i = ID.objects.create()
            sh = Show.objects.get(pk = shownum)
            for seat_id in sb:
                st = Seat.objects.get(pk = seat_id)
                b = Booking.objects.create(seat=st, booking_id = i, show = sh)
            seats_a = Seat.objects.filter(pk__in = sb).order_by('row','number').values('row','number')
            seats = Seat.objects.filter(hallno__show__id =shownum).order_by('row','number').values('row','number', 'id')
            seats_b = Seat.objects.filter(booking__show__id =shownum).order_by('row','number').values('id')
            seats_booked = [i['id'] for i in seats_b]
            return render(request, "booking/seats.html", {"seats": seats, "seats_booked": seats_booked, "shownum":shownum, "booked":1, "id":i, "show":sh, 'seats_new':seats_a})
           
    return render(request, "booking/seats.html", {"seats": seats, "seats_booked": seats_booked, "shownum":shownum})

def cancel(request):

    if request.method == "POST" and request.POST.get('uid'):
        print('bye')
        new_seats = [int(i) for i in (request.POST.getlist('seat'))]
        uid = str(request.POST.get('uid'))
        user_seats = Seat.objects.filter(booking__booking_id = uid)
        seats_selected = Seat.objects.filter (pk__in = new_seats)
        seats_deselected = user_seats.difference(seats_selected)
        for i in seats_deselected:
            Booking.objects.filter(Q(booking_id = uid) & Q(seat = i)).delete()
        return render(request, "booking/cancel.html", {"pop":seats_deselected, "uid2": uid})
    
    elif request.method == "POST" and request.POST.get('id'):
        print('hi')
        uid = str(request.POST.get('id'))
        user_seats = Seat.objects.filter(booking__booking_id = uid).order_by('row','number').values('row','number','id')
        seats = Seat.objects.filter(hallno__show__booking__booking_id = uid).order_by('row','number').values('row','number','id').distinct()
        print(user_seats)
        return render(request, "booking/cancel.html", {"seats": seats, "user_seats": user_seats, "uid":uid})
    
    return render(request, "booking/cancel.html")