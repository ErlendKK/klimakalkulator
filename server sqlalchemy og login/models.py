from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
import os
from sqlalchemy.exc import IntegrityError
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    photo_filename = db.Column(db.String)

    projects = db.relationship('Project', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_file(file):
        filename = file.filename
        file_format_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
        file_size_allowed = file.content_length <= 5 * 1024 * 1024
        return file_format_allowed and file_size_allowed

    def get_photo_url(self):
        return f"{app.config['SERVER_URL']}/user_data/{self.photo_filename}" if self.photo_filename else None

    @classmethod
    def add_user(cls, data):
        user = cls(
            name=data.get('name'),
            email=data.get('email'),
            photo_filename=data.get('photo_filename')
        )
        user.set_password(data.get('password'))
        try:
            db.session.add(user)
            db.session.commit()
            return {"status": "success", "user_data": user}
        except IntegrityError:
            db.session.rollback()
            return {"status": "failed", "message": "Email already registered"}

    @classmethod
    def get_user_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def rename_and_store_photo(self, photo):
        try:
            original_filename = secure_filename(photo.filename)
            unique_id = uuid.uuid4().hex
            extension = original_filename.rsplit('.', 1)[1].lower()
            self.photo_filename = f"{unique_id}.{extension}"
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], self.photo_filename)
            photo.save(photo_path)
            return self.photo_filename
        except Exception as e:
            return None



class Project(db.Model):
    __tablename__ = 'Projects'
    project_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    bta = db.Column(db.Float, nullable=False)
    prosjektstart = db.Column(db.Integer, nullable=False)
    analyseperiode = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    created_date = db.Column(db.String, nullable=False)
    updated_date = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)

class Product(db.Model):
    __tablename__ = 'Products'
    product_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.project_id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    bygningsdel = db.Column(db.String, nullable=False)
    produktgruppe = db.Column(db.String, nullable=False)
    utskiftingsintervall = db.Column(db.Integer, nullable=False)
    vedlikeholdsutslipp = db.Column(db.Float, nullable=False)
    type = db.Column(db.String, nullable=False)
    uuid = db.Column(db.String)
    owner = db.Column(db.String)
    name = db.Column(db.String)
    regNo = db.Column(db.String)
    validUntil = db.Column(db.String)
    classific = db.Column(db.String)

class EmissionFactor(db.Model):
    __tablename__ = 'EmissionFactors'
    emission_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id'), nullable=False)
    A1 = db.Column(db.Float)
    A2 = db.Column(db.Float)
    A3 = db.Column(db.Float)
    A1A2A3 = db.Column(db.Float)
    A4 = db.Column(db.Float)
    C1 = db.Column(db.Float)
    C2 = db.Column(db.Float)
    C3 = db.Column(db.Float)
    C4 = db.Column(db.Float)
    D = db.Column(db.Float)
