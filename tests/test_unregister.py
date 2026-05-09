"""Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

import pytest


def test_unregister_success(client):
    """Test that a student can successfully unregister from an activity."""
    # Arrange
    email_to_remove = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email_to_remove in response.json()["message"]
    assert activity_name in response.json()["message"]


def test_unregister_removes_participant_from_activity(client):
    """Test that unregistering removes the participant from the activity's participants list."""
    # Arrange
    email_to_remove = "daniel@mergington.edu"
    activity_name = "Chess Club"
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    
    # Assert
    assert response.status_code == 200
    activities_after = client.get("/activities").json()
    assert email_to_remove not in activities_after[activity_name]["participants"]
    assert len(activities_after[activity_name]["participants"]) == initial_count - 1


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregistering from a non-existent activity returns 404."""
    # Arrange
    test_email = "student@mergington.edu"
    activity_name = "Nonexistent Activity"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_registered_returns_404(client):
    """Test that unregistering a non-registered student returns 404."""
    # Arrange
    test_email = "not.registered@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]


def test_unregister_twice_returns_404_second_time(client):
    """Test that unregistering the same participant twice returns 404 on second attempt."""
    # Arrange
    email_to_remove = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Act: First unregister should succeed
    response1 = client.delete(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    
    # Second unregister should fail
    response2 = client.delete(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 404
    assert "not registered" in response2.json()["detail"]


def test_unregister_response_format(client):
    """Test that unregister response has correct format."""
    # Arrange
    email_to_remove = "emma@mergington.edu"
    activity_name = "Programming Class"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)


def test_unregister_does_not_affect_other_activities(client):
    """Test that unregistering from one activity doesn't affect other activities."""
    # Arrange
    email = "emma@mergington.edu"
    activity1 = "Programming Class"
    activity2 = "Chess Club"
    
    # Act: Get initial participant counts
    initial_activities = client.get("/activities").json()
    initial_activity2_count = len(initial_activities[activity2]["participants"])
    
    # Unregister from activity1
    response = client.delete(
        f"/activities/{activity1}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify activity1 was modified
    activities_after = client.get("/activities").json()
    assert email not in activities_after[activity1]["participants"]
    
    # Verify activity2 was not affected
    assert len(activities_after[activity2]["participants"]) == initial_activity2_count
