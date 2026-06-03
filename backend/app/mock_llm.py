class MockLLM:

    def generate(self, prompt: str):

        prompt = prompt.lower()

    # User can login
        if "login" in prompt:
            return {
                "test_cases": [
                    "User can login with valid credentials",
                    "Invalid password shows error"
                ],
                "robot_framework": """
                *** Test Cases ***
                    Login Test
                    Open Browser    http://example.com
                """,
                "usability_tests": [
                    "Can user find login button?",
                    "Is login form understandable?"
                ]
            }
    # User can reset password
        if "password" in prompt: 
            return {
                "test_cases": [
                    "User can request password reset",
                    "Invalid email shows error"
                ],
                "robot_framework": """
                *** Test Cases ***
                    Password Reset Test
                """,
                "usability_tests": [
                    "Is reset link easy to find?"
                ]
            }
    # User can register account
        if "register" in prompt: 
            return {
                "test_cases": [
                    "User can register with valid information",
                    "Registration fails when email is already in use",
                    "Password must meet complexity requirements",
                    "Required fields must be completed"
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
                    "Can users find the registration page easily?",
                    "Do users understand the password requirements?",
                    "Are validation messages clear and actionable?",
                    "Can users complete registration without assistance?"
                ]
            }
    # User can edit profile
        if "profile" in prompt: 
            return {
                "test_cases": [
                    "User can update profile information successfully",
                    "Changes are saved and visible after refresh",
                    "Required fields cannot be left empty",
                    "Invalid email format is rejected",
                    "User receives confirmation after saving profile"
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
                    "Can users easily find the profile settings page?",
                    "Do users understand which fields can be edited?",
                    "Is the save action clearly visible?",
                    "Are validation messages understandable?",
                    "Can users confirm that changes were saved?"
                ]
            }

        return {
            "test_cases": [
                "Generic happy path"
            ],
            "robot_framework": """
                *** Test Cases ***
                Generic Test
            """,
            "usability_tests": [
                "Can user complete task?"
            ]
        }