class MockLLM:

    def __init__(self):

        self.templates = {
            "login": self.login_case,
            "password": self.password_case,
            "register": self.register_case,
            "profile": self.profile_case
        }

    def generate(self, prompt: str):

        prompt = prompt.lower()

        for key, handler in self.templates.items():
            if key in prompt:
                return handler()

        return self.generic_case()

    # User can login
    def login_case(self):
        return {
            "test_cases": [
                {
                    "summary": "User can log in with valid credentials",
                    "description": "Precondition: User has a valid account. Steps: Enter valid username and password and submit the login form. Expected result: User is successfully logged in."
                },
                {
                    "summary": "Invalid password displays an error",
                    "description": "Precondition: User has a valid account. Steps: Enter a valid username and an incorrect password and submit the login form. Expected result: A clear error message is displayed and the user is not logged in."
                }
            ],
            "robot_framework": """
            *** Test Cases ***
                Login Test
                Open Browser    http://example.com
            """,
            "usability_tests": [
                {
                    "test": "User can easily understand and complete the login process.",
                    "test_case_keys": ["ABC-10", "ABC-11"]
                },
                {
                    "test": "User understands the error message when an invalid password is entered.",
                    "test_case_keys": ["ABC-11"]
                }
            ]
        }

    # User can reset password
    def password_case(self):
        return {
            "test_cases": [
                {
                    "summary": "User can request password reset",
                    "description": "Precondition: User has an account. Steps: Open the password reset page, enter a valid email address and submit the request. Expected result: A password reset request is successfully submitted."
                },
                {
                    "summary": "Invalid email shows error",
                    "description": "Precondition: User is on the password reset page. Steps: Enter an invalid email address and submit the request. Expected result: A clear validation error is displayed."
                }
            ],
            "robot_framework": """
            *** Test Cases ***
                Password Reset Test
            """,
            "usability_tests": [
                {
                    "test": "User can easily find and understand the password reset option.",
                    "test_case_keys": ["ABC-20"]
                },
                {
                    "test": "User understands the error message for an invalid email address.",
                    "test_case_keys": ["ABC-21"]
                }
            ]
        }

    # User can register account
    def register_case(self):
        return {
            "test_cases": [
                {
                    "summary": "User can register with valid information",
                    "description": "Precondition: User is on the registration page. Steps: Enter valid registration information and submit the form. Expected result: The account is created successfully."
                },
                {
                    "summary": "Registration fails when email is already in use",
                    "description": "Precondition: An account already exists with the email address. Steps: Enter the existing email address and submit the registration form. Expected result: A clear error message indicates that the email is already in use."
                },
                {
                    "summary": "Password must meet complexity requirements",
                    "description": "Precondition: User is on the registration page. Steps: Enter a password that does not meet the required complexity rules. Expected result: The user receives a clear validation message explaining the password requirements."
                },
                {
                    "summary": "Required fields must be completed",
                    "description": "Precondition: User is on the registration page. Steps: Leave one or more required fields empty and submit the form. Expected result: The user is prevented from registering and receives clear validation messages."
                }
            ],
            "robot_framework": """
            *** Test Cases ***
                User Registration Test
                Open Browser    http://example.com
                Click Element    register_button
                Input Text    email_field    test@example.com
                Input Text    password_field    SecurePassword123
                Click Button    submit_button
                Page Should Contain    Registration successful
            """,
            "usability_tests": [
                {
                    "test": "User can easily find the registration page.",
                    "test_case_keys": ["ABC-30"]
                },
                {
                    "test": "User understands the password requirements.",
                    "test_case_keys": ["ABC-32"]
                },
                {
                    "test": "User understands the validation messages when registration fails.",
                    "test_case_keys": ["ABC-31", "ABC-32", "ABC-33"]
                },
                {
                    "test": "User can complete registration without assistance.",
                    "test_case_keys": ["ABC-30", "ABC-31", "ABC-32", "ABC-33"]
                }
            ]
        }

    # User can edit profile
    def profile_case(self):
        return {
            "test_cases": [
                {
                    "summary": "User can update profile information successfully",
                    "description": "Precondition: User is logged in. Steps: Open profile settings, edit profile information and save the changes. Expected result: The updated profile information is saved successfully."
                },
                {
                    "summary": "Changes are saved and visible after refresh",
                    "description": "Precondition: User is logged in. Steps: Update profile information, save the changes and refresh the page. Expected result: The updated information is still displayed after refresh."
                },
                {
                    "summary": "Required fields cannot be left empty",
                    "description": "Precondition: User is editing their profile. Steps: Remove a required field value and attempt to save. Expected result: The user is prevented from saving and receives a clear validation message."
                },
                {
                    "summary": "Invalid email format is rejected",
                    "description": "Precondition: User is editing their profile. Steps: Enter an invalid email address and save. Expected result: The invalid email is rejected and a clear validation message is displayed."
                },
                {
                    "summary": "User receives confirmation after saving profile",
                    "description": "Precondition: User is editing their profile. Steps: Change profile information and save. Expected result: The user receives confirmation that the changes were saved."
                }
            ],
            "robot_framework": """
            *** Test Cases ***
                Edit Profile Test
                Open Browser    http://example.com
                Click Element    profile_menu
                Click Element    edit_profile_button
                Input Text    first_name_field    John
                Input Text    last_name_field    Doe
                Click Button    save_button
                Page Should Contain    Profile updated successfully
            """,
            "usability_tests": [
                {
                    "test": "User can easily find the profile settings page.",
                    "test_case_keys": ["ABC-40"]
                },
                {
                    "test": "User understands which fields can be edited.",
                    "test_case_keys": ["ABC-40"]
                },
                {
                    "test": "User can easily identify the save action.",
                    "test_case_keys": ["ABC-40", "ABC-41"]
                },
                {
                    "test": "User understands the validation messages.",
                    "test_case_keys": ["ABC-42", "ABC-43"]
                },
                {
                    "test": "User can confirm that profile changes were saved.",
                    "test_case_keys": ["ABC-41", "ABC-44"]
                }
            ]
        }

    # Generic user story
    def generic_case(self):
        return {
            "test_cases": [
                {
                    "summary": "Generic happy path",
                    "description": "Precondition: User can access the feature. Steps: Complete the main user flow with valid information. Expected result: The requested action is completed successfully."
                }
            ],
            "robot_framework": """
            *** Test Cases ***
                Generic Test
            """,
            "usability_tests": [
                {
                    "test": "User can understand and complete the task.",
                    "test_case_keys": ["ABC-50"]
                }
            ]
        }