"""Tests for GET /activities endpoint."""

import pytest


def test_get_activities_success(client, test_activities):
    """Test that GET /activities returns all activities with correct structure."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify all test activities are returned
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_returns_correct_data(client, test_activities):
    """Test that activities include all required fields."""
    response = client.get("/activities")
    activities = response.json()
    
    chess_club = activities["Chess Club"]
    
    # Verify all required fields are present
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    # Verify values are correct
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert chess_club["max_participants"] == 12


def test_get_activities_participants_list(client, test_activities):
    """Test that activities return the correct participants list."""
    response = client.get("/activities")
    activities = response.json()
    
    # Chess Club should have 2 participants
    assert len(activities["Chess Club"]["participants"]) == 2
    assert "alice@mergington.edu" in activities["Chess Club"]["participants"]
    assert "bob@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Programming Class should have 1 participant
    assert len(activities["Programming Class"]["participants"]) == 1
    assert "charlie@mergington.edu" in activities["Programming Class"]["participants"]
    
    # Gym Class should have 0 participants
    assert len(activities["Gym Class"]["participants"]) == 0
