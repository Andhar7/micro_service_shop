# User Service Test Commands

This document contains all commands to run tests for the User Service.

## Prerequisites

Make sure you have the Django environment set up and dependencies installed:

```bash
# Activate virtual environment (if using one)
source ckg/bin/activate  # or your virtual environment path

# Install dependencies
pip install -r requirements.txt  # if requirements.txt exists
```

## Basic Test Commands

### Run All Tests
```bash
python manage.py test
```

### Run All Tests with Verbose Output
```bash
python manage.py test -v 2
```

### Run Only User App Tests
```bash
python manage.py test apps.users
```

### Run Tests with Keep Database (faster for repeated runs)
```bash
python manage.py test apps.users --keepdb
```

## Specific Test Class Commands

### Run User Model Tests
```bash
python manage.py test apps.users.tests.UserModelTest
```

### Run User Profile Model Tests
```bash
python manage.py test apps.users.tests.UserProfileModelTest
```

### Run User Registration API Tests
```bash
python manage.py test apps.users.tests.UserRegistrationAPITest
```

### Run User Profile API Tests
```bash
python manage.py test apps.users.tests.UserProfileAPITest
```

### Run Serializer Tests
```bash
python manage.py test apps.users.tests.UserSerializerTest
```

### Run Integration Tests
```bash
python manage.py test apps.users.tests.AuthenticationIntegrationTest
```

## Specific Test Method Commands

### Run Single Test Method
```bash
python manage.py test apps.users.tests.UserRegistrationAPITest.test_register_user_success
```

### Run Multiple Specific Tests
```bash
python manage.py test apps.users.tests.UserModelTest.test_create_user apps.users.tests.UserRegistrationAPITest.test_register_user_success
```

## Test Coverage Commands

### Install Coverage (if not already installed)
```bash
pip install coverage
```

### Run Tests with Coverage
```bash
coverage run --source='.' manage.py test apps.users
```

### Generate Coverage Report
```bash
coverage report
```

### Generate HTML Coverage Report
```bash
coverage html
```

### View Coverage Report in Browser
```bash
# After running coverage html
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

## Test Database Commands

### Run Tests with Custom Database Settings
```bash
python manage.py test apps.users --settings=config.test_settings
```

### Run Tests with In-Memory Database (faster)
```bash
python manage.py test apps.users --settings=config.test_settings --keepdb
```

## Debugging Test Commands

### Run Tests with Python Debugger
```bash
python manage.py test apps.users --debug-mode
```

### Run Tests with PDB on Failure
```bash
python manage.py test apps.users --pdb
```

### Run Tests in Parallel (faster for large test suites)
```bash
python manage.py test apps.users --parallel auto
```

## Test Output Formats

### Run Tests with Minimal Output
```bash
python manage.py test apps.users -v 0
```

### Run Tests with Maximum Verbosity
```bash
python manage.py test apps.users -v 3
```

### Run Tests and Save Output to File
```bash
python manage.py test apps.users > test_results.txt 2>&1
```

## Continuous Integration Commands

### Run Tests with XML Output (for CI)
```bash
# Install django-nose for XML output
pip install django-nose

# Add to settings.py:
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# NOSE_ARGS = ['--with-xunit', '--xunit-file=test-results.xml']

python manage.py test apps.users
```

### Run Tests with JUnit XML Output
```bash
# Using pytest-django (alternative)
pip install pytest-django pytest-cov
pytest apps/users/tests.py --junitxml=test-results.xml --cov=apps.users
```

## Manual API Testing

### Run Manual API Tests (Original Bash Script)
```bash
# Make sure the server is running first
python manage.py runserver

# In another terminal, run the manual tests
chmod +x apps/users/test_api_manual.sh
./apps/users/test_api_manual.sh
```

## Performance Testing

### Run Tests with Time Measurement
```bash
time python manage.py test apps.users
```

### Run Tests with Memory Profiling
```bash
# Install memory-profiler
pip install memory-profiler

# Run with memory profiling
python -m memory_profiler manage.py test apps.users
```

## Environment-Specific Commands

### Run Tests for Development
```bash
DJANGO_SETTINGS_MODULE=config.settings python manage.py test apps.users
```

### Run Tests for Production (with production-like settings)
```bash
DJANGO_SETTINGS_MODULE=config.production_settings python manage.py test apps.users
```

## Quick Test Commands for Development

### Run Failed Tests Only (after a test run)
```bash
python manage.py test apps.users --failfast
```

### Run Tests and Stop on First Failure
```bash
python manage.py test apps.users --failfast
```

### Run Tests with Tags (if using Django's test tags)
```bash
python manage.py test apps.users --tag=unit
python manage.py test apps.users --tag=integration
```

## Best Practices

1. **Run tests before committing code:**
   ```bash
   python manage.py test apps.users
   ```

2. **Run tests with coverage to ensure good test coverage:**
   ```bash
   coverage run --source='.' manage.py test apps.users && coverage report
   ```

3. **Use keepdb for faster repeated test runs during development:**
   ```bash
   python manage.py test apps.users --keepdb -v 2
   ```

4. **Run specific failing tests to debug issues:**
   ```bash
   python manage.py test apps.users.tests.UserRegistrationAPITest.test_register_user_success -v 2
   ```

## Notes

- The original bash script has been renamed to `test_api_manual.sh` and can be used for manual API testing
- All Python unit tests are in `apps/users/tests.py`
- Tests use Django's built-in testing framework with DRF's APITestCase
- JWT authentication is properly mocked in tests using RefreshToken
- Tests include model validation, API endpoints, serializers, and integration scenarios

# Create folder in parent directories
:!mkdir -p %:h


   1. gg - Go to the first character of the file.
   2. v - Enter Visual mode.
   3. G - Go to the end of the file.

