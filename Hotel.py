from enum import Enum
from abc import ABC , abstractmethod
import json
from datetime import datetime , date
import copy
class  FileManager(ABC):
  def __init__(self,file_name) -> None:
    super().__init__()
    self.file_name=file_name
  @abstractmethod
  def load(file_name)-> tuple: 
    pass
  @abstractmethod
  def save(file_name,content : dict) :
    pass

class FileManagerRooms(FileManager):
  def load(self):
      rooms = {}
      max_id = 0
      try:
          with open(self.file_name, 'r') as f:
              for line in f:
                  if line.strip():
                      data = json.loads(line)
                      room = Room.from_dict(data)
                      rooms[room.room_number] = room
                      if room.room_number > max_id:
                          max_id = room.room_number
      except FileNotFoundError:
          pass
      return rooms, max_id

  def save(self, rooms: dict):
      with open(self.file_name, 'w') as f:
          for room in rooms.values():
              f.write(json.dumps(room.to_dict()) + '\n')


class FileManagerGuests(FileManager):
  def load(self):
      guests = {}
      max_id = 0
      try:
          with open(self.file_name, 'r') as f:
              for line in f:
                  if line.strip():
                      data = json.loads(line)
                      guest = Guest.from_dict(data)
                      guests[guest.guest_id] = guest
                      if guest.guest_id > max_id:
                          max_id = guest.guest_id
      except FileNotFoundError:
          pass
      return guests, max_id

  def save(self, guests: dict):
      with open(self.file_name, 'w') as f:
          for guest in guests.values():
              f.write(json.dumps(guest.to_dict()) + '\n')


class FileManagerReservations(FileManager):
  def load(self, rooms_dict: dict):
      reservations = {}
      max_id = 0
      try:
          with open(self.file_name, 'r') as f:
              for line in f:
                  if line.strip():
                      data = json.loads(line)
                      res = Reservation.from_dict(data, rooms_dict)
                      reservations[res.reservation_id] = res
                      if res.reservation_id > max_id:
                          max_id = res.reservation_id
      except FileNotFoundError:
          pass
      return reservations, max_id

  def save(self, reservations: dict):
      with open(self.file_name, 'w') as f:
          for res in reservations.values():
              f.write(json.dumps(res.to_dict()) + '\n')
class Room_type (Enum):
  SINGLE=1
  DOUBLE=2
  SUITE=3
  PENTHOUSE= 4

class StatusRoom(Enum):
    AVAILABLE = 1
    OCCUPIED = 2
    MAINTENANCE = 3
    DIRTY_CLEANING = 4

class StatusReservation(Enum):
    PENDING = 1
    CONFIRMED = 2
    CHECKED_IN = 3
    CHECKED_OUT = 4
    CANCELLED = 5

class Membership_type(Enum):
    REGULAR = 1
    GOLD = 2
    PLATINUM = 3

class payment_method(Enum):
  CASH = 1
  CREDIT_CARD = 2
  PAYPAL = 3

class payment_status(Enum):
  PENDING = 1
  PAID = 2
  REFUNDED = 3

class Service :
  def __init__(self,service_id, service_name, price) -> None:
    self.__service_id=service_id
    self.__service_name=service_name
    self.__price=price
    self.__available=True
  
  @property
  def price(self):
    return self.__price
  @property
  def is_available(self):
    return self.__available
  @property
  def service_name(self):
    return self.__service_name
  @property
  def service_id(self):
    return self.__service_id

  @price.setter
  def price(self,price):
    validation.float_number_is_valid(price)
    self.price=price
  @service_id.setter
  def service_id(self, value):
    validation.int_number_is_valid(value)
    self.__service_id = value
  @service_name.setter
  def service_name(self, value):
    validation.name_is_valid(value)
    self.__service_name = value

  def update_price(self,new_price):
    validation.float_number_is_valid(new_price)
    self.__price=new_price
  def toggle_availability(self):
    self.available= not self.available

  def to_dict(self):
    return {
            "service_id": self.service_id,
            "service_name": self.service_name,
            "price": self.price,
            "is_available": self.is_available
        }
  @classmethod
  def from_dict(cls,d):
    return cls(**d)

