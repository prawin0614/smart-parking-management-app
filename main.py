import os

from server import create_server


def main():
    port = int(os.environ.get("PORT", "8000"))
    host = "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"
    server = create_server(host, port)

    print(f"Smart Parking Management System running on http://{host}:{port}")

    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()