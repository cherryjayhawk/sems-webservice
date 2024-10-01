# from sshtunnel import SSHTunnelForwarder # type: ignore
# from dotenv import dotenv_values

# config = dotenv_values(".env")

# # Global variable to hold the SSH tunnel
# tunnel = None

# def start_tunnel():
#     global tunnel
#     if tunnel is None:
#         tunnel = SSHTunnelForwarder(
#             (config["SSH_HOSTNAME"], int(config["SSH_PORT"])),
#             ssh_username=config["SSH_USERNAME"],
#             ssh_password=config["SSH_PASSWORD"],
#             remote_bind_address=(config["DB_HOSTNAME"], int(config["DB_PORT"])),
#             local_bind_address=('127.0.0.1', 3307),
#             allow_agent=False,
#             host_pkey_directories='/tmp'
#         )
#         tunnel.start()
#         print("SSH tunnel started")

# def stop_tunnel():
#     global tunnel
#     if tunnel is not None:
#         tunnel.stop()
#         tunnel = None
#         print("SSH tunnel stopped")
