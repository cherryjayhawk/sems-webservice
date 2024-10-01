# from fastapi import APIRouter
# from fastapi.encoders import jsonable_encoder
# # from lib.db import get_db_connection
# import pickle
# import warnings

# router = APIRouter()
# LABEL = ["jagung", "bawang merah"]

# @router.get("")
# async def sensors():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(f"SELECT tr_unit.unit_id as id, tr_unit.unit_name_idn as label, tr_unit.unit_symbol as symbol, tr_unit.area as area, area.name as area_name, tm_site.site_name as site_name, active, max_norm_value, min_norm_value FROM tr_unit JOIN area ON tr_unit.area=area.id JOIN tm_site ON tm_site.site_id=area.site_id WHERE tr_unit.area != ''")
#     records = cursor.fetchall()

#     cursor.close()
#     conn.close() 
#     return records

# @router.get("")
# async def get_sensor(id: str = None):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(f"SELECT unit_id as id, unit_name_idn as label, unit_symbol as symbol, tr_unit.area as area, area.name as area_name, active, max_norm_value, min_norm_value FROM tr_unit JOIN area ON tr_unit.area=area.id WHERE area != '' AND unit_id = '{id}'")
#     record = cursor.fetchone()

#     cursor.close()
#     conn.close() 

#     return record
    
# # @router.delete("")
# # def delete_sensor(token: Annotated[str, Depends(oauth2_scheme)], id: str = None):
# #     conn = get_db_connection()

# #     cursor = conn.cursor()

# #     cursor.execute(f"DELETE FROM tr_unit WHERE unit_id = '{id}'")
# #     conn.commit()

# #     cursor.close()
# #     conn.close()
# #     return {
# #         "message": "Berhasil menghapus perangkat"
# #     }