class ServiceOrder:
    def __init__(self, order_id: int, reservation_id: int, service: Service, quantity: int, ordered_at = None):
        self.order_id = order_id
        self.reservation_id = reservation_id
        self.service = service
        self.quantity = quantity
        self.ordered_at = ordered_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        validation.int_number_is_valid(value)
        self.__order_id = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        validation.int_number_is_valid(value)
        self.__quantity = value

    def calculate_total(self) :
        return self.quantity * self.service.price

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "reservation_id": self.reservation_id,
            "service": self.service.to_dict(),
            "quantity": self.quantity,
            "ordered_at": self.ordered_at
        }

    @classmethod
    def from_dict(cls, data):
        srv = Service.from_dict(data['service'])
        return cls(data['order_id'], data['reservation_id'], srv, data['quantity'], data['ordered_at'])

class Guest :
  def __init__(self,guest_id, first_name, last_name, email, phone,national_id_or_passport,membership_type : Membership_type,loyalty_points,Service_orders=None) :
    self.guest_id = guest_id
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.phone = phone
    self.national_id_or_passport = national_id_or_passport
    self.membership_type = membership_type
    self.loyalty_points = loyalty_points
    self.__service_orders = Service_orders or []

  @property
  def guest_id(self):
      return self.__guest_id

  @guest_id.setter
  def guest_id(self, id_val):
    validation.int_number_is_valid(id_val)
    self.__guest_id = id_val

  @property
  def first_name(self):
    return self.__first_name

  @first_name.setter
  def first_name(self, name):
    validation.name_is_valid(name)
    self.__first_name = name

  @property
  def last_name(self):
    return self.__last_name

  @last_name.setter
  def last_name(self, name):
    validation.name_is_valid(name)
    self.__last_name = name

  @property
  def email(self):
    return self.__email

  @email.setter
  def email(self, email_val):
    validation.email_is_valid(email_val)
    self.__email = email_val

  @property
  def phone(self):
    return self.__phone

  @phone.setter
  def phone(self, phone_val):
      validation.phone_number_is_valid(phone_val)
      self.__phone = phone_val

  @property
  def national_id_or_passport(self):
      return self.__national_id_or_passport

  @national_id_or_passport.setter
  def national_id_or_passport(self, value):
      self.__national_id_or_passport = str(value)

  @property
  def membership_type(self):
      return self.__membership_type

  @membership_type.setter
  def membership_type(self, m_type):
      validation.is_enum_attr(m_type, Membership_type)
      self.__membership_type = m_type

  @property
  def loyalty_points(self):
      return self.__loyalty_points

  @loyalty_points.setter
  def loyalty_points(self, points):
      validation.float_number_is_valid(points)
      self.__loyalty_points = float(points)

  @property
  def service_orders(self):
      return copy.copy(self.__service_orders)

  def update_profile(self, email=None, phone=None):
      if email:
          self.email = email
      if phone:
          self.phone = phone

  def add_loyalty_points(self, points: float):
      validation.float_number_is_valid(points)
      self.loyalty_points += points

  def redeem_loyalty_points(self, points: float):
      validation.float_number_is_valid(points)
      if points > self.loyalty_points:
          raise ValueError("Insufficient loyalty points balance.")
      self.loyalty_points -= points

  def add_service_order(self, service_order: ServiceOrder):  
      self.__service_orders.append(service_order)
  def get_reservation_history(self, reservations_dict: dict) -> list:
        return [res for res in reservations_dict.values() if res.guest.guest_id == self.guest_id]

  def to_dict(self):
      return {
          'guest_id': self.guest_id,
          'first_name': self.first_name,
          'last_name': self.last_name,
          'email': self.email,
          'phone': self.phone,
          'national_id_or_passport': self.national_id_or_passport,
          'membership_type': self.membership_type.value,
          'loyalty_points': self.loyalty_points,
          'service_orders': [order.to_dict() for order in self.__service_orders]
      }

  @classmethod
  def from_dict(cls, data):
      orders = [ServiceOrder.from_dict(o) for o in data.get('Service_orders', [])]
      return cls(
          guest_id=data['guest_id'],
          first_name=data['first_name'],
          last_name=data['last_name'],
          email=data['email'],
          phone=data['phone'],
          national_id_or_passport=data['national_id_or_passport'],
          membership_type=Membership_type(data['membership_type']),
          loyalty_points=data['loyalty_points'],
          Service_orders=orders
      )


