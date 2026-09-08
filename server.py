import json
import mimetypes
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from slot_service import (
    add_slot,
    get_all_slots,
    update_slot_status,
    delete_slot
)

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"


class ParkingServer(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):

        response = json.dumps(data).encode()

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        self.wfile.write(response)

    def send_file(self, file_path):

        content = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

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

        request_path = urlparse(self.path).path

        if request_path == "/slots":

            try:
                slots = get_all_slots()

            except Exception as e:
                self.send_json(500, {
                    "message": str(e)
                })

                return

            self.send_json(200, slots)
            return

        static_path = {
            "/": "index.html",
            "/index.html": "index.html",
            "/style.css": "style.css",
            "/script.js": "script.js"
        }.get(request_path)

        if static_path:
            file_path = FRONTEND_DIR / static_path
            self.send_file(file_path)
            return

        else:

            self.send_json(404, {
                "message": "Endpoint not found"
            })

    # =========================
    # POST
    # =========================

    def do_POST(self):

        if urlparse(self.path).path == "/slots":

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

        request_path = urlparse(self.path).path

        if request_path.startswith("/slots/"):

            try:

                slot_id = int(
                    request_path.split("/")[-1]
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

        request_path = urlparse(self.path).path

        if request_path.startswith("/slots/"):

            try:

                slot_id = int(
                    request_path.split("/")[-1]
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


def create_server(host, port):
    return HTTPServer((host, port), ParkingServer)