"""Tests for the GET /activities endpoint."""

import pytest


def test_get_activities_success(client):
    """Test that GET /activities returns all activities with correct structure."""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert all(activity in activities for activity in expected_activities)


def test_get_activities_contains_required_fields(client):
    """Test that each activity has all required fields."""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields"


def test_get_activities_participants_is_list(client):
    """Test that participants field is a list of strings."""
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list), \
            f"Participants for '{activity_name}' is not a list"
        for participant in activity_data["participants"]:
            assert isinstance(participant, str), \
                f"Participant '{participant}' in '{activity_name}' is not a string"


def test_get_activities_has_initial_participants(client):
    """Test that initial activities have expected participants."""
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert activities["Chess Club"]["participants"] == expected_chess_participants
