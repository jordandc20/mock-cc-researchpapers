#!/usr/bin/env python3

from app import app
from models import db, Research, Author, ResearchAuthors

if __name__ == '__main__':
    with app.app_context():
        import ipdb; ipdb.set_trace()
        r1 = Research(topic = "AI In Day To Day Life", year = 1994, page_count = 10)