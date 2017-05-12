# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cpd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Disposal(db.Model):
    email_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(120))
    date_posted = db.Column(db.Date)
    rent = db.Column(db.Float)
    size = db.Column(db.String(30))
    size_max = db.Column(db.Float)
    size_min = db.Column(db.Float)
    lease = db.Column(db.String(120))
    rates = db.Column(db.Float)
    service = db.Column(db.Float)
    address = db.Column(db.String(120))
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    post_code = db.Column(db.String(10))
    area_code = db.Column(db.String(5))
    hood = db.Column(db.String(60))
    my_hood = db.Column(db.String(60))

    def __init__(self, email_id, location, date_posted, rent, size, size_max, size_min, hood, my_hood,
                 size_avg, address, lng, lat, post_code, area_code, lease, rates, service):
        self.email_id = email_id
        self.location = location
        self.size = size
        self.size_max = size_max
        self.size_avg = size_avg
        self.size_min = size_min
        self.rent = rent
        self.date_posted = date_posted
        self.lease = lease
        self.rates = rates
        self.service = service
        self.address = address
        self.lng = lng
        self.lat = lat
        self.post_code = post_code
        self.area_code = area_code
        self.hood = hood
        self.my_hood = my_hood

    def __repr__(self):
        s = \
            '<Location {}>' + \
            '<date_posted {}>' + \
            '<service {}>'
        return s.format(self.location, self.date_posted, self.service)

    def to_dict(self):
        d = self.__dict__
        if '_sa_instance_state' in d:
            d.pop('_sa_instance_state')
        return d


class Acquisition(db.Model):
    email_id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.Date)
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    size_max = db.Column(db.Float)
    size_min = db.Column(db.Float)
    size = db.Column(db.String(30))
    areas = db.Column(db.String(500))

    def __init__(self, email_id, budget_min, budget_max, areas, size_max, size_min, date_posted, size):
        self.areas = areas
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.size_max = size_max
        self.size_min = size_min
        self.size = size
        self.email_id = email_id
        self.date_posted = date_posted

    def to_dict(self):
        d = self.__dict__
        if '_sa_instance_state' in d:
            d.pop('_sa_instance_state')
        return d


class AcquisitionArea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.Integer)
    description = db.Column(db.String(60))

    def __init__(self, email_id, description):
        self.email_id = email_id
        self.description = description

    def to_dict(self):
        d = self.__dict__
        if '_sa_instance_state' in d:
            d.pop('_sa_instance_state')
        return d


class RejectedArea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(500))

    def __init__(self, description):
        self.description = description

    def to_dict(self):
        d = self.__dict__
        if '_sa_instance_state' in d:
            d.pop('_sa_instance_state')
        return d


