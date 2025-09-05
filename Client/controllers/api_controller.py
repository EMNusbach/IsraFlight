
import requests
from config import API_BASE_URL

class ApiController:
    def __init__(self, base_url=None):
        self.base_url = base_url or API_BASE_URL
        self.session = requests.Session()

    def _url(self, path):
        if path.startswith("/"):
            path = path[1:]
        return f"{self.base_url}/{path}"

    def get(self, path, params=None):
        resp = self.session.get(self._url(path), params=params, timeout=20)
        resp.raise_for_status()
        return resp.json()

    def post(self, path, json=None, data=None, files=None):
        try:
            resp = self.session.post(self._url(path), json=json, data=data, files=files, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            try:
                # Try to parse JSON from the error response
                error_data = resp.json()
            except Exception:
                error_data = {"message": str(e), "content": resp.text}
            import json
            raise Exception(json.dumps(error_data))


    def put(self, path, json=None):
        resp = self.session.put(self._url(path), json=json, timeout=20)
        resp.raise_for_status()
        if resp.status_code == 204 or not resp.content.strip():
            return True
        return resp.json()

    def delete(self, path):
        resp = self.session.delete(self._url(path), timeout=20)
        resp.raise_for_status()
        return resp.status_code == 204
