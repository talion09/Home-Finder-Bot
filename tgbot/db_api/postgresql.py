from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from tgbot.config import load_config

config = load_config(".env")


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            database=config.db.database,
            max_inactive_connection_lifetime=3
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):

        async with self.pool.acquire() as connection:
            connection: Connection()
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orientir_users (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE, 
        language VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    @staticmethod
    def format_args2(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=2)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, first_name, username, telegram_id, language):
        sql = "INSERT INTO Orientir_users (first_name, username, telegram_id, language) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, first_name, username, telegram_id, language, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Orientir_users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Orientir_users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_user(self, telegram_id, **kwargs):
        sql = "UPDATE Orientir_users SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, *parameters, execute=True)

    async def count_users(self):
        return await self.execute("SELECT COUNT(*) FROM Orientir_users;", fetchval=True, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Orientir_users", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orientir_admins (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE, 
        name VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_administrator(self, telegram_id, name):
        sql = "INSERT INTO Orientir_admins (telegram_id, name) VALUES ($1, $2) returning *"
        return await self.execute(sql, telegram_id, name, fetchrow=True)

    async def select_all_admins(self):
        sql = "SELECT * FROM Orientir_admins"
        return await self.execute(sql, fetch=True)

    async def select_id_admins(self):
        sql = "SELECT telegram_id FROM Orientir_admins"
        return await self.execute(sql, fetch=True)

    async def select_admin(self, **kwargs):
        sql = "SELECT * FROM Orientir_admins WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_admin(self, telegram_id):
        await self.execute("DELETE FROM Orientir_admins WHERE telegram_id=$1", telegram_id, execute=True)

    async def drop_admins(self):
        await self.execute("DROP TABLE Orientir_admins", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_flats(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orientir_flats (
        key_id SERIAL PRIMARY KEY,
        id BIGINT NOT NULL UNIQUE,
        catg_code INT NOT NULL,
        category VARCHAR(255) NOT NULL,
        type_code INT NOT NULL,
        type VARCHAR(255) NOT NULL,
        room_code INT NULL,
        room VARCHAR(255) NULL,
        room_uz VARCHAR(255) NULL,
        sub1_code INT NOT NULL,
        sub1category VARCHAR(255) NOT NULL,
        sub1category_uz VARCHAR(255) NOT NULL,
        sub2_code INT NOT NULL,
        sub2category VARCHAR(255) NOT NULL,
        sub2category_uz VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL,
        url_uz VARCHAR(255) NOT NULL,
        text VARCHAR(255) NOT NULL,
        text_uz VARCHAR(255) NOT NULL,
        descrip VARCHAR(255) NOT NULL,
        desc_uz VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_flat(self, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz,
                       sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz):
        sql = "INSERT INTO Orientir_flats (id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, " \
              "sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, " \
              "url, url_uz, text, text_uz, descrip, desc_uz) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, " \
              "$12, $13, $14, $15, $16, $17, $18, $19, $20) returning *"
        return await self.execute(sql, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz,
                                  sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz, fetchrow=True)

    async def drop_flats(self):
        await self.execute("DROP TABLE Orientir_flats", execute=True)

    async def select_in_types(self, catg_code, type_code):
        sql = "SELECT * FROM Orientir_flats WHERE catg_code=$1 AND type_code=$2"
        return await self.execute(sql, catg_code, type_code, fetch=True)

    async def select_in_rooms(self, catg_code, type_code, room_code):
        sql = "SELECT * FROM Orientir_flats WHERE catg_code=$1 AND type_code=$2 AND room_code=$3"
        return await self.execute(sql, catg_code, type_code, room_code, fetch=True)

    async def select_in_regions(self, catg_code, type_code, room_code, sub1_code):
        sql = "SELECT * FROM Orientir_flats WHERE catg_code=$1 AND type_code=$2 AND room_code=$3 AND sub1_code=$4"
        return await self.execute(sql, catg_code, type_code, room_code, sub1_code, fetch=True)

    async def select_quarter(self, catg_code, type_code, sub1_code):
        sql = "SELECT * FROM Orientir_flats WHERE catg_code=$1 AND type_code=$2 AND sub1_code=$3"
        return await self.execute(sql, catg_code, type_code, sub1_code, fetch=True)

    async def ids_in_flats_sub1(self, sub1_code, room_code, catg_code):
        sql = "SELECT * FROM Orientir_flats WHERE sub1_code=$1 AND room_code=$2 AND catg_code=$3"
        return await self.execute(sql, sub1_code, room_code, catg_code, fetch=True)

    async def ids_in_flats_sub2(self, sub2_code, room_code, catg_code):
        sql = "SELECT * FROM Orientir_flats WHERE sub2_code=$1 AND room_code=$2 AND catg_code=$3"
        return await self.execute(sql, sub2_code, room_code, catg_code, fetch=True)

    async def select_flat(self, **kwargs):
        sql = "SELECT * FROM Orientir_flats WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_flats(self, **kwargs):
        sql = "SELECT * FROM Orientir_flats WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_flat(self, id, **kwargs):
        sql = "UPDATE Orientir_flats SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE id=$1"
        return await self.execute(sql, id, *parameters, execute=True)

    async def delete_flat(self, id):
        await self.execute("DELETE FROM Orientir_flats WHERE id=$1", id, execute=True)

    async def select_room_code(self):
        sql = "SELECT room_code FROM Orientir_flats"
        return await self.execute(sql, fetch=True)

    async def select_sub1(self):
        sql = "SELECT sub1_code FROM Orientir_flats"
        return await self.execute(sql, fetch=True)

    async def select_sub2(self):
        sql = "SELECT sub2_code FROM Orientir_flats"
        return await self.execute(sql, fetch=True)

    async def select_all_flats(self):
        sql = "SELECT * FROM Orientir_flats"
        return await self.execute(sql, fetch=True)

    async def select_inline(self, room):
        sql = "SELECT * FROM Orientir_flats WHERE room ILIKE $1"
        return await self.execute(sql, room, fetch=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_cart(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orientir_cart (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL, 
        object_id INT NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_to_cart(self, telegram_id, object_id):
        sql = "INSERT INTO Orientir_cart (telegram_id, object_id) VALUES ($1, $2) returning *"
        return await self.execute(sql, telegram_id, object_id, fetchrow=True)

    async def select_all_objects(self, telegram_id):
        sql = "SELECT * FROM Orientir_cart WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetch=True)

    async def select_cart(self, **kwargs):
        sql = "SELECT * FROM Orientir_cart WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def drop_cart(self):
        await self.execute("DROP TABLE Orientir_cart", execute=True)

    async def delete_cart(self, telegram_id, object_id):
        await self.execute("DELETE FROM Orientir_cart WHERE telegram_id=$1 AND object_id=$2", telegram_id, object_id, execute=True)

    async def delete_whole_cart(self, telegram_id):
        await self.execute("DELETE FROM Orientir_cart WHERE telegram_id=$1", telegram_id, execute=True)

    async def count_cart(self, telegram_id):
        sql = "SELECT COUNT(*) FROM Orientir_cart WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchval=True, execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_groups(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orientir_groups (
        id SERIAL PRIMARY KEY,
        type_group VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        group_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, fetch=True)

    async def add_group(self, type_group, name, group_id):
        sql = "INSERT INTO Orientir_groups (type_group, name, group_id) VALUES ($1, $2, $3) returning *"
        return await self.execute(sql, type_group, name, group_id, fetchrow=True)

    async def select_all_groups(self):
        sql = "SELECT * FROM Orientir_groups"
        return await self.execute(sql, fetch=True)

    async def select_group(self, **kwargs):
        sql = "SELECT * FROM Orientir_groups WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_group(self, group_id):
        await self.execute("DELETE FROM Orientir_groups WHERE group_id=$1", group_id, execute=True)

    async def drop_groups(self):
        await self.execute("DROP TABLE Orientir_groups", execute=True)

