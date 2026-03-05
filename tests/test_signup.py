"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_success(client, test_activities):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_duplicate_email(client, test_activities):
    """Test that signing up with duplicate email returns error."""
    # Try to sign up with an email that's already registered
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower() or "already" in data["detail"].lower()


def test_signup_activity_not_found(client, test_activities):
    """Test that signing up for non-existent activity returns 404."""
    response = client.post(
        "/activities/Non-existent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_adds_participant_to_list(client, test_activities):
    """Test that signup actually adds the participant to the activity."""
    # Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()["Programming Class"]["participants"])
    
    # Sign up new participant
    client.post(
        "/activities/Programming Class/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    new_count = len(response.json()["Programming Class"]["participants"])
    assert new_count == initial_count + 1
    assert "newstudent@mergington.edu" in response.json()["Programming Class"]["participants"]


def test_signup_empty_activity_then_add(client, test_activities):
    """Test signing up for an activity with no current participants."""
    response = client.post(
        "/activities/Gym Class/signup",
        params={"email": "gym_student@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify participant was added
    response = client.get("/activities")
    assert "gym_student@mergington.edu" in response.json()["Gym Class"]["participants"]
