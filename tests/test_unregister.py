"""Tests for DELETE /activities/{activity_name}/signup endpoint."""

import pytest


def test_unregister_success(client, test_activities):
    """Test successful unregister from an activity."""
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert "alice@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_not_registered(client, test_activities):
    """Test that unregistering non-existent participant returns error."""
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "notregistered@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"].lower() or "not" in data["detail"].lower()


def test_unregister_activity_not_found(client, test_activities):
    """Test that unregistering from non-existent activity returns 404."""
    response = client.delete(
        "/activities/Non-existent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_removes_participant(client, test_activities):
    """Test that unregister actually removes the participant from the activity."""
    # Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])
    
    # Unregister participant
    client.delete(
        "/activities/Chess Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    new_count = len(response.json()["Chess Club"]["participants"])
    assert new_count == initial_count - 1
    assert "alice@mergington.edu" not in response.json()["Chess Club"]["participants"]


def test_unregister_last_participant(client, test_activities):
    """Test unregistering the last participant from an activity."""
    response = client.delete(
        "/activities/Programming Class/signup",
        params={"email": "charlie@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify activity now has no participants
    response = client.get("/activities")
    assert len(response.json()["Programming Class"]["participants"]) == 0


def test_unregister_then_signup_again(client, test_activities):
    """Test that a participant can sign up again after unregistering."""
    # Unregister
    client.delete(
        "/activities/Chess Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    
    # Sign up again
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify participant is in the list
    response = client.get("/activities")
    assert "alice@mergington.edu" in response.json()["Chess Club"]["participants"]
