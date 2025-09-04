# models.py
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Admin:
    Id: Optional[int]
    Username: str
    Password: str  
    Email: str 

@dataclass
class Airport:
    id: Optional[int]
    name: str
    code: str
    city: str
    country: str

@dataclass
class Auth:
    Id: Optional[int]
    Username: str
    Role: str
    Password: Optional[str]  = None

@dataclass
class Booking:
    id: Optional[int]
    frequentFlyerId: int
    flightId: int
    bookingDate: str  # datetime string


@dataclass
class Flight:
    id: Optional[int]
    planeId: int
    departureAirportId: int
    arrivalAirportId:int
    departureTime: str  # datetime string
    arrivalTime: str  # datetime string
    price: float

@dataclass
class FrequentFlyer:
    Id: Optional[int]
    Username: str
    Password: str 
    FirstName: str
    LastName: str
    Email: str 
    PhoneNumber: str
    DateOfBirth: str  # datetime string
    PassportNumber: str

@dataclass
class Plane:
    Id: Optional[int]
    Manufacturer: str
    Nickname: str
    Year: int
    ImageUrl: Optional[str] = None


@dataclass
class Ticket:
    Id: Optional[int]
    BookingId: int
    FlightId: int
    Seat: str  
    PdfUrl: str  




