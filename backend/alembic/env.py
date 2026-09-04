from alembic.config import Config
from alembic import command

alembic_cfg = Config("alembic.ini")

def migrate():
    command.upgrade(alembic_cfg, "head")

def downgrade(revision="base"):
    command.downgrade(alembic_cfg, revision)

if __name__ == "__main__":
    migrate()
