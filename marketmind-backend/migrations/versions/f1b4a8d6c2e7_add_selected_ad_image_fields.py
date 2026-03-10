"""Add selected ad image fields to generated_content

Revision ID: f1b4a8d6c2e7
Revises: e5a1b9c2d4f6
Create Date: 2026-03-10 21:05:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f1b4a8d6c2e7"
down_revision = "e5a1b9c2d4f6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("generated_content", sa.Column("selected_image_option_id", sa.String(length=40), nullable=True))
    op.add_column("generated_content", sa.Column("selected_image_base64", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("generated_content", "selected_image_base64")
    op.drop_column("generated_content", "selected_image_option_id")
