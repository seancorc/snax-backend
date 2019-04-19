from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Restraunt(db.Model):
    __tablename__ = 'restraunt'
    id = db.Column(db.Integer, primary_key=True)
    menu = db.relationship('Menu')
    name = db.Column(db.String, nullable=False)
    

    def __init__(self, **kwargs):
        self.menu = kwargs.get('menu')
        self.name = kwargs.get('name')

    
class Menu(db.model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    restrauntID = db.Column(db.Integer, db.foreignkey('restraunt.id'))
    #db.relationship('Restraunt') Use this if we want a bidirectional many to one relationship from Menu back to Restraunt 

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.restrauntID = kwargs.get('restrauntID')
