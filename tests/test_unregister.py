from src import app as app_module


def test_unregister_removes_an_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_not_found_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}


def test_unregister_allows_the_same_participant_to_sign_up_again(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    assert app_module.activities[activity_name]["participants"].count(email) == 1