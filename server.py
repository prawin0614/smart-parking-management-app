import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from slot_service import (
    add_slot,
    get_all_slots,
    update_slot_status,
    delete_slot
)


class ParkingServer(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        response = json.dumps(data)
        self.wfile.write(response.encode())

    def do_OPTIONS(self):

        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def read_json(self):

        content_length = int(self.headers.get("Content-Length", 0))

        body = self.rfile.read(content_length)

        return json.loads(body)

    # =========================
    # GET
    # =========================

    def do_GET(self):

        if self.path == "/slots":

            try:
                slots = get_all_slots()

            except Exception as e:
                self.send_json(500, {
                    "message": str(e)
                })

                return

            self.send_json(200, slots)

        else:

            self.send_json(404, {
                "message": "Endpoint not found"
            })

    # =========================
    # POST
    # =========================

    def do_POST(self):

        if self.path == "/slots":

            try:

                data = self.read_json()

                slot_number = data["slot_number"]
                vehicle_type = data["vehicle_type"]

                result = add_slot(
                    slot_number,
                    vehicle_type
                )

                self.send_json(201, result)

            except Exception as e:

                self.send_json(400, {
                    "message": str(e)
                })

        else:

            self.send_json(404, {
                "message": "Endpoint not found"
            })

    # =========================
    # PUT
    # =========================

    def do_PUT(self):

        if self.path.startswith("/slots/"):

            try:

                slot_id = int(
                    self.path.split("/")[-1]
                )

                data = self.read_json()

                status = data["status"]

                if status not in ["AVAILABLE", "OCCUPIED"]:

                    self.send_json(400, {
                        "message": "Invalid status"
                    })

                    return

                result = update_slot_status(
                    slot_id,
                    status
                )

                status_code = 404 if result.get("message") == "Slot not found" else 200
                self.send_json(status_code, result)

            except Exception as e:

                self.send_json(400, {
                    "message": str(e)
                })

        else:

            self.send_json(404, {
                "message": "Endpoint not found"
            })

    # =========================
    # DELETE
    # =========================

    def do_DELETE(self):

        if self.path.startswith("/slots/"):

            try:

                slot_id = int(
                    self.path.split("/")[-1]
                )

                result = delete_slot(slot_id)

                status_code = 404 if result.get("message") == "Slot not found" else 200
                self.send_json(status_code, result)

            except Exception as e:

                self.send_json(400, {
                    "message": str(e)
                })

        else:

            self.send_json(404, {
                "message": "Endpoint not found"
            })


server = HTTPServer(
    ("127.0.0.1", 8000),
    ParkingServer
)

print("Parking server running on http://127.0.0.1:8000")

if __name__ == "__main__":
    server.serve_forever()