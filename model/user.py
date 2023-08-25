from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Float, DateTime
from config.db import meta, engine


users = Table("users", meta, 
            Column("id", Integer, primary_key=True),
            Column('name', String(255), nullable=False),
            Column('last_name', String(255), nullable=False),
            Column('login', String(255), nullable=False),
            Column('password', String(255), nullable=False),
            Column('status', String(30), nullable=False),
            Column('created_at', DateTime, nullable=False),
            Column('updated_at', DateTime, nullable=False),
        )

meta.create_all(bind=engine, tables=[users])