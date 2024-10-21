# alembic/env.py
from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context

from app.models import Base  # Import your models here

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py, can be acquired:
# ... etc.


def get_url():
    return os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
