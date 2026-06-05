from src import app as app_module


def test_signup_adds_a_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_rejects_a_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}
    assert app_module.activities[activity_name]["participants"].count(email) == 1


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_allows_same_student_in_different_activities(client):
    # Arrange
    email = "multi-activity@mergington.edu"

    # Act
    chess_response = client.post("/activities/Chess Club/signup", params={"email": email})
    science_response = client.post("/activities/Science Club/signup", params={"email": email})

    # Assert
    assert chess_response.status_code == 200
    assert science_response.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]
    assert email in app_module.activities["Science Club"]["participants"]