class Room:
  def __init__(self, room_number: int, room_type: Room_type, price_per_night: float,
                status: StatusRoom = StatusRoom.AVAILABLE, max_occupancy: int = 2, amenities=None):
    self.room_number = room_number
    self.room_type = room_type
    self.price_per_night = price_per_night
    self.status = status
    self.max_occupancy = max_occupancy
    self.__amenities = amenities or []

  @property
  def room_number(self):
      return self.__room_number

  @room_number.setter
  def room_number(self, value):
    validation.int_number_is_valid(value)
    self.__room_number = value

  @property
  def room_type(self):
    return self.__room_type

  @room_type.setter
  def room_type(self, value):
    validation.is_enum_attr(value, Room_type) 
    self.__room_type = value

  @property
  def price_per_night(self):
    return self.__price_per_night

  @price_per_night.setter
  def price_per_night(self, value):
    validation.float_number_is_valid(value)
    self.__price_per_night = float(value)

  @property
  def status(self):
    return self.__status

  @status.setter
  def status(self, value):
    validation.is_enum_attr(value, StatusRoom)
    self.__status = value

  @property
  def max_occupancy(self):
    return self.__max_occupancy

  @max_occupancy.setter
  def max_occupancy(self, value):
    validation.int_number_is_valid(value)
    self.__max_occupancy = value

  @property
  def amenities(self):
    return copy.copy(self.__amenities)

  def calculate_cost(self, nights: int) -> float:
    return self.price_per_night * nights

  def add_amenity(self, amenity_name: str):
    validation.name_is_valid(amenity_name)
    if amenity_name not in self.__amenities:
        self.__amenities.append(amenity_name)

  def remove_amenity(self, amenity_name: str):
    if amenity_name in self.__amenities:
      self.__amenities.remove(amenity_name)

  def update_status(self, new_status: StatusRoom):
    self.status = new_status

  def is_available(self, check_in_date: date, check_out_date: date, reservations_list: list) -> bool:
    if self.status in [StatusRoom.MAINTENANCE, StatusRoom.DIRTY_CLEANING]:
        return False
    
    for res in reservations_list:
        if res.room.room_number == self.room_number and res.status not in [StatusReservation.CANCELLED, StatusReservation.CHECKED_OUT]:
            if not (check_out_date <= res.check_in_date or check_in_date >= res.check_out_date):
                return False
    return True

  def to_dict(self):
      return {
          'room_number': self.room_number,
          'room_type': self.room_type.value,
          'price_per_night': self.price_per_night,
          'status': self.status.value,
          'max_occupancy': self.max_occupancy,
          'amenities': self.amenities
      }

  @classmethod
  def from_dict(cls, data):
    data_copy = data.copy()
    data_copy['room_type'] = Room_type(data_copy['room_type'])
    data_copy['status'] = StatusRoom(data_copy['status'])
    return cls(**data_copy)

