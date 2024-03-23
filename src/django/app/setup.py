import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookoverflow.settings")
django.setup()

from shared.models import *

def add__univeristy_record():
    longitude = -73.9712
    latitude = 40.7850
    record = University(
        domain="nyu.edu",
        name="New York University",
        location=Point(longitude, latitude)
    )
    record.save()

if __name__ == "__main__":
    add__univeristy_record()
