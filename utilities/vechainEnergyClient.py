import os
import http.client


class vechainEnergyClient:
    async def start_session(self, session_id, state):
        conn = http.client.HTTPSConnection(os.getenv('VECHAIN_ENERGY_BASE_URL'))
        payload = "{\"state\": \"" + state + "\"}"
        headers = {'Content-Type': "application/json"}
        conn.request("POST", f"/session/{session_id}", payload, headers)
        res = conn.getresponse()

    async def get_session(self, session_id):
        conn = http.client.HTTPSConnection(os.getenv('VECHAIN_ENERGY_BASE_URL'))
        conn.request("GET", f"/session/{session_id}")
        res = conn.getresponse()
        data = res.read()
        return data.decode()

    async def get_user_info(self, token_type, access_token):
        conn = http.client.HTTPSConnection(os.getenv('VECHAIN_ENERGY_BASE_URL'))
        headers = {'authorization': f"{token_type} {access_token}"}
        conn.request("POST", f"/oauth2/userinfo", None, headers)
        response = conn.getresponse()
        return response.read().decode()
