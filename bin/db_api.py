from operator import itemgetter
import asyncio
import sqlite3
from contextlib import asynccontextmanager
from contextlib import AsyncContextDecorator
from datetime import datetime

class anime_db(AsyncContextDecorator):
    
    def __init__(self):
        self.connection = sqlite3.connect('anime.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Anime (
        year INTEGER,
        name TEXT NOT NULL PRIMARY KEY,
        png TEXT NOT NULL,
        raiting TEXT NOT NULL,
        url TEXT NOT NULL,
        trailer TEXT,
        genre TEXT,
        description TEXT,
        series TEXT,
        fullDescription TEXT
        )
        ''')
        self.connection.commit()
    
    async def __aenter__(self):
        print('init')
        return self 
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print('close')
        self.connection.close()
    
    async def search(self,type,value):
        if type =="Genre":
            self.cursor.execute('SELECT * FROM Anime WHERE genre LIKE ?', ['%' + value + '%'])
            return self.cursor.fetchall()
        if type =="Year":
            self.cursor.execute('SELECT * FROM Anime WHERE year =?', [value])
            return self.cursor.fetchall()
        if type =="Name":
            self.cursor.execute('SELECT * FROM Anime WHERE name =?', [value])
            return self.cursor.fetchall()
    
    async def update(self):
        #some func
        print("Еще не пашит ()")
 
    async def anime_on_year_set(self,data,year):
        self.cursor.execute('DELETE FROM Anime WHERE year=?',[year])
        for anime in data:
            self.cursor.execute('INSERT INTO Anime (year, name, png, raiting, url, genre,description) VALUES (?,?,?,?,?,?,?)', (year,anime[0],anime[2],anime[3],anime[1],anime[5],anime[4] ))
            self.connection.commit()

class stats_db(AsyncContextDecorator):
    
    def __init__ (self):
        self.connection = sqlite3.connect('statistic.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nick TEXT NOT NULL,
        user_id TEXT NOT NULL,
        channel_id TEXT NOT NULL,
        server_id INTEGER NOT NULL,
        time_join DATETIME NOT NULL,
        time_leave DATETIME
        )
        ''')
        self.connection.commit()
    
    async def __aenter__(self):
        print("Инициализация")
        return(self)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Выход")
        self.connection.close()
    
    async def on_join(self,server,channel,member):
        if not member.nick:
            self.cursor.execute('INSERT INTO stats (nick,user_id, channel_id, server_id, time_join) VALUES (?,?,?,?,?)', (member.name,member.id,channel.id,server.id,datetime.now().replace(microsecond=0)))
        else:
            self.cursor.execute('INSERT INTO stats (nick,user_id, channel_id, server_id, time_join) VALUES (?,?,?,?,?)', (member.nick,member.id,channel.id,server.id,datetime.now().replace(microsecond=0)))
        self.connection.commit()
    
    async def on_leave(self,member):
        self.cursor.execute('UPDATE stats SET time_leave = ? WHERE id = (SELECT id FROM stats WHERE user_id = ? ORDER BY id DESC LIMIT 1)', (datetime.now().replace(microsecond=0),member.id))
        self.connection.commit()
    
    async def clean_emptys(self):
        self.cursor.execute('DELETE FROM stats WHERE time_leave IS NULL')
        self.connection.commit()
    
    async def get_stats(self,user_id, server_id):
        self.cursor.execute('SELECT time_join,time_leave FROM stats WHERE user_id=? AND server_id =?',[user_id,server_id])
        return self.cursor.fetchall()