# import pymysql # type: ignore
# from app.api import tunnel, startup_event
# from dotenv import dotenv_values

# config = dotenv_values(".env")

# def get_db_connection():
#     if tunnel is None or not tunnel.is_active:
#         startup_event()
#     return pymysql.connect(
#         host='127.0.0.1',
#         user=config["DB_USERNAME"],
#         passwd=config["DB_PASSWORD"],
#         db=config["DB_MAIN"],
#         port=tunnel.local_bind_port,
#         cursorclass=pymysql.cursors.DictCursor
#     )
