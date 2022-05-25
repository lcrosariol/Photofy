from django.test import TestCase, Client
from .models import Photo, Equipment, Booking, User, Profile, Transaction
from datetime import date
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment
from django.urls import reverse, resolve, path, include
from . import views
from django.forms.models import model_to_dict

class BookingTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='test', password='12345test')
        bookingDict = {
            "date": date.today(),
            "location": "Sacramento",
            "customer_name": "John Appleseed",
            "phone_number": "9164794366",
            "comment": "Test comment",
            "user": user

        }
        Booking.objects.create(
            date=bookingDict["date"],
            location=bookingDict["location"],
            customer_name=bookingDict["customer_name"],
            phone_number=bookingDict["phone_number"],
            comment=bookingDict["comment"],
            user=bookingDict["user"]
            )
        user1 = User.objects.get(id=user.id)
        bookings = Booking.objects.all()
        print("This is user:", user1)
        print("These are the bookings", bookings)
        listsBookings = list(bookings)
        
    def test_check_user_values(self):
        user = User.objects.create(username='test2', password='12345test')
        bookings = Booking.objects.all()
        print("Bookings:", bookings)
        listBookings = list(bookings)
        self.assertEqual(listBookings[0].customer_name, 'John Appleseed')
        self.assertEqual(user.username, 'test2')

class EquipmentTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='test1', password='12345test')
        profile = Profile.objects.get(user_id=user.id)
        equipments = Equipment.objects.create(type='P', model="Canon Rebel XTI")
        print("Equipment: ", equipments)
        profile.equipments.add(equipments)
        profile.save()
    
    def test_check_equipment_values(self):
        user = User.objects.get(username='test1')
        profile = Profile.objects.get(user_id=user.id)
        equipments = Equipment.objects.all()
        print("Profile: ", profile)
        print(f"Equipments: {profile.equipments}")
        listEquipments = list(equipments)
        self.assertEqual(listEquipments[0].model, 'Canon Rebel XTI')
        self.assertEqual(listEquipments[0].type, 'P')

class TransactionTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='test3', password='test12345')
        bookingDict = {
            "date": date.today(),
            "location": "Sacramento",
            "customer_name": "John Appleseed",
            "phone_number": "9164794366",
            "comment": "Test comment",
            "user": user
        }
        booking = Booking.objects.create(
            date=bookingDict["date"],
            location=bookingDict["location"],
            customer_name=bookingDict["customer_name"],
            phone_number=bookingDict["phone_number"],
            comment=bookingDict["comment"],
            user=bookingDict["user"]
            )
        print("Booking: ", booking)

        transaction = Transaction.objects.create(payment_method='Z', amount=500, date=date.today(), booking=booking, paid=False)
        print("Transaction: ", transaction)

    def test_checkTransactions(self):
        transactions = Transaction.objects.all()
        listTransactions = list(transactions)
        self.assertEqual(listTransactions[0].amount, 500)
        self.assertEqual(listTransactions[0].payment_method, 'Z')
        self.assertEqual(listTransactions[0].booking.location, 'Sacramento')



class PhotoTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='test4', password='test12345')
        photo = Photo.objects.create(url="https://i.imgur.com/KAL1fJf.png", description='test', user=user)
        print("Photo :", photo.url)

    def test_checkPhoto(self):
        photos = Photo.objects.all()
        listPhotos = list(photos)
        self.assertEqual(len(listPhotos), 1)
        self.assertEqual(listPhotos[0].url, 'https://i.imgur.com/KAL1fJf.png')
        self.assertEqual(listPhotos[0].description, 'test')
        self.assertEqual(listPhotos[0].user.username, 'test4')

class URLSTestCase(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        user = User.objects.create(username='test5', password='test12345')
        bookingDict = {
            "date": date.today(),
            "location": "Sacramento",
            "customer_name": "John Appleseed",
            "phone_number": "9164794366",
            "comment": "Test comment",
            "user": user
        }
        booking = Booking.objects.create(
            date=bookingDict["date"],
            location=bookingDict["location"],
            customer_name=bookingDict["customer_name"],
            phone_number=bookingDict["phone_number"],
            comment=bookingDict["comment"],
            user=bookingDict["user"]
            )
    
    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed = 'home.html'
        self.assertEqual(response.status_code, 200)
    
    def test_photographers(self):
        url = reverse('photographers')
        response = self.client.get(url)
        self.assertTemplateUsed = 'photographers.html'
        self.assertEqual(response.status_code, 200)
    
    def test_booking(self):
        bookings = Booking.objects.all()
        listBookings = list(bookings)
        firstBooking = listBookings[0]
        url = reverse('booking', args=(firstBooking.pk,))
        print("URL Booking: ", url)
        response = self.client.get(url)
        self.assertTemplateUsed = 'bookings/booking_detail.html'
        self.assertContains(response, firstBooking.customer_name)
        self.assertEqual(response.status_code, 200)

    def test_bookings(self):
        url = reverse('bookings')
        response = self.client.get(url)
        self.assertTemplateUsed = 'bookings/index.html'
        self.assertEqual(response.status_code, 200)

    def test_portfolio(self):
        url = reverse('portfolio')
        response = self.client.get(url)
        self.assertTemplateUsed = 'portfolio.html'
        self.assertEqual(response.status_code, 200)
    
    def test_equipment(self):
        url = reverse('equipment')
        response = self.client.get(url)
        self.assertTemplateUsed = 'equipment.html'
        self.assertEqual(response.status_code, 200)
    
    def test_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_transactions(self):
        url = reverse('transactions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_create_transaction(self):
        url = reverse('transaction_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_add_photo(self):
        user = User.objects.get(username='test5')
        url = reverse('add_photo', args=(user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
class TransactionFormTestCase(TestCase):
    def test_transaction_form(self):
        user = User.objects.create(username='test3', password='test12345')
        booking = Booking.objects.create(
            date=date.today(),
            location="San Diego",
            customer_name="Tim Jones",
            phone_number="9168765432",
            comment="Comment Test",
            user=user
            )
        print("Booking: ", booking)

        transaction = Transaction.objects.create(payment_method='Z', amount=500, date=date.today(), booking=booking, paid=False)
        data = model_to_dict(transaction)
        response = self.client.post("/transaction/create", data=data)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertTemplateUsed(views.TransactionCreate.as_view())

class TestRedirectNonUser(TestCase):

    def test_home_redirect_nonuser(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_equipment_redirect_nonuser(self):
        url = reverse('equipment')
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=/equipment/")
    
    def test_portfolio_redirect_nonuser(self):
        url = reverse('portfolio')
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=/portfolio/")

    def test_bookings_redirect_nonuser(self):
        url = reverse('bookings')
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=/bookings/")
    
    def test_transactions_redirect_nonuser(self):
        url = reverse('transactions')
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=/transactions/")
    
    def test_portfolio_redirect_nonuser(self):
        url = reverse('portfolio')
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=/portfolio/")
