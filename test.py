import requests


class TestGroupPost:
    def test_group_with_d(self):
        r = requests.post("http://localhost:8080/group", json={"name": "test_d", "description": "test"})
        assert r.status_code == 201
        assert 'id' in r.json()

    def test_group_without_d(self):
        r = requests.post("http://localhost:8080/group", json={"name": "test"})
        assert r.status_code == 201
        assert 'id' in r.json()


class TestAllGroups:
    def test_all_groups(self):
        r = requests.get("http://localhost:8080/groups")
        assert r.status_code == 200
        r = r.json()
        assert len(r) > 0
        assert 'id' in r[0]
        assert 'name' in r[0]
        assert 'description' in r[0]


class TestConcreteGroups:
    def test_correct_get(self):
        r = requests.get("http://localhost:8080/group/1")
        assert r.status_code == 200
        r = r.json()
        assert 'id' in r
        assert 'name' in r
        assert 'description' in r
        assert 'participants' in r

    def test_incorrect_get(self):
        r = requests.get("http://localhost:8080/group/100000")
        assert r.status_code == 404

    def test_correct_put(self):
        r = requests.put("http://localhost:8080/group/1", json={"name": "test_put"})
        assert r.status_code == 200

    def test_incorrect_put(self):
        r = requests.put("http://localhost:8080/group/100000", json={"name": "test"})
        assert r.status_code == 404

    def test_correct_delete(self):
        r = requests.delete("http://localhost:8080/group/2")
        assert r.status_code == 204

    def test_incorrect_delete(self):
        r = requests.delete("http://localhost:8080/group/100000")
        assert r.status_code == 404


class TestParticipantPost:
    def test_participant_with_w(self):
        r = requests.post("http://localhost:8080/group/1/participant", json={"name": "test_u_w", "wish": "test"})
        assert r.status_code == 201
        assert 'id' in r.json()

    def test_participant_without_w(self):
        r = requests.post("http://localhost:8080/group/1/participant", json={"name": "test"})
        assert r.status_code == 201
        assert 'id' in r.json()

    def test_incorrect(self):
        r = requests.post("http://localhost:8080/group/100000/participant", json={"name": "test_error"})
        assert r.status_code == 404


class TestParticipantDelete:
    def test_correct(self):
        r = requests.delete("http://localhost:8080/group/1/participant/1")
        assert r.status_code == 204

    def test_group_incorrect(self):
        r = requests.delete("http://localhost:8080/group/100000/participant/1")
        assert r.status_code == 404

    def test_participant_incorrect(self):
        r = requests.delete("http://localhost:8080/group/1/participant/1000000")
        assert r.status_code == 404


class TestToss:
    def test_incorrect_id(self):
        r = requests.post("http://localhost:8080/group/100000/toss")
        assert r.status_code == 404

    def test_incorrect_toss(self):
        r = requests.post("http://localhost:8080/group/1/toss")
        assert r.status_code == 409

    def test_correct_toss(self):
        requests.post("http://localhost:8080/group/1/participant", json={"name": "test2"})
        requests.post("http://localhost:8080/group/1/participant", json={"name": "test3"})
        r = requests.post("http://localhost:8080/group/1/toss")
        assert r.status_code == 200
        r = r.json()
        assert len(r) > 0
        assert 'id' in r[0]
        assert 'name' in r[0]
        assert 'wish' in r[0]
        assert 'recipient' in r[0]


class TestRecipient:
    def test_correct(self):
        r = requests.get("http://localhost:8080/group/1/participant/1/recipient")
        assert r.status_code == 200
        r = r.json()
        assert 'id' in r
        assert 'name' in r
        assert 'with' in r

    def test_incorrect_group(self):
        r = requests.get("http://localhost:8080/group/1000000/participant/2/recipient")
        assert r.status_code == 404

    def test_incorrect_participant(self):
        r = requests.get("http://localhost:8080/group/1/participant/1000000/recipient")
        assert r.status_code == 404
