from manage import db


class TestModel(db.Model):

    __tablename__ = 'test_model'
    number = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String(20))
    # date = db.Column(db.Date)


    def __repr__(self):
        return '<User %r>' % self.username



