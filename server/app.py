#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api,Resource

from models import db , Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class AllResearch(Resource):
    def get(self):
        all_research = Research.query.all()
        dict_researches = [research.to_dict() for research in all_research]
        return make_response(dict_researches,200)
api.add_resource(AllResearch, '/research')

class ResearchById(Resource):
    def get(self,id):
        research_paper  = Research.query.filter_by(id=id).first()
        if not research_paper:
            return make_response({"error": "Research paper not found"},404)        
        return make_response(research_paper.to_dict(rules=('authors',)),200)
    
    def delete(self,id):
        research_paper  = Research.query.filter_by(id=id).first()
        if not research_paper:
            return make_response({"error": "Research paper not found"},404)        
        db.session.delete(research_paper)
        db.session.commit()
        return make_response('',201)
    
api.add_resource(ResearchById,'/research/<int:id>')

class Authors(Resource):
    def get(self):
        all_authors = Author.query.all()
        dict_authors = [author.to_dict() for author in all_authors]
        return make_response(dict_authors,200)
    
api.add_resource(Authors, '/authors')

class Research_Authors(Resource):
    def post(self):
        data = request.get_json()
        
        try:
            new_res_au  = ResearchAuthors(
                author_id=data['author_id'],
                research_id=data['research_id']
                )
            db.session.add(new_res_au)
            db.session.commit()
        except Exception as ex:
            return make_response({"errors": [ex.__str__()]},422)        
        return make_response(new_res_au.authors.to_dict(),201)
    
api.add_resource(Research_Authors, '/research_author')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
