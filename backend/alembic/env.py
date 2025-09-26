from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import models  # noqa

config = context.config
fileConfig(config.config_file_name)
target_metadata = models.Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url") or os.getenv("DATABASE_URL")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = configuration.get("sqlalchemy.url") or os.getenv("DATABASE_URL")
    connectable = engine_from_config(configuration, prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()