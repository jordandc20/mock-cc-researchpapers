from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Research(db.Model,SerializerMixin):
    __tablename__ = 'researches'
    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_Authors = db.relationship("ResearchAuthors", backref="research_paper")
    authors = association_proxy('research_Authors', 'authors')

    serialize_rules = ('-research_Authors','-authors.research_paper','-created_at','-updated_at')
    
    @validates('year')
    def validate_year(self,key,value):
        if not len(str(value)) == 4:
            raise ValueError('year must be 4 digits')
        return value
        
class ResearchAuthors(db.Model,SerializerMixin):
    __tablename__ = "research_Authors"
    id = db.Column(db.Integer, primary_key = True)
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    serialize_rules = ('-authors.research_Authors','-research_paper.research_Authors','-created_at','-updated_at',)
    
    
class Author(db.Model,SerializerMixin):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    research_Authors = db.relationship("ResearchAuthors", backref="authors")
    researches = association_proxy('research_Authors', 'research_paper')

    serialize_rules = ('-research_Authors','-researches.authors','-created_at','-updated_at',)

    @validates('field_of_study')
    def validate_field_of_study(self,key,value):
        vals = ['AI', 'Robotics', 'Machine Learning', 'Vision', 'Cybersecurity']
        if value not in vals:
            raise ValueError('Field of study must be in allowed set')
        return value