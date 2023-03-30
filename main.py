from flask import Flask, request, jsonify, abort
from models import Group, Participant

app = Flask(__name__)

groups = []


@app.route('/group', methods=['POST'])
def new_group():
    name = request.get_json()["name"]
    description = None if "description" not in request.get_json() else request.get_json()["description"]
    groups.append(Group(name, description=description))
    return {"id": groups[-1].id}, "201"


@app.route('/groups', methods=['GET'])
def all_groups():
    data = [{"id": group.id, "name": group.name, "description": group.description} for group in groups]
    return jsonify(data)


@app.route('/group/<group_id>', methods=['GET', "PUT", 'DELETE'])
def get_group(group_id):
    groups_with_id = list(filter(lambda g: g.id == int(group_id), groups))
    if len(groups_with_id) == 0:
        abort(404)
    group = groups_with_id[0]
    if request.method == "GET":
        data = {"id": group_id, "name": group.name, "description": group.description,
                "participants": [{"id": participant.id, "name": participant.name, "wish": participant.id,
                "recipient": None if participant.recipient is None else {"id": participant.recipient.id, "name":
                                                                 participant.recipient.name, "wish":
            participant.recipient.wish}} for participant in group.participants]}
        return jsonify(data)
    elif request.method == 'PUT':
        name = request.get_json()["name"]
        description = None if "description" not in request.get_json() else request.get_json()["description"]
        groups.remove(group)
        group.name = name
        group.description = description
        groups.append(group)
        return 'ok', 200
    else:
        groups.remove(group)
        return 'ok', 204


@app.route('/group/<group_id>/participant', methods=['POST'])
def new_participant(group_id):
    groups_with_id = list(filter(lambda g: g.id == int(group_id), groups))
    if len(groups_with_id) == 0:
        abort(404)
    group = groups_with_id[0]
    name = request.get_json()["name"]
    wish = None if "wish" not in request.get_json() else request.get_json()["wish"]
    participant = Participant(name, wish=wish)
    groups.remove(group)
    group.participants.append(participant)
    groups.append(group)
    return {'id': group.participants[-1].id}, 201


@app.route('/group/<group_id>/participant/<participant_id>', methods=['DELETE'])
def delete_participant(group_id, participant_id):
    groups_with_id = list(filter(lambda g: g.id == int(group_id), groups))
    if len(groups_with_id) == 0:
        abort(404)
    group = groups_with_id[0]
    participant_with_id = list(filter(lambda p: p.id == int(participant_id), group.participants))
    if len(participant_with_id) == 0:
        abort(404)
    participant = participant_with_id[0]
    groups.remove(group)
    group.participants.remove(participant)
    groups.append(group)
    return 'ok', 204


@app.route('/group/<group_id>/toss', methods=['POST'])
def toss(group_id):
    groups_with_id = list(filter(lambda g: g.id == int(group_id), groups))
    if len(groups_with_id) == 0:
        abort(404)
    group = groups_with_id[0]
    if len(group.participants) < 3:
        abort(409)
    ids = list(map(lambda p: p.id, group.participants))
    print(ids)
    participants = []
    for p in group.participants:
        for i in ids:
            if i != p.id:
                participant_with_id = list(filter(lambda pg: pg.id == int(i), group.participants))
                p.recipient = participant_with_id[0]
                participants.append(p)
                ids.remove(i)
                break
    groups.remove(group)
    group.participants = participants
    groups.append(group)
    data = [{"id": p.id, "name": p.name, "wish": p.wish, "recipient": {"id": p.recipient.id, "name": p.recipient.name,
                                                                       "wish": p.recipient.wish}} for p in
            group.participants]
    return jsonify(data)


@app.route('/group/<group_id>/participant/<participant_id>/recipient', methods=['GET'])
def get_recipient(group_id, participant_id):
    groups_with_id = list(filter(lambda g: g.id == int(group_id), groups))
    if len(groups_with_id) == 0:
        abort(404)
    group = groups_with_id[0]
    participant_with_id = list(filter(lambda p: p.id == int(participant_id), group.participants))
    if len(participant_with_id) == 0:
        abort(404)
    participant = participant_with_id[0]
    data = {"id": participant.recipient.id, "name": participant.recipient.name, "wish": participant.recipient.wish}
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
