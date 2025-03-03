from sqlalchemy import (ForeignKey, Column, Integer, String, MetaData, Table, create_engine)
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Here we defining many to many reationship between devs and companies
company_dev_rel = Table('company_dev_rel', Base.metadata,
                        Column('company_id', Integer, ForeignKey('companies.id')),
                        Column('dev_id', Integer, ForeignKey('devs.id'))
    )


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # one to many relationship between companies and freebies
    freebies = relationship('Freebie', back_populates='company')

    # many to many relationship between companies and devs
    devs = relationship('Dev', secondary='company_dev_rel', back_populates="companies")

   
    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(name=item_name, dev=dev, company=self)
        session.add(new_freebie)
        session.commit()
        return new_freebie
    
    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_Year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())



    # one to many relationship between Dev and freebies
    freebies = relationship('Freebie', back_populates='dev')

    # Many to mant relationship between Dev and Company
    companies = relationship('Company', secondary='company_dev_rel', back_populates='devs')

    def __repr__(self):
        return f'<Dev {self.name}>'
    

    #Method to check if the dev has received a specific freebie
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.name == item_name:
                return True
        return False

    # Method to give away a freebie to another dev
    def give_away(self, dev, freebie):
        # Only proceed if this dev owns the freebie
        if freebie.dev == self:
            freebie.dev = dev
            session.commit()  # Commit the transaction to the database
            return True
        return False


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    name = Column(String())

    # We then go ahead and define the FOREIGN KEYS
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    #Defining the relationships between Freebie to Dev and Freebie to company
    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')
     


    def print_details(self):
        return f"{self.dev.name} owns a {self.name} from {self.company.name}."

# Creating the database with sqlite3
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

