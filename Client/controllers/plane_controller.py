from controllers.api_controller import ApiController


class PlaneController:
    def __init__(self, api: ApiController):
        self.api = api

    def get_all_planes(self):
        return self.api.get("planes")  # GET /planes

        
    def get_plane_by_id(self, plane_id):
        return self.api.get(f"planes/{plane_id}")

    def add_plane(self, data):
        try:
            response = self.api.post("planes", data)  # POST /planes
            return {"success": True, "data": response}
        except Exception as e:
            if hasattr(e, 'response') and e.response is not None:
                return {"success": False,  "error": e.response.text}
            return {"success": False, "error": str(e)}

    def update_plane(self, plane_id, data):
        try:
            response = self.api.put(f"planes/{plane_id}", data)  # PUT /planes/{id}
            return {"success": True, "data": response}
        except Exception as e:
            if hasattr(e, 'response') and e.response is not None:
                return {"success": False,  "error": e.response.text}
            return {"success": False, "error": str(e)}

    def delete_plane(self, plane_id):
        self.api.delete(f"planes/{plane_id}")  # DELETE /planes/{id}
        return True