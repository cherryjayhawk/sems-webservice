from datetime import datetime, timedelta
from typing import Annotated, Union
from sshtunnel import SSHTunnelForwarder
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
# from jwt.exceptions import InvalidTokenError
# from passlib.context import CryptContext
from pydantic import BaseModel
# import jwt
import pymysql
from dotenv import dotenv_values

from lib.data import realtime, realtime_AREA001, realtime_AREA002, realtime_AREA003

config = dotenv_values(".env")

app = FastAPI()

origins = [
    "*", 
]

# app.include_router(sensors.router, tags=["Sensor"], prefix="/sensors")
# app.include_router(areas.router, tags=["Area"], prefix="/areas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)                      

current_date = ((datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
start_date = ((datetime.now()).strftime("%Y-%m-%d"))

# Set-ExecutionPolicy Unrestricted -Scope Process
# venv/Scripts/activate

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "5299046ce9c9d18d8ea25d31c2b29aac884df89ba6050decff662becbe869d57"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    password: Union[str, None] = None
    email: Union[str, None] = None
    phone: Union[str, None] = None
    sts: Union[str, None] = None
    role_id: Union[int, None] = None

class UserInDB(User):
    hashed_password: str


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def authenticate_user(db, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

tunnel = None

@app.on_event("startup")
def startup_event():
    global tunnel
    if tunnel is None:
        tunnel = SSHTunnelForwarder(
            (config["SSH_HOSTNAME"], int(config["SSH_PORT"])),
            ssh_username=config["SSH_USERNAME"],
            ssh_password=config["SSH_PASSWORD"],
            remote_bind_address=(config["DB_HOSTNAME"], int(config["DB_PORT"])),
            local_bind_address=('127.0.0.1', 3307),
            allow_agent=False,
            host_pkey_directories='/tmp'
        )
        tunnel.start()
        print("SSH tunnel started")

@app.on_event("shutdown")
def shutdown_event():
    global tunnel
    if tunnel is not None:
        tunnel.stop()
        tunnel = None
        print("SSH tunnel stopped")

def get_db_connection():
    if tunnel is None or not tunnel.is_active:
        startup_event()
    return pymysql.connect(
        host='127.0.0.1',
        user=config["DB_USERNAME"],
        passwd=config["DB_PASSWORD"],
        db=config["DB_MAIN"],
        port=tunnel.local_bind_port,
        cursorclass=pymysql.cursors.DictCursor
    )

# async def get_current_user():
#         conn = get_db_connection()
#         cursor = conn.cursor() 
#         cursor.execute(f"SELECT * FROM tm_user")
#         records = cursor.fetchall()
#         users = {}

#         for item in records:
#             item["username"] = item["user_name"]
#             item["hashed_password"] = item["user_pass"]
#             item["email"] = item["user_email"]
#             item["phone"] = item["user_phone"]
#             del item["user_name"]
#             del item["user_pass"]
#             users[item["username"]] = item

#         credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             username: str = payload.get("sub")
#             if username is None:
#                 raise credentials_exception
#             token_data = TokenData(username=username)
#         except InvalidTokenError:
#             raise credentials_exception
#         user = get_user(users, username=token_data.username)
#         if user is None:
#             raise credentials_exception
#         return user


# async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):

#     # if current_user.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

@app.get("/")
async def home():
    return RedirectResponse("/docs")

@app.post("/api/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        # conn = get_db_connection()
        # cursor = conn.cursor() 
        # cursor.execute(f"SELECT * FROM tm_user")
        # records = cursor.fetchall()
        # users = {}

        # for item in records:
        #     item["username"] = item["user_name"]
        #     item["hashed_password"] = item["user_pass"]
        #     del item["user_name"]
        #     del item["user_pass"]
        #     users[item["username"]] = item

        # user = authenticate_user(users, form_data.username, form_data.password)
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Incorrect username or password",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )
        # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # access_token = create_access_token(
        #     data={"sub": user.username}, expires_delta=access_token_expires
        # )
        return {"access_token": "undefined", "token_type": "bearer"}

# @app.get("/users/me", response_model=User)
# async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):

#     return current_user

# @app.get("/users")
# def get_all_users():
#         conn = get_db_connection()
#         cursor = conn.cursor() 

#         cursor.execute(f"SELECT * FROM tm_user")
#         users = cursor.fetchall()

#         cursor.close()
#         conn.close()
#         return users

# @app.get("/users/me/items/")
# async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):

#     return [{"item_id": "Foo", "owner": current_user.username}]


# @app.post("/api/register")
# async def register_user(data: User):
#         conn = get_db_connection()
#         cursor = conn.cursor() 

#         cursor.execute(f"SELECT user_name, user_pass FROM tm_user")
#         records = cursor.fetchall()
#         users = {}

#         for item in records:
#             item["username"] = item["user_name"]
#             item["hashed_password"] = item["user_pass"]
#             del item["user_name"]
#             del item["user_pass"]
#             users[item["username"]] = item

#         # Check if the username is already taken
#         if data.username in users:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Username already registered",
#             )
        
#         # Hash the user's password
#         hashed_password = get_password_hash(data.password)

#         # Add the new user to the database
#         cursor.execute(f"INSERT INTO tm_user (user_id, user_name, user_pass, user_email, user_phone, user_sts, user_created, role_id, user_updated) VALUES ('2', '{data.username}', '{hashed_password}', '{data.email}', '{data.phone}', '{data.sts}', now(), {data.role_id}, now())")
#         conn.commit()

#         cursor.close()
#         conn.close()

@app.get("/api/update")
def read_update_data(area: Union[str, None] = None):
# def read_update_data( area: Union[str, None] = None): 

        if (area == None):
            return realtime
        elif (area == "AREA001"):
            return realtime_AREA001
        elif (area == "AREA002"):
            return realtime_AREA002
        elif (area == "AREA003"):
            return realtime_AREA003
        else:
            return []
    
@app.get("/api/reports")
async def read_update_data( start_date: str, end_date: str):
        conn = get_db_connection()
        cursor = conn.cursor() 

        cursor.execute(f"SELECT DATE_FORMAT(read_date, '%Y-%m-%d %H:%i:00') AS datetime, ds_id AS sensor_id, read_value AS value FROM tm_sensor_read WHERE read_date BETWEEN '{start_date}' AND '{end_date}' GROUP BY sensor_id, datetime ORDER BY datetime")
        records = cursor.fetchall()

        cursor.close()
        conn.close() 
        return records

@app.get("/api/history")
async def read_history_data( area: str, start_date: Union[str, None] = start_date, end_date: Union[str, None] = current_date):

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT tr_unit.unit_id as unit_id, tr_unit.unit_name_idn as unit_name FROM tr_unit JOIN area ON tr_unit.area=area.id WHERE tr_unit.active = '1' AND tr_unit.area = '{area}'")
        parameters = cursor.fetchall()

        params = []
        for param in parameters:
            params.append(param)

        records = {
                "read_date" : [],
                "sensor_data" : []
            }
        
        cursor.execute(f"SELECT (DATE_FORMAT(read_date, '%Y-%m-%d %H:00:00')) as datetime FROM tm_sensor_read WHERE read_date BETWEEN '{start_date}' AND '{end_date}' GROUP BY datetime")
        dates = cursor.fetchall()
        for date in dates:
            records["read_date"].append(str(date['datetime']))
    
        for param in params:
            value = []
            cursor.execute(f"SELECT (DATE_FORMAT(read_date, '%Y-%m-%d %H:00:00')) AS datetime, FORMAT(AVG(read_value), 2) as average_value FROM tm_sensor_read JOIN tr_unit ON tm_sensor_read.ds_id = tr_unit.unit_id WHERE read_date BETWEEN '{start_date}' AND '{end_date}' AND tm_sensor_read.ds_id = '{param['unit_id']}' GROUP BY datetime")
            read_values = cursor.fetchall()
            for read_value in read_values:
                value.append(read_value['average_value'])
            
            records["sensor_data"].append({"id": param['unit_id'], "label": param['unit_name'], "data": value})

        cursor.close()
        conn.close() 
        return records

@app.get("/api/overviews")
async def overviews():
    conn = get_db_connection()
    cursor = conn.cursor()

    # cursor.execute(f"SELECT COUNT(site_id) as site_count FROM tm_site")
    # site_count = cursor.fetchone()

    # cursor.execute(f"SELECT COUNT(dev_id) as device_count FROM tm_device")
    # device_count = cursor.fetchone()

    # cursor.execute(f"SELECT COUNT(ds_id) as sensor_count FROM td_device_sensor")
    # sensor_count = cursor.fetchone()

    cursor.execute(f"select read_date as last_update from tm_sensor_read ORDER BY read_date DESC limit 1")
    last_update = cursor.fetchone()

    cursor.close()
    conn.close() 
    return {"last_update": last_update["last_update"], "site_count": 1, "device_count": 1, "sensor_count": 23}

@app.get("/api/sites")
async def read_site( site_id: str = None):
        conn = get_db_connection()
        cursor = conn.cursor()

        data = None

        if (site_id == None):
            cursor.execute(f"SELECT * FROM tm_site")
            records = cursor.fetchall()
            data = [{'id': item["site_id"],
                    'name': item["site_name"],
                    'address': item["site_address"], 
                    'long': item["site_lon"], 
                    'lat': item["site_lat"], 
                    'elevasi': item["site_elevasi"],
                    'sts': item["site_sts"],
                    'created': item["site_created"],
                    'update': item["site_update"]} for item in records];
        else:
            cursor.execute(f"SELECT * FROM tm_site WHERE site_id = '{site_id}'")
            record = cursor.fetchone()
            data = {'id': record["site_id"],
                'name': record["site_name"],
                'address': record["site_address"], 
                'long': record["site_lon"], 
                'lat': record["site_lat"], 
                'elevasi': record["site_elevasi"],
                'sts': record["site_sts"],
                'created': record["site_created"],
                'update': record["site_update"]}
        
        cursor.close()
        conn.close() 
        return data

@app.get("/api/areas")
async def areas( site_id: str = None):
        conn = get_db_connection()
        cursor = conn.cursor()

        if (site_id != None):
            cursor.execute(f"SELECT area.id as id, area.name as area_name, area.site_id, tm_site.site_name as site_name, type FROM area JOIN tm_site ON area.site_id=tm_site.site_id WHERE area.site_id = '{site_id}'")
        else:
            cursor.execute(f"SELECT area.id as id, area.name as area_name, area.site_id, tm_site.site_name as site_name, type FROM area JOIN tm_site ON area.site_id=tm_site.site_id")

        records = cursor.fetchall()

        cursor.close()
        conn.close() 
        return records


class Area(BaseModel):
    id: str #unit_id
    name: str #area_name
    site_id: str #site_id
    type: str #type

@app.post("/api/areas")
async def add_area( area: Area):

        conn = get_db_connection()
        cursor = conn.cursor()

        if (area):
            cursor.execute(f"INSERT INTO area VALUES ('{area.id}', '{area.name}', '{area.site_id}', '{area.type}')")
            conn.commit()
        else:
            raise HTTPException(status_code=400, detail="Invalid area data")

        cursor.close()
        conn.close() 
        return {
            "message": "Berhasil mendaftarkan area baru"
        }
    
@app.put("/api/areas")
async def edit_area( area: Area, id: str):

        conn = get_db_connection()

        cursor = conn.cursor()
        if (area and id):
            cursor.execute(f"UPDATE area SET id = '{area.id}', name = '{area.name}', site_id = '{area.site_id}', type = '{area.type}' WHERE id = '{id}'")
            conn.commit()
        else:
            raise HTTPException(status_code=400, detail="Invalid area data")

        cursor.close()
        conn.close() 
        return {
            "message": "Berhasil mengubah informasi area"
        }

@app.get("/api/area")
async def area( area_id: str = None):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT area.id as id, name, site_id, type FROM area WHERE id = '{area_id}'")
        records = cursor.fetchone()

        cursor.close()
        conn.close() 
        return records
    
@app.get("/api/sensors")
async def sensors():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT tr_unit.unit_id as id, tr_unit.unit_name_idn as label, tr_unit.unit_symbol as symbol, tr_unit.area as area, area.name as area_name, tm_site.site_name as site_name, active, max_norm_value, min_norm_value FROM tr_unit JOIN area ON tr_unit.area=area.id JOIN tm_site ON tm_site.site_id=area.site_id WHERE tr_unit.area != ''")
        records = cursor.fetchall()

        cursor.close()
        conn.close() 
        return records

@app.get("/api/sensor")
async def get_sensor( id: str = None):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT unit_id as id, unit_name_idn as label, unit_symbol as symbol, tr_unit.area as area, area.name as area_name, active, max_norm_value, min_norm_value FROM tr_unit JOIN area ON tr_unit.area=area.id WHERE area != '' AND unit_id = '{id}'")
        record = cursor.fetchone()

        cursor.close()
        conn.close() 

        return record
    
@app.delete("/api/sensor")
async def delete_sensor( id: str = None):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"DELETE FROM tr_unit WHERE unit_id = '{id}'")
        conn.commit()

        cursor.close()
        conn.close()
        return {
            "message": "Berhasil menghapus perangkat"
        }

class Sensor(BaseModel):
    id: str #unit_id
    unit_name: Union[str, None] = '-' #unit_name
    label: str #unit_name_idn
    symbol: str #unit_symbol
    sts: int = 1 #unit_sts
    update: str = current_date #unit_update
    area: Union[str, int] #area
    active: int = 1 #active
    min_norm_value: Union[int, float, str] #min_norm_value
    max_norm_value: Union[int, float, str] #max_norm_value

@app.put("/api/sensors")
async def edit_sensor( sensor: Sensor, id: str):

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(f"UPDATE tr_unit SET unit_id = '{sensor.id}', unit_name_idn = '{sensor.label}', unit_symbol = '{sensor.symbol}', area = '{sensor.area}', active = '{sensor.active}', min_norm_value = '{sensor.min_norm_value}', max_norm_value = '{sensor.max_norm_value}'  WHERE unit_id = '{id}'")
        conn.commit()

        cursor.close()
        conn.close()
        return {
            "message": "Berhasil mengubah informasi perangkat"
        }

@app.post("/api/sensors")
async def add_sensor( sensor: Sensor):

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO tr_unit VALUES ('{sensor.id}', '{sensor.unit_name}', '{sensor.label}', '{sensor.symbol}', '{sensor.sts}', '{sensor.update}', '{sensor.area}', '{sensor.active}', '{sensor.min_norm_value}', '{sensor.max_norm_value}')")
        conn.commit()

        cursor.close()
        conn.close()
        return {
            "message": "Berhasil mendaftarkan perangkat baru"
        }
    
@app.get("/api/sensor/avg")
async def get_sensor(area: str = None, start_date: Union[str, None] = start_date, end_date: Union[str, None] = current_date):

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(f"SELECT tm_sensor_read.ds_id as id, FORMAT(AVG(read_value), 2) as average FROM tm_sensor_read JOIN tr_unit ON tm_sensor_read.ds_id=tr_unit.unit_id WHERE tr_unit.area='{area}' AND tm_sensor_read.read_date BETWEEN '{start_date}' AND '{end_date}' group by tm_sensor_read.ds_id")

        record = cursor.fetchall()

        cursor.close()
        conn.close() 

        return {
            f"{area}": record
        }