"""Add BrandMemory model

Revision ID: b3f2c1d9e8a1
Revises: a7401fbd1541
Create Date: 2026-02-24 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b3f2c1d9e8a1"
down_revision = "a7401fbd1541"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "brand_memory",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("preferred_tone", sa.String(length=80), nullable=True),
        sa.Column("preferred_platform", sa.String(length=80), nullable=True),
        sa.Column("preferred_region", sa.String(length=80), nullable=True),
        sa.Column("style_notes", sa.Text(), nullable=True),
        sa.Column("cta_preferences", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade():
    op.drop_table("brand_memory")
