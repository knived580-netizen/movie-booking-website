import qrcode
import base64
from io import BytesIO
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Theatre, Show, Booking

def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, "movie_detail.html", {"movie": movie})

def theatre_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    shows = Show.objects.filter(movie=movie).order_by('theatre__name', 'show_time')
    
    theatres_dict = {}
    for show in shows:
        if show.theatre not in theatres_dict:
            theatres_dict[show.theatre] = []
        theatres_dict[show.theatre].append(show)

    return render(request, "theatre_list.html", {
        "movie": movie,
        "theatres_dict": theatres_dict
    })

def ticket_quantity(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        
        # Check available seats
        total_seats = 40  # 5 rows * 8 cols
        all_booked_seat_strings = Booking.objects.filter(show=show).values_list('seat_number', flat=True)
        booked_seats = []
        for seat_string in all_booked_seat_strings:
            if seat_string:
                booked_seats.extend([s.strip() for s in seat_string.split(',')])
        available_seats = total_seats - len(set(booked_seats))
        
        if available_seats < quantity:
            return render(request, "quantity_selection.html", {"show": show, "error": f"Only {available_seats} seats available. Please select fewer tickets."})
        
        return redirect('seat_selection', show_id=show.id, quantity=quantity)

    return render(request, "quantity_selection.html", {"show": show})

def seat_selection(request, show_id, quantity):
    show = get_object_or_404(Show, id=show_id)
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        seat = request.POST.get('seat') # expecting comma-separated list like "A1,A2"
        
        # Calculate price
        subtotal = show.movie.price * quantity
        gst = subtotal * (show.movie.gst_percentage / Decimal('100.0'))
        total_amount = subtotal + gst
        
        booking = Booking.objects.create(
            show=show,
            name=name,
            email=email,
            seat_number=seat,
            amount_paid=total_amount
            # payment_status defaults to False
        )
        
        return redirect('payment_gateway', booking_id=booking.ticket_id)

    import json
    
    # We fetch ALL seat strings (which might be comma separated themselves), 
    # and flatten them into a single list of occupied seats so the JS knows what's taken.
    all_booked_seat_strings = Booking.objects.filter(show=show).values_list('seat_number', flat=True)
    booked_seats = []
    for seat_string in all_booked_seat_strings:
        if seat_string:
            booked_seats.extend([s.strip() for s in seat_string.split(',')])
    
    return render(request, "seat_selection.html", {
        "show": show,
        "quantity": quantity,
        "booked_seats_json": json.dumps(booked_seats)
    })

from django.core.mail import EmailMessage

def generate_ticket_qr(booking):
    import json
    qr_data = json.dumps({
        "Ticket ID": str(booking.ticket_id),
        "Movie": booking.show.movie.title,
        "Seat": booking.seat_number,
        "Name": booking.name
    })
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def payment_gateway(request, booking_id):
    booking = get_object_or_404(Booking, ticket_id=booking_id)

    # Generate UPI QR Code
    upi_id = "9048315528@pthdfc"
    merchant_name = "MovieBooking"
    upi_url = f"upi://pay?pa={upi_id}&pn={merchant_name}&am={booking.amount_paid}&cu=INR"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(upi_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "payment_gateway.html", {
        "booking": booking,
        "qr_code_base64": qr_code_base64
    })

def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, ticket_id=booking_id)
    if request.method == "POST":
        return render(request, "processing_payment.html", {"booking": booking})
    return redirect('payment_gateway', booking_id=booking_id)

def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, ticket_id=booking_id)
    if request.method == "POST":
        # Simulate payment success
        booking.payment_status = True
        booking.save()

        # Send Email
        subject = f"Your Tickets for {booking.show.movie.title}"
        body = f"""
Dear {booking.name},

Your payment of ₹{booking.amount_paid} was successful!
Here are your booking details:

Movie: {booking.show.movie.title}
Theatre: {booking.show.theatre.name}
Time: {booking.show.show_time.strftime('%I:%M %p')}
Seat(s): {booking.seat_number}

Please find your Ticket QR Code attached to this email. Show it at the entrance.

Enjoy the movie!
MovieBooking Team
        """
        
        from django.contrib import messages
        
        email = EmailMessage(
            subject,
            body,
            'noreply@moviebooking.com',
            [booking.email]
        )
        
        qr_bytes = generate_ticket_qr(booking)
        email.attach('ticket_qr.png', qr_bytes, 'image/png')
        
        try:
            email.send(fail_silently=False)
            messages.success(request, "Ticket confirmed and sent to your email!")
        except Exception as e:
            print(f"Email failed to send: {e}")
            messages.warning(request, "Ticket confirmed! However, we couldn't send the email. Please screenshot this page.")

        return redirect('ticket_detail', booking_id=booking.ticket_id)
    return redirect('payment_gateway', booking_id=booking_id)

def ticket_detail(request, booking_id):
    booking = get_object_or_404(Booking, ticket_id=booking_id)
    
    qr_bytes = generate_ticket_qr(booking)
    qr_code_base64 = base64.b64encode(qr_bytes).decode()

    return render(request, "ticket.html", {
        "booking": booking,
        "qr_code_base64": qr_code_base64
    })