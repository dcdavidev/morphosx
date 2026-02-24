import uvicorn
import argparse

def main():
    parser = argparse.ArgumentParser(description="MorphosX Media Engine CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command: start
    start_parser = subparsers.add_parser("start", help="Start the MorphosX server")
    start_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    start_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    start_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()

    if args.command == "start":
        uvicorn.run("morphosx.app.main:app", host=args.host, port=args.port, reload=args.reload)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
