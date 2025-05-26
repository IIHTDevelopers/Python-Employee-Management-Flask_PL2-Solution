import unittest
from app import app, get_db_connection
from tests.TestUtils import TestUtils
from bs4 import BeautifulSoup

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.test_obj = TestUtils()

    def test_get_db_connection(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            result = isinstance(tables, list)
            conn.close()
            self.test_obj.yakshaAssert("TestDBConnection", result, "functional")
            print("TestDBConnection = Passed" if result else "TestDBConnection = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestDBConnection", False, "functional")
            print(f"TestDBConnection = Failed | Exception: {e}")

    def test_index_route(self):
        try:
            response = self.client.get('/')
            result = response.status_code == 200 and b'Welcome' in response.data
            self.test_obj.yakshaAssert("TestIndexRoute", result, "functional")
            print("TestIndexRoute = Passed" if result else "TestIndexRoute = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestIndexRoute", False, "functional")
            print(f"TestIndexRoute = Failed | Exception: {e}")

    def test_register_user_logic(self):
        try:
            test_data = {'username': 'admin', 'password': 'admin123'}
            response = self.client.post('/register', data=test_data, follow_redirects=True)
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                                ('admin', 'admin123')).fetchone()
            conn.close()
            result = (response.status_code == 200 and b'Login' in response.data and user is not None)
            self.test_obj.yakshaAssert("TestRegisterUserLogic", result, "functional")
            print("TestRegisterUserLogic = Passed" if result else "TestRegisterUserLogic = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestRegisterUserLogic", False, "functional")
            print(f"TestRegisterUserLogic = Failed | Exception: {e}")

    def test_login_user_logic(self):
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'admin123'))
            conn.commit()
            conn.close()
            response = self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
            result = response.status_code == 200 and b'Dashboard' in response.data
            self.test_obj.yakshaAssert("TestLoginUserLogic", result, "functional")
            print("TestLoginUserLogic = Passed" if result else "TestLoginUserLogic = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestLoginUserLogic", False, "functional")
            print(f"TestLoginUserLogic = Failed | Exception: {e}")

    def test_dashboard_displays_minimum_employees(self):
        try:
            self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})
            response = self.client.get('/dashboard', follow_redirects=True)
            soup = BeautifulSoup(response.data, 'html.parser')
            rows = soup.find_all('tr')
            result = len(rows) >= 4
            self.test_obj.yakshaAssert("TestDashboardMinimumEmployees", result, "functional")
            print("TestDashboardMinimumEmployees = Passed" if result else "TestDashboardMinimumEmployees = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestDashboardMinimumEmployees", False, "functional")
            print(f"TestDashboardMinimumEmployees = Failed | Exception: {e}")

    def test_check_employee_jhon_exists(self):
        try:
            conn = get_db_connection()
            emp = conn.execute('SELECT * FROM employees WHERE name=? AND salary=? AND address=?',
                               ('Jhon', '56000', '24 King Ave, Dubai')).fetchone()
            conn.close()
            result = emp is not None
            self.test_obj.yakshaAssert("TestCheckEmployeeJhon", result, "functional")
            print("TestCheckEmployeeJhon = Passed" if result else "TestCheckEmployeeJhon = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestCheckEmployeeJhon", False, "functional")
            print(f"TestCheckEmployeeJhon = Failed | Exception: {e}")

    def test_check_employee_raj_patel_age_58(self):
        try:
            conn = get_db_connection()
            emp = conn.execute(
                "SELECT * FROM employees WHERE name=? AND age=? AND salary=? AND address=?",
                ("Raj Patel", 58, 62000, "67 Queen St, Toronto")
            ).fetchone()
            conn.close()
            result = emp is not None
            self.test_obj.yakshaAssert("TestCheckEmployeeRajPatelAge58", result, "functional")
            print("TestCheckEmployeeRajPatelAge58 = Passed" if result else "TestCheckEmployeeRajPatelAge58 = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestCheckEmployeeRajPatelAge58", False, "functional")
            print(f"TestCheckEmployeeRajPatelAge58 = Failed | Exception: {e}")

    def test_check_alice_watson_exists(self):
        try:
            test_data = {
                'name': 'Alice Watson',
                'salary': '72000',
                'address': '55 Sunset Blvd, LA'
            }

            conn = get_db_connection()
            emp = conn.execute(
                'SELECT * FROM employees WHERE name = ? AND salary = ? AND address = ?',
                (test_data['name'], test_data['salary'], test_data['address'])
            ).fetchone()
            conn.close()

            result = emp is not None

            self.test_obj.yakshaAssert("TestCheckAliceWatsonExists", result, "functional")
            print("TestCheckAliceWatsonExists = Passed" if result else "TestCheckAliceWatsonExists = Failed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestCheckAliceWatsonExists", False, "functional")
            print(f"TestCheckAliceWatsonExists = Failed | Exception: {e}")

    def test_get_all_employees_api(self):
        try:
            response = self.client.get('/employees')
            data = response.get_json()
            result = (
                response.status_code == 200 and
                data.get('status') == 'success' and
                isinstance(data.get('employees'), list) and
                len(data['employees']) >= 5
            )
            self.test_obj.yakshaAssert("TestGetAllEmployeesAPI", result, "functional")
            print("TestGetAllEmployeesAPI = Passed" if result else "TestGetAllEmployeesAPI = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestGetAllEmployeesAPI", False, "functional")
            print(f"TestGetAllEmployeesAPI = Failed | Exception: {e}")


# Run the tests
if __name__ == '__main__':
    unittest.main()