class Reservation:
  def __init__(self, reservation_id: int, guest: Guest, room: Room, check_in_date: date,
                check_out_date: date, status: StatusReservation = StatusReservation.PENDING,
                number_of_guests: int = 1, created_at: date = None):
    self.reservation_id = reservation_id
    self.guest = guest
    self.room = room
    self.check_in_date = check_in_date
    self.check_out_date = check_out_date
    self.__status = status
    self.number_of_guests = number_of_guests
    self.created_at = created_at or date.today()

  @property
  def reservation_id(self):
    return self.__reservation_id

  @reservation_id.setter
  def reservation_id(self, value):
    validation.int_number_is_valid(value)
    self.__reservation_id = value

  @property
  def guest(self):
    return self.__guest

  @guest.setter
  def guest(self, value):
    self.__guest = value

  @property
  def room(self):
    return self.__room

  @room.setter
  def room(self, value):
    self.__room = value

  @property
  def check_in_date(self) -> date:
    return self.__check_in_date

  @check_in_date.setter
  def check_in_date(self, value):
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d").date()
    self.__check_in_date = value

  @property
  def check_out_date(self) -> date:
    return self.__check_out_date

  @check_out_date.setter
  def check_out_date(self, value):
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d").date()
    if value <= self.check_in_date:
        raise ValueError("Check-out date must be after check-in date.")
    self.__check_out_date = value

  @property
  def status(self) -> StatusReservation:
     return self.__status

  @status.setter
  def status(self, value):
    validation.is_enum_attr(value, StatusReservation)
    self.__status = value

  @property
  def number_of_guests(self):
    return self.__number_of_guests

  @number_of_guests.setter
  def number_of_guests(self, value):
    validation.int_number_is_valid(value)
    if value > self.room.max_occupancy:
        raise ValueError(f"Number of guests exceeds room capacity ({self.room.max_occupancy}).")
    self.__number_of_guests = value

  @property
  def created_at(self) -> date:
    return self.__created_at

  @created_at.setter
  def created_at(self, value):
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d").date()
    self.__created_at = value

  def confirm_reservation(self):
    self.status = StatusReservation.CONFIRMED

  def check_in(self) -> bool:
    if date.today() >= self.check_in_date:
        self.status = StatusReservation.CHECKED_IN
        self.room.status = StatusRoom.OCCUPIED
        return True
    return False

  def check_out(self):
    self.status = StatusReservation.CHECKED_OUT
    self.room.status = StatusRoom.DIRTY_CLEANING

  def cancel_reservation(self):
    self.status = StatusReservation.CANCELLED
    self.room.status = StatusRoom.AVAILABLE

  def to_dict(self):
    return {
        'reservation_id': self.reservation_id,
        'guest': self.guest.to_dict(),
        'room_number': self.room.room_number,
        'check_in_date': self.check_in_date.strftime("%Y-%m-%d"),
        'check_out_date': self.check_out_date.strftime("%Y-%m-%d"),
        'status': self.status.value,
        'number_of_guests': self.number_of_guests,
        'created_at': self.created_at.strftime("%Y-%m-%d")
    }

  @classmethod
  def from_dict(cls, data, rooms_dict: dict):
    guest = Guest.from_dict(data['guest'])
    room = rooms_dict[data['room_number']]
    return cls(
        reservation_id=data['reservation_id'],
        guest=guest,
        room=room,
        check_in_date=data['check_in_date'],
        check_out_date=data['check_out_date'],
        status=StatusReservation(data['status']),
        number_of_guests=data['number_of_guests'],
        created_at=data['created_at']
    )



class Invoice:
    def __init__(self, reservation: Reservation):
        self.reservation = reservation

    def calculate_room_subtotal(self) -> float:
        num_nights = (self.reservation.check_out_date - self.reservation.check_in_date).days
        num_nights = max(1, num_nights)
        return num_nights * self.reservation.room.price_per_night

    def calculate_services_subtotal(self) -> float:
        total_services = 0.0
        for order in getattr(self.reservation.guest, 'service_orders', []):
            if order.reservation_id == self.reservation.reservation_id:
                total_services += order.service.price * order.quantity
        return total_services

    def calculate_subtotal(self) -> float:
        return self.calculate_room_subtotal() + self.calculate_services_subtotal()

    def calculate_discount(self) -> float:
        discount_rate = self.reservation.guest.membership_type.value / 100.0
        return self.calculate_subtotal() * discount_rate

    def calculate_tax(self) -> float:
        return (self.calculate_subtotal() - self.calculate_discount()) * 0.14

    def calculate_grand_total(self) -> float:
        return self.calculate_subtotal() - self.calculate_discount() + self.calculate_tax()
class Payment:
  def __init__(self, payment_id: int, invoice: Invoice, payment_method: payment_method, 
                payment_status: payment_status = payment_status.PENDING):
      self.payment_id = payment_id
      self.invoice = invoice              
      self.amount = invoice.calculate_grand_total()
      self.payment_method = payment_method
      self.payment_status = payment_status
      self.transaction_date = datetime.now()

  def process_payment(self) -> bool:
      self.payment_status = payment_status.PAID
      
      earned_points = self.amount / 10
      self.invoice.reservation.guest.add_loyalty_points(earned_points)
      return True

