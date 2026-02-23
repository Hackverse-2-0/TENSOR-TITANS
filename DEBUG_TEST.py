"""
PDS Leak Detection Platform - Comprehensive Debug & Testing Suite
Tests all API endpoints, database operations, and ML models
"""

import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DebugTester:
    def __init__(self, base_url='http://localhost:5000/api/v1'):
        self.base_url = base_url
        self.token = None
        self.admin_token = None
        self.test_results = []
        self.user_id = None
        self.admin_id = None
        self.shop_id = None
        
    def print_header(self, text):
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}{Colors.ENDC}\n")
    
    def print_test(self, test_name, status, message=""):
        """Print test result"""
        status_text = f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}" if status else f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"
        print(f"  [{status_text}] {test_name}")
        if message:
            print(f"      {Colors.WARNING}→ {message}{Colors.ENDC}")
        self.test_results.append((test_name, status))
    
    def test_health_check(self):
        """Test API health check endpoint"""
        self.print_header("TEST 1: Health Check")
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.print_test("Health endpoint accessible", True, f"Status: {data.get('status')}")
                return True
            else:
                self.print_test("Health endpoint accessible", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Health endpoint accessible", False, str(e))
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        self.print_header("TEST 2: User Registration")
        try:
            # Test with valid data
            reg_data = {
                "username": f"testuser_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com",
                "password": "TestPassword123!",
                "role": "admin"
            }
            
            response = requests.post(f"{self.base_url}/auth/register", json=reg_data)
            
            if response.status_code == 201:
                data = response.json()
                # store user details for login
                self.admin_id = data.get('user', {}).get('id') or data.get('user_id')
                self.last_reg_username = reg_data['username']
                self.last_reg_password = reg_data['password']
                self.print_test("User registration successful", True, f"User ID: {self.admin_id}")
                return True
            elif response.status_code == 400:
                error_msg = response.json().get('error', '')
                self.print_test("User registration validation", "duplicate" not in error_msg.lower(), error_msg)
                return False
            else:
                self.print_test("User registration successful", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("User registration successful", False, str(e))
            return False
    
    def test_user_login(self):
        """Test user login"""
        self.print_header("TEST 3: User Login & Authentication")
        try:
            # Prefer the username/password created during registration
            username = getattr(self, 'last_reg_username', None) or ("admin" if not self.admin_id else "admin")
            password = getattr(self, 'last_reg_password', None) or "AdminPass123!"
            login_data = {
                "username": username,
                "password": password
            }
            
            response = requests.post(f"{self.base_url}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                # support multiple token key names
                self.token = data.get('access_token') or data.get('accessToken') or data.get('token')
                self.user_id = data.get('user', {}).get('id') if data.get('user') else data.get('user_id')
                
                if self.token:
                    self.print_test("User login successful", True, f"Token acquired (length: {len(self.token)})")
                    return True
                else:
                    self.print_test("User login successful", False, "No token received")
                    return False
            else:
                self.print_test("User login successful", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_test("User login successful", False, str(e))
            return False
    
    def test_get_current_user(self):
        """Test getting current user"""
        self.print_header("TEST 4: Get Current User")
        if not self.token:
            self.print_test("Get current user", False, "No token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                user = data.get('user', {})
                self.print_test("Get current user successful", True, f"User: {user.get('username')}, Role: {user.get('role')}")
                return True
            else:
                # print response body for debugging
                self.print_test("Get current user successful", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_test("Get current user successful", False, str(e))
            return False
    
    def test_shop_creation(self):
        """Test shop creation"""
        self.print_header("TEST 5: Shop Management")
        if not self.token:
            self.print_test("Create shop", False, "No token available")
            return False
        
        try:
            shop_data = {
                "name": f"Test Shop {int(time.time())}",
                "address": "123 Test Street",
                "city": "Test City",
                "state": "Test State",
                "pincode": "123456",
                "contact_person": "John Doe",
                "contact_phone": "9876543210"
            }
            
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.base_url}/shops", json=shop_data, headers=headers)
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.shop_id = data.get('shop', {}).get('id') or data.get('id')
                self.print_test("Create shop successful", True, f"Shop ID: {self.shop_id}")
                return True
            else:
                self.print_test("Create shop successful", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.print_test("Create shop successful", False, str(e))
            return False
    
    def test_list_shops(self):
        """Test shop listing"""
        self.print_header("TEST 6: List Shops")
        if not self.token:
            self.print_test("List shops", False, "No token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/shops", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                shops = data.get('shops', [])
                count = len(shops)
                self.print_test("List shops successful", True, f"Found {count} shops")
                return True
            else:
                self.print_test("List shops successful", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("List shops successful", False, str(e))
            return False
    
    def test_data_ingestion(self):
        """Test data ingestion"""
        self.print_header("TEST 7: Data Ingestion")
        if not self.token or not self.shop_id:
            self.print_test("Data ingestion", False, "No token or shop_id available")
            return False
        
        try:
            # Test stock ingestion
            stock_data = {
                "items": [
                    {
                        "item_name": "Rice",
                        "quantity": 100,
                        "unit": "kg",
                        "date": datetime.now().isoformat()
                    },
                    {
                        "item_name": "Wheat",
                        "quantity": 50,
                        "unit": "kg",
                        "date": datetime.now().isoformat()
                    }
                ]
            }
            
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{self.base_url}/data/stock/{self.shop_id}",
                json=stock_data,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                self.print_test("Stock data ingestion", True, "Stock items saved")
                
                # Test biometric ingestion
                biometric_data = {
                    "logs": [
                        {
                            "employee_id": "EMP001",
                            "name": "Test Employee",
                            "check_in_time": datetime.now().isoformat(),
                            "check_out_time": datetime.now().isoformat()
                        }
                    ]
                }
                
                response = requests.post(
                    f"{self.base_url}/data/biometric/{self.shop_id}",
                    json=biometric_data,
                    headers=headers
                )
                
                if response.status_code in [200, 201]:
                    self.print_test("Biometric data ingestion", True, "Biometric logs saved")
                    return True
                else:
                    self.print_test("Biometric data ingestion", False, f"Status: {response.status_code}")
                    return False
            else:
                self.print_test("Stock data ingestion", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Data ingestion", False, str(e))
            return False
    
    def test_anomaly_detection(self):
        """Test anomaly detection"""
        self.print_header("TEST 8: Anomaly Detection")
        if not self.token or not self.shop_id:
            self.print_test("Anomaly detection", False, "No token or shop_id available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{self.base_url}/anomalies/detect/{self.shop_id}",
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                anomalies = data.get('anomalies', [])
                self.print_test("Anomaly detection", True, f"Detected {len(anomalies)} anomalies")
                return True
            else:
                self.print_test("Anomaly detection", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Anomaly detection", False, str(e))
            return False
    
    def test_error_handling(self):
        """Test error handling"""
        self.print_header("TEST 9: Error Handling")
        
        try:
            # Test invalid endpoint
            response = requests.get(f"{self.base_url}/invalid-endpoint")
            self.print_test("404 error handling", response.status_code == 404, f"Status: {response.status_code}")
            
            # Test unauthorized access
            response = requests.get(f"{self.base_url}/auth/me")
            self.print_test("401 unauthorized handling", response.status_code == 401, f"Status: {response.status_code}")
            
            # Test invalid JSON
            response = requests.post(
                f"{self.base_url}/auth/login",
                headers={"Content-Type": "application/json"},
                data="invalid json"
            )
            self.print_test("400 bad request handling", response.status_code == 400, f"Status: {response.status_code}")
            
            return True
        except Exception as e:
            self.print_test("Error handling", False, str(e))
            return False
    
    def test_cors_headers(self):
        """Test CORS headers"""
        self.print_header("TEST 10: CORS Headers")
        try:
            response = requests.get(f"{self.base_url}/health")
            cors_headers = ['Access-Control-Allow-Origin', 'Access-Control-Allow-Methods']
            
            has_cors = any(header in response.headers for header in cors_headers)
            self.print_test("CORS headers present", has_cors, f"Headers: {list(response.headers.keys())[:5]}...")
            return has_cors
        except Exception as e:
            self.print_test("CORS headers", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}")
        print("╔════════════════════════════════════════════════════════╗")
        print("║  PDS LEAK DETECTION PLATFORM - DEBUG TEST SUITE        ║")
        print("║  Version 1.0.0                                         ║")
        print(f"║  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                            ║")
        print("╚════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        
        # Run tests in sequence
        self.test_health_check()
        self.test_user_registration()
        self.test_user_login()
        self.test_get_current_user()
        self.test_shop_creation()
        self.test_list_shops()
        self.test_data_ingestion()
        self.test_anomaly_detection()
        self.test_error_handling()
        self.test_cors_headers()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("TEST SUMMARY")
        
        passed = sum(1 for _, status in self.test_results if status)
        total = len(self.test_results)
        percentage = (passed / total * 100) if total > 0 else 0
        
        print(f"  Total Tests: {total}")
        print(f"  {Colors.OKGREEN}Passed: {passed}{Colors.ENDC}")
        print(f"  {Colors.FAIL}Failed: {total - passed}{Colors.ENDC}")
        print(f"  Success Rate: {percentage:.1f}%\n")
        
        if percentage == 100:
            print(f"  {Colors.OKGREEN}{Colors.BOLD}✓ All tests passed!{Colors.ENDC}\n")
        elif percentage >= 80:
            print(f"  {Colors.WARNING}⚠ Most tests passed, some issues found.{Colors.ENDC}\n")
        else:
            print(f"  {Colors.FAIL}✗ Multiple test failures detected.{Colors.ENDC}\n")

if __name__ == '__main__':
    tester = DebugTester()
    tester.run_all_tests()
