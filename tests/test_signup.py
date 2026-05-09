"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_success(client):
    """Test that a student can successfully sign up for an activity."""
    # Arrange
    test_email = "alex@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert test_email in response.json()["message"]
    assert activity_name in response.json()["message"]


def test_signup_adds_participant_to_activity(client, reset_activities):
    """Test that signing up adds the participant to the activity's participants list."""
    # Arrange
    test_email = "new.student@mergington.edu"
    activity_name = "Programming Class"
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 200
    activities_after = client.get("/activities").json()
    assert test_email in activities_after[activity_name]["participants"]
    assert len(activities_after[activity_name]["participants"]) == initial_count + 1


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404."""
    # Arrange
    test_email = "student@mergington.edu"
    activity_name = "Nonexistent Activity"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email_returns_400(client):
    """Test that signing up with the same email twice returns 400."""
    # Arrange
    test_email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Act: Try to sign up a user already registered for the activity
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_same_email_different_activities_allowed(client):
    """Test that a student can sign up for multiple different activities."""
    # Arrange
    test_email = "TestStudent@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Act: Sign up for first activity
    response1 = client.post(
        f"/activities/{activity1}/signup?email={test_email}"
    )
    
    # Sign up for second activity
    response2 = client.post(
        f"/activities/{activity2}/signup?email={test_email}"
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities = client.get("/activities").json()
    assert test_email in activities[activity1]["participants"]
    assert test_email in activities[activity2]["participants"]


def test_signup_response_format(client):
    """Test that signup response has correct format."""
    # Arrange
    test_email = "format.test@mergington.edu"
    activity_name = "Gym Class"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
