import argparse
import asyncio
import signal
import tracemalloc

from localtunnel._logging import logger
from localtunnel.tunnel_manager import TunnelManager

tracemalloc.start()

def parse_arguments():
    """
    Parse command-line arguments for the LocalTunnel CLI.
    """
    parser = argparse.ArgumentParser(
        description="LocalTunnel CLI for managing tunnels. https://github.com/gweidart/localtunnel-py"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        required=True,
        help="Local port to expose via the tunnel.",
    )
    parser.add_argument(
        "-s",
        "--subdomain",
        type=str,
        default=None,
        help="Optional subdomain for the tunnel. (e.g., https://subdomain.loca.lt",
    )
    parser.add_argument(
        "-t",
        "--host",
        type=str,
        default="https://localtunnel.me",
        help="LocalTunnel server host URL.",
    )
    parser.add_argument(
        "-m",
        "--monitor",
        action="store_true",
        help="Enable tunnel monitoring."
    )
    return parser.parse_args()

async def async_main(stop_event):
    """
    Main entry point for the LocalTunnel CLI.
    """
    args = parse_arguments()

    # Initialize TunnelManager
    manager = TunnelManager()

    # Add tunnel based on CLI input
    manager.add_tunnel(port=args.port, subdomain=args.subdomain, host=args.host)

    # Open the tunnel(s)
    try:
        logger.info("Opening tunnels...")
        await manager.open_all()

        # Display tunnel URLs
        for tunnel in manager.tunnels:
            logger.info(f"\u2728 Tunnel open at URL: {tunnel.get_tunnel_url()}")

        # Monitor the tunnel(s) if requested
        if args.monitor:
            logger.info("Monitoring tunnels...")
            await manager.monitor_all()
        else:
            await asyncio.wait_for(stop_event.wait(), timeout=3600)  # Keep the CLI running, with a timeout of 1 hour

    except asyncio.TimeoutError:
        logger.warning("Timeout reached, shutting down after 1 hour of inactivity.")
    except (ConnectionError, asyncio.CancelledError) as e:
        logger.error(f"A specific error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Closing tunnels...")
        await manager.close_all()

def main():
    """
    Entry point for the CLI.
    Parses arguments and runs the asynchronous logic.
    """
    stop_event = asyncio.Event()
    loop = asyncio.get_event_loop()

    # Signal handler to gracefully handle Ctrl+C
    def handle_signal():
        logger.info("\nReceived exit signal. Closing Tunnel gracefully...")
        stop_event.set()

    # Register the signal handler for SIGINT (Ctrl+C) using loop.add_signal_handler
    loop.add_signal_handler(signal.SIGINT, handle_signal)

    # Run the asynchronous logic with parsed arguments
    try:
        loop.run_until_complete(async_main(stop_event))
    except KeyboardInterrupt:
        logger.info("\nTunnel interrupted by user.")
    finally:
        logger.info("Tunnel closed.")
        loop.close()

if __name__ == "__main__":
    main()

