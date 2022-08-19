from app import app, db

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def to_json(self):
        return {
            "id": self.id,
            "title": self.name,
            "items": [i.to_json() for i in self.item]
        }

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    price = db.Column(db.Integer)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))

    item = db.relationship('Section', backref="item", lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.name,
            "modifiers": [i.to_json() for i in self.modifiersitem]
        }

class Modifiers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    modifiers = db.relationship('ModifiersItem', backref="Modifiers", lazy=True)


class ModifiersItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    modifiers_id = db.Column(db.Integer, db.ForeignKey('modifiers.id'))

    modifiersitem = db.relationship('Item', backref="modifiersitem", lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.Modifiers.name,
        }