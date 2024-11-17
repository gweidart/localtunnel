import argparse
import asyncio
import tracemalloc

from localtunnel._logging import logger
from localtunnel.tunnel_manager import TunnelManager


def parse_arguments():
    """
    Parse command-line arguments for the LocalTunnel CLI.
    """
    parser = argparse.ArgumentParser(
        description="LocalTunnel CLI for managing tunnels."
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
        "-m", "--monitor", action="store_true", help="Enable tunnel monitoring."
    )
    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        default="INFO",
        help="Set the log level (e.g., DEBUG, INFO, WARNING).",
    )
    return parser.parse_args()


async def async_main():
    """
    Main entry point for the LocalTunnel CLI.
    """
    args = parse_arguments()

    # Set logging level
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=args.log_level)

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
            logger.info("✨ Tunnel open at URL: {}", tunnel.get_tunnel_url())

        # Monitor the tunnel(s) if requested
        if args.monitor:
            logger.info("Monitoring tunnels...")
            await manager.monitor_all()
        else:
            await asyncio.Event().wait()  # Keep the CLI running

    except Exception as e:
        logger.error("An error occurred: {}", e)
    finally:
        logger.info("Closing tunnels...")
        await manager.close_all()


def main():
    """
    Entry point for the CLI.
    Parses arguments and runs the asynchronous logic.
    """
    # Run the asynchronous logic with parsed arguments
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
    tracemalloc.start()