class validation:
  @staticmethod
  def name_is_valid(name : str):
    if name.isalnum() :
      return
    else :
       raise ValueError(name ,"is invalid name")

  @staticmethod
  def email_is_valid(email: str):
    if isinstance(email, str) and '@' in email and '.' in email:
      return
    raise ValueError(f"'{email}' is an invalid email")

  @staticmethod
  def phone_number_is_valid(number: str):
    str_num = str(number).strip()
    if str_num.startswith('+') and str_num[1:].isdigit():
      return
    if str_num.isdigit():
      return
    raise ValueError(f"'{number}' is an invalid phone number")

  @staticmethod
  def int_number_is_valid(number : int):
    if isinstance(number, int) and number >= 0:
      return
    raise ValueError(f"'{number}' is an invalid integer")

  @staticmethod
  def float_number_is_valid(number : float):
    if isinstance(number, (int, float)) and number >= 0:
      return
    raise ValueError(f"'{number}' is an invalid price/float value")

  @staticmethod
  def is_enum_attr(var ,cls):
    if var not in cls:
      raise ValueError("the variable is not Attribute of enum")

  @staticmethod
  def is_obj_from_cls(obj,cls):
    if isinstance(obj,cls):
      raise ValueError("invlaid object")
  @staticmethod
  def is_datetime(date:str):
    s=date.split('-')
    if len(s) == 3 :
      if len(s[0])==4 and len(s[1])==2 and len(s[2])==2 :
        return
    raise ValueError(str(date) + " is invalid datetime")

class Hotel:
  __singleton = None

  def __new__(cls):
      if cls.__singleton is None:
          cls.__singleton = super().__new__(cls)
      return cls.__singleton

  def __init__(self):
      if hasattr(self, '_initialized') and self._initialized:
          return

      self.f_rooms = FileManagerRooms('rooms.json')
      self.f_guests = FileManagerGuests('guests.json')
      self.f_reservations = FileManagerReservations('reservations.json')

      self.rooms, self.__room_counter = self.f_rooms.load()
      self.guests, self.__guest_counter = self.f_guests.load()
      self.reservations, self.__reservation_counter = self.f_reservations.load(self.rooms)

      self._initialized = True

  def save_all(self):
      self.f_rooms.save(self.rooms)
      self.f_guests.save(self.guests)
      self.f_reservations.save(self.reservations)

  def generate_next_guest_id(self) -> int:
      self.__guest_counter += 1
      return self.__guest_counter

  def generate_next_room_number(self) -> int:
      self.__room_counter += 1
      return self.__room_counter

  def generate_next_reservation_id(self) -> int:
      self.__reservation_counter += 1
      return self.__reservation_counter

  def add_room(self, room: Room):
      self.rooms[room.room_number] = room
      self.save_all()

  def register_guest(self, guest: Guest):
      self.guests[guest.guest_id] = guest
      self.save_all()

  def find_available_rooms(self, check_in_date: date, check_out_date: date,
                            room_type: Room_type, guests_count: int) -> list:
      available = []
      res_list = list(self.reservations.values())
      for room in self.rooms.values():
          if room.room_type == room_type and room.max_occupancy >= guests_count:
              if room.is_available(check_in_date, check_out_date, res_list):
                  available.append(room)
      return available

  def create_reservation(self, guest_id: int, room_number: int,
                          check_in_date: date, check_out_date: date, number_of_guests: int) -> Reservation:
      guest = self.guests.get(guest_id)
      room = self.rooms.get(room_number)

      if not guest or not room:
          raise ValueError("Guest or Room not found.")

      res_list = list(self.reservations.values())
      if not room.is_available(check_in_date, check_out_date, res_list):
          raise ValueError("Room is not available for the specified dates.")

      res_id = self.generate_next_reservation_id()
      reservation = Reservation(res_id, guest, room, check_in_date, check_out_date,
                                StatusReservation.PENDING, number_of_guests)
      self.reservations[res_id] = reservation
      self.save_all()
      return reservation

  def update_room(self, room_number: int, price_per_night: float, max_occupancy: int, room_type: Room_type, status: StatusRoom):
    if room_number in self.rooms:
        room = self.rooms[room_number]
        room.price_per_night = price_per_night
        room.max_occupancy = max_occupancy
        room.room_type = room_type
        room.status = status
        self.save_all()

def update_reservation(self, res_id: int, check_in_date, check_out_date, number_of_guests: int, status: StatusReservation):
    if res_id in self.reservations:
        res = self.reservations[res_id]
        res.check_in_date = check_in_date
        res.check_out_date = check_out_date
        res.number_of_guests = number_of_guests
        res.status = status
        self.save_all()