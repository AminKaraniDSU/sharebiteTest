from os import abort
from app import app, db
import json
from models import *
from flask import request
from flask import jsonify

@app.route("/api/test", methods=['GET'])
def test_api():
    return json.dumps({"test":"test"})

@app.route("/api/menu", methods=['GET'])
def menu_builder():
    menus = db.session.query(Section).all()
    menus = [menu.to_json() for menu in menus]
    return jsonify(menus)

@app.route("/api/menu/<int:id_menu>", methods=["GET"])
def get_menu(id_menu):
    menus = Section.query.get(id_menu)
    if menus is None:
        return json.dumps({"success": False, "data": "No data found"})
    return jsonify(menus.to_json())

@app.route('/api/menu', methods=['POST'])
def create_menu():
    if not request.json:
        return json.dumps({"success": False, "data": "No json in request"})
    menu = Section(
        name=request.json.get('title'),
        description=request.json.get('description')
    )
    db.session.add(menu)
    db.session.commit()
    return {"id": menu.id, "name": menu.name, "description": menu.description}, 201

@app.route('/api/menu/<int:id_menu>', methods=['PUT'])
def update_menu(id_menu):
    if not request.json:
        return json.dumps({"success": False, "data": "No json in request"})
    menu = Section.query.get(id_menu)
    if menu is None:
        return json.dumps({"success": False, "data": "No data found"})
    menu.name = request.json.get('title', menu.name)
    menu.description = request.json.get('description', menu.description)
    db.session.commit()
    return jsonify(menu.to_json())


@app.route("/api/menu/<int:id_menu>", methods=["DELETE"])
def delete_menu(id_menu):
    menu = Section.query.get(id_menu)
    if menu is None:
        return json.dumps({"success": False, "data": "No data found"})
    item = db.session.query(Item).filter(Item.section_id == id_menu).all()
    if item is not None:
        return json.dumps({"success": False, "data": "Cant delete as it belong to some items"})
    db.session.delete(menu)
    db.session.commit()
    return jsonify({'result': True})






@app.route("/api/item/<int:id_item>", methods=["GET"])
def get_item(id_item):
    item = Item.query.get(id_item)
    if item is None:
        return json.dumps({"success": False, "data": "No data found"})
    return jsonify(item.to_json())

@app.route('/api/item', methods=['POST'])
def create_item():
    if not request.json:
        return json.dumps({"success": False, "data": "No json in request"})
    sec = db.session.query(Section).filter(Section.id == request.json.get('section_id')).first()
    if sec is None:
        return json.dumps({"success": False, "data": "session not found"})
    item = Item(
        name=request.json.get('title'),
        description=request.json.get('description'),
        price=request.json.get('price'),
        section_id=request.json.get('section_id'),
    )
    db.session.add(item)
    db.session.commit()
    return {"id": item.id, "name": item.name, "description": item.description,
            "price": item.id, "section_id": item.section_id}, 201

@app.route('/api/item/<int:id_item>', methods=['PUT'])
def update_item(id_item):
    if not request.json:
        return json.dumps({"success": False, "data": "No json in request"})
    item = Item.query.get(id_item)
    if item is None:
        return json.dumps({"success": False, "data": "No data found"})
    item.name = request.json.get('title', item.name)
    item.description = request.json.get('description', item.description)
    item.price = request.json.get('price', item.price)
    db.session.commit()
    return jsonify(item.to_json())


@app.route("/api/item/<int:id_item>", methods=["DELETE"])
def delete_item(id_item):
    item = Item.query.get(id_item)
    if item is None:
        return json.dumps({"success": False, "data": "No data found"})
    modifiers = db.session.query(ModifiersItem).filter(ModifiersItem.item_id == id_item).all()
    if item is not None:
        for modifier in modifiers:
            db.session.delete(modifier)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'result': True})








@app.route("/api/modifiers/<int:id_modifiers>", methods=["GET"])
def get_modifiers(id_modifiers):
    modifiers = Modifiers.query.get(id_modifiers)
    if modifiers is None:
        return json.dumps({"success": False, "data": "No data found"})
    return jsonify(modifiers.to_json())

@app.route('/api/modifiers', methods=['POST'])
def create_modifiers():
    if not request.json:
        return json.dumps({"success": False, "data": "No json in request"})
    modifiers = Modifiers(
        name=request.json.get('title'),
        description=request.json.get('description')
    )
    db.session.add(modifiers)
    db.session.commit()
    return {"id": modifiers.id, "name": modifiers.name, "description": modifiers.description}, 201

@app.route('/api/modifiers/<int:id_modifiers>', methods=['PUT'])
def update_modifiers(id_modifiers):
    if not request.json:
        return json.dumps({"success": False, "data": "No json in request"})
    modifiers = Modifiers.query.get(id_modifiers)
    if modifiers is None:
        return json.dumps({"success": False, "data": "No data found"})
    modifiers.name = request.json.get('title', modifiers.name)
    modifiers.description = request.json.get('description', modifiers.description)
    db.session.commit()
    return jsonify(modifiers.to_json())


@app.route("/api/modifiers/<int:id_modifiers>", methods=["DELETE"])
def delete_modifiers(id_modifiers):
    modifiers = Modifiers.query.get(id_modifiers)
    if modifiers is None:
        return json.dumps({"success": False, "data": "No data found"})
    modifiers_item = db.session.query(ModifiersItem).filter(ModifiersItem.modifiers_id == id_modifiers).all()
    if modifiers_item is not None:
        return json.dumps({"success": False, "data": "Cant delete as it belong to some items"})
    db.session.delete(modifiers)
    db.session.commit()
    return jsonify({'result': True})

@app.route("/api/map_items_n_modifiers", methods=["POST"])
def map_items_n_modifiers():
    if not request.json:
        return json.dumps({"success": False, "data": "No json in request"})
    modifiers_item = ModifiersItem(
        item_id=request.json.get('item_id'),
        modifiers_id=request.json.get('modifiers_id')
    )
    db.session.add(modifiers_item)
    db.session.commit()
    return {"id": modifiers_item.id, "item_id": modifiers_item.item_id,
            "modifiers_id": modifiers_item.modifiers_id}, 201


@app.route("/api/unmap_items_n_modifiers", methods=["POST"])
def unmap_items_n_modifiers():
    if not request.json:
        return json.dumps({"success": False, "data": "No json in request"})
    item_id = request.json.get('item_id'),
    modifiers_id = request.json.get('modifiers_id')
    modifiers_item = db.session.query(ModifiersItem).filter(ModifiersItem.item_id == item_id).fillter(
        ModifiersItem.modifiers_id == modifiers_id
    ).first()
    if modifiers_item is None:
        return json.dumps({"success": False, "data": "No json in request"})
    db.session.delete(modifiers_item)
    db.session.commit()
    return jsonify({'result': True})