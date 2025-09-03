from controllers.api_controller import ApiController


class PlaneController:
    def __init__(self, api: ApiController):
        self.api = api

    def get_all_planes(self):
        """Fetch all planes from API"""
        try:
            return self.api.get("planes")  # GET /planes
        except Exception as e:
            print(f"❌ Error fetching planes: {e}")
            return []
        
    def get_plane_by_id(self, plane_id):
        return self.api.get(f"planes/{plane_id}")

    def add_plane(self, data):
        """Add a new plane to the API"""
        try:
            return self.api.post("planes", data)  # POST /planes
        except Exception as e:
            print(f"❌ Error adding plane: {e}")
            return None

    def update_plane(self, plane_id, data):
        """Update an existing plane"""
        try:
            return self.api.put(f"planes/{plane_id}", data)  # PUT /planes/{id}
        except Exception as e:
            print(f"❌ Error updating plane {plane_id}: {e}")
            return None

    def delete_plane(self, plane_id):
        """Delete a plane from the API"""
        try:
            self.api.delete(f"planes/{plane_id}")  # DELETE /planes/{id}
            return True
        except Exception as e:
            print(f"❌ Error deleting plane {plane_id}: {e}")
            return False
