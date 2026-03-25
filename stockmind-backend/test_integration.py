#!/usr/bin/env python3
"""
Integration test script for StockMind Backend
Tests all auth and simulation endpoints with real data
"""

import asyncio
import httpx
import json
from typing import Optional

BASE_URL = "http://localhost:8000/api"

class APITester:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_id: Optional[str] = None

    async def test_auth_flow(self):
        """Test complete authentication flow"""
        print("\n" + "="*60)
        print("TESTING AUTHENTICATION FLOW")
        print("="*60)

        # 1. Register new user
        print("\n[1] Testing User Registration...")
        reg_data = {
            "email": f"test_user_{int(asyncio.get_event_loop().time())}@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/register",
                json=reg_data
            )
            assert response.status_code == 200, f"Registration failed: {response.text}"
            result = response.json()
            self.access_token = result["access_token"]
            self.refresh_token = result["refresh_token"]
            print(f"✓ User registered successfully")
            print(f"  Access Token: {self.access_token[:20]}...")
            print(f"  Refresh Token: {self.refresh_token[:20]}...")
        except Exception as e:
            print(f"✗ Registration failed: {e}")
            return False

        # 2. Get current user
        print("\n[2] Testing Get Current User...")
        try:
            response = await self.client.get(
                f"{BASE_URL}/auth/me",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            assert response.status_code == 200, f"Get user failed: {response.text}"
            user = response.json()
            self.user_id = user["id"]
            print(f"✓ Current user fetched successfully")
            print(f"  ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  Name: {user.get('full_name')}")
        except Exception as e:
            print(f"✗ Get current user failed: {e}")
            return False

        # 3. Test token refresh
        print("\n[3] Testing Token Refresh...")
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/refresh",
                json={"refresh_token": self.refresh_token}
            )
            assert response.status_code == 200, f"Refresh failed: {response.text}"
            result = response.json()
            self.access_token = result["access_token"]
            print(f"✓ Token refreshed successfully")
            print(f"  New Access Token: {self.access_token[:20]}...")
        except Exception as e:
            print(f"✗ Token refresh failed: {e}")
            return False

        # 4. Test logout
        print("\n[4] Testing Logout...")
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/logout",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            assert response.status_code == 200, f"Logout failed: {response.text}"
            print(f"✓ User logged out successfully")
            self.access_token = None
        except Exception as e:
            print(f"✗ Logout failed: {e}")
            return False

        return True

    async def test_simulation_flow(self):
        """Test simulation endpoints with real data"""
        print("\n" + "="*60)
        print("TESTING SIMULATION FLOW")
        print("="*60)

        # Re-login for simulation tests
        print("\n[0] Re-authenticating for simulation tests...")
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": "test@example.com",
                    "password": "demo123456"
                }
            )
            if response.status_code == 200:
                result = response.json()
                self.access_token = result["access_token"]
                print(f"✓ Re-authenticated successfully")
            else:
                print(f"⚠ Could not re-auth, using previous token")
        except Exception as e:
            print(f"⚠ Re-auth failed: {e}")

        # 1. Start simulation
        print("\n[1] Testing Start Simulation...")
        sim_data = {
            "ticker": "AAPL",
            "num_agents": 50,
            "agent_types": {
                "hedge_fund": 10,
                "retail": 25,
                "news": 5,
                "regulator": 3,
                "market_maker": 7
            },
            "time_horizon": "1d"
        }
        
        simulation_id = None
        try:
            response = await self.client.post(
                f"{BASE_URL}/simulation/start",
                json=sim_data,
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            assert response.status_code == 200, f"Start simulation failed: {response.text}"
            result = response.json()
            simulation_id = result["simulation_id"]
            print(f"✓ Simulation started successfully")
            print(f"  Simulation ID: {simulation_id}")
            print(f"  Ticker: {result['ticker']}")
            print(f"  Initial Price: ${result['current_price']:.2f}")
        except Exception as e:
            print(f"✗ Start simulation failed: {e}")
            return False

        # 2. Get simulation status
        print("\n[2] Testing Get Simulation Status...")
        try:
            response = await self.client.get(
                f"{BASE_URL}/simulation/status/{simulation_id}",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            assert response.status_code == 200, f"Get status failed: {response.text}"
            status = response.json()
            print(f"✓ Simulation status retrieved")
            print(f"  Status: {status['status']}")
            print(f"  Current Price: ${status['current_price']:.2f}")
            print(f"  Current Tick: {status['current_tick']}/{status['total_ticks']}")
            print(f"  Sentiment - Bullish: {status['sentiment']['bullish']}%, " +
                  f"Bearish: {status['sentiment']['bearish']}%, " +
                  f"Neutral: {status['sentiment']['neutral']}%")
        except Exception as e:
            print(f"✗ Get status failed: {e}")
            return False

        # 3. Get agents list
        print("\n[3] Testing Get Agents List...")
        try:
            response = await self.client.get(
                f"{BASE_URL}/agents?simulation_id={simulation_id}",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            assert response.status_code == 200, f"Get agents failed: {response.text}"
            agents = response.json()
            print(f"✓ Agents retrieved successfully")
            print(f"  Total Agents: {len(agents)}")
            if agents:
                print(f"  Sample Agent: {agents[0]['agent_id']}")
                print(f"    Type: {agents[0]['agent_type']}")
                print(f"    Sentiment: {agents[0]['sentiment']}")
        except Exception as e:
            print(f"✗ Get agents failed: {e}")
            return False

        # 4. Get news feed
        print("\n[4] Testing Get News Feed...")
        try:
            response = await self.client.get(
                f"{BASE_URL}/news?ticker=AAPL&limit=5",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            assert response.status_code == 200, f"Get news failed: {response.text}"
            news = response.json()
            print(f"✓ News feed retrieved successfully")
            print(f"  Total News Items: {len(news)}")
            if news:
                print(f"  Sample News: {news[0]['title'][:50]}...")
                print(f"    Sentiment: {news[0]['sentiment']}")
        except Exception as e:
            print(f"✗ Get news failed: {e}")
            return False

        return True

    async def run_all_tests(self):
        """Run all integration tests"""
        print("\n")
        print("╔" + "="*58 + "╗")
        print("║" + " "*10 + "StockMind Backend Integration Tests" + " "*14 + "║")
        print("╚" + "="*58 + "╝")

        auth_ok = await self.test_auth_flow()
        sim_ok = await self.test_simulation_flow()

        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Authentication Flow: {'✓ PASSED' if auth_ok else '✗ FAILED'}")
        print(f"Simulation Flow: {'✓ PASSED' if sim_ok else '✗ FAILED'}")
        print("="*60)

        await self.client.aclose()

        return auth_ok and sim_ok


async def main():
    """Main test runner"""
    tester = APITester()
    success = await tester.run_all_tests()
    exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
