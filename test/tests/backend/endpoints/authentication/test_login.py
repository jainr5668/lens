import json
import requests
from tests.backend.constants import Schema_Files, Status_Code, Test_USER_Credentials

url = "http://localhost:8000/endpoints/auth/login"


def test_auth_login(framework):
    """Test to check the login endpoint"""

    framework.log.info("Adding Test User")
    framework.add_test_user("level_5")
    payload = {
        "email": Test_USER_Credentials.EMAIL,
        "password": Test_USER_Credentials.PASSWORD,
    }
    framework.log.step("Make a POST request to /endpoints/auth/login")
    response = framework.requests.post(url, payload)
    actual_response = response.body

    framework.log.step("Verify 200 status code is returned")
    assert Status_Code.CREATED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.CREATED} but got {response.status_code}"
    )

    framework.log.step("Verify response body")

    assert "token" in actual_response, framework.log.error(
        f"response is not as expected: {actual_response}"
    )


def test_auth_login_verbs(framework):
    """Tests that only POST method is allowed for /auth/login and will return 405 for other methods."""

    framework.log.step("Call /endpoints/auth/login with verb GET")
    headers = framework.get_admin_headers
    response = framework.requests.get(url=url, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/login with verb PATCH")
    response = framework.requests.patch(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/login with verb PUT")
    response = framework.requests.put(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/login with verb DELETE")
    response = framework.requests.delete(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/login with verb OPTIONS")
    response = framework.requests.request(method="options", url=url, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )


def test_auth_login_invalid_email(framework):
    """Test to check the login endpoint"""

    framework.log.info("Adding Test User")
    framework.add_test_user("level_5")
    payload = {
        "email": "test@lens.com",
        "password": Test_USER_Credentials.PASSWORD,
    }
    framework.log.step("Make a POST request to /endpoints/auth/login")
    response = framework.requests.post(url, payload)

    framework.log.step("Verify 401 status code is returned")
    assert Status_Code.UNAUTHORIZED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.UNAUTHORIZED} but got {response.status_code}"
    )


def test_auth_login_invalid_password(framework):
    """Test to check the login endpoint"""

    framework.log.info("Adding Test User")
    framework.add_test_user("level_5")
    payload = {
        "email": Test_USER_Credentials.EMAIL,
        "password": "12345678",
    }
    framework.log.step("Make a POST request to /endpoints/auth/login")
    response = framework.requests.post(url, payload)

    framework.log.step("Verify 401 status code is returned")
    assert Status_Code.UNAUTHORIZED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.UNAUTHORIZED} but got {response.status_code}"
    )

    framework.log.step("Verify response body")
    assert framework.utility.response_validator(
        response.body, Schema_Files.AUTHENTICATION
    )


def test_auth_login_empty_payload(framework):
    """Test to check the login endpoint"""

    framework.log.info("Adding Test User")
    framework.add_test_user("level_5")
    payload = {}
    framework.log.step("Make a POST request to /endpoints/auth/login")
    response = framework.requests.post(url, payload)

    framework.log.step("Verify 400 status code is returned")
    assert Status_Code.BAD_REQUEST == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.BAD_REQUEST} but got {response.status_code}"
    )

    framework.log.step("Verify response body")
    assert framework.utility.response_validator(
        response.body, Schema_Files.AUTHENTICATION
    )
