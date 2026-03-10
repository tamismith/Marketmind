"""Add content_type to generated_content

Revision ID: e5a1b9c2d4f6
Revises: c4d7e2a1f9b3
Create Date: 2026-03-10 20:10:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e5a1b9c2d4f6"
down_revision = "c4d7e2a1f9b3"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "generated_content",
        sa.Column("content_type", sa.String(length=20), nullable=False, server_default="text"),
    )
    op.alter_column("generated_content", "content_type", server_default=None)


def downgrade():
    op.drop_column("generated_content", "content_type")
