#!/usr/bin/env python3

# Script goes here!

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Here we will have some test data to test the models relationships
def seed():

    # To dreate sample data
    deva = Dev(name="Joe")
    devb = Dev(name="Jim")

    companyx = Company(name="Mpesa")
    companyz = Company(name="Safaricom")
    
    freebie1 = Freebie(name="Free Water bottle", company=companyx, dev=deva)

    freebie2 = Freebie(name="Free Mac book", company=companyx, dev=devb)

    freebie3 = Freebie(name="Laptop", company=companyz, dev=deva)

    freebie4 = Freebie(name="Free Tshirt", company=companyz, dev=devb)
    
    # Before proceeding further we need to add the relationship between company and dev
    companyx.devs.append(deva)
    companyx.devs.append(devb)

    companyz.devs.append(devb)
    companyz.devs.append(deva)

    session.add(companyx)
    session.add(companyz)
    session.add(deva)

    session.commit()


    # Query and print details
    for freebie in session.query(Freebie).all():
        print(freebie.print_details())


    # Make Deva give a freebie to Devb
    freebie = session.query(Freebie).filter_by(name="Laptop").first()
    deva.give_away(devb, freebie)

    # Query and print the data to check relationships
    print(f"Company: {companyx.name} Freebies:")
    for freebie in companyx.freebies:
        print(f"  {freebie.print_details()}")

    print(f"\nCompany: {companyz.name} Freebies:")
    for freebie in companyz.freebies:
        print(f"  {freebie.print_details()}")
    
    # Check if Dev2 has received the "Laptop"
    print(f"\nHas Dev2 received a Laptop? {devb.received_one('Laptop')}")

    # Check if Dev2 has received the "Laptop"
    print(f"\nHas Dev2 received a Laptop? {devb.received_one('Laptop')}")


if __name__ == '__main__':
    seed()

    session.close()