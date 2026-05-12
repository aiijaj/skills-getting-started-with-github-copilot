from urllib.parse import quote


def test_get_activities(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    sign_up_url = f"/activities/{quote(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(sign_up_url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    sign_up_url = f"/activities/{quote(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(sign_up_url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_delete_participant_unregisters_client(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    delete_url = f"/activities/{quote(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(delete_url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_delete_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    delete_url = f"/activities/{quote(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(delete_url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
