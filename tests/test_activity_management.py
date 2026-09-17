from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_updates_activity_participants_immediately():
    activity_name = "Soccer Club"
    email = "new-player@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "participant-test@mergington.edu"

    sign_up_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert sign_up_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == (
        f"Unregistered {email} from {activity_name}"
    )

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
