from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import sys
import os
sys.path.append(os.getcwd())  # Add this to import your app modules

# Import your database URL and Base metadata
from database import SQLALCHEMY_DATABASE_URL, Base  # Adjust import path as needed

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Override the sqlalchemy.url value with your app's URL dynamically
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Base metadata to enable Alembic's autogenerate feature
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()