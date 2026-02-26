"""Extend GeneratedContent for A/B variants

Revision ID: c4d7e2a1f9b3
Revises: b3f2c1d9e8a1
Create Date: 2026-02-26 14:45:00.000000

"""
from alembic import op
import json
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c4d7e2a1f9b3"
down_revision = "b3f2c1d9e8a1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("generated_content", sa.Column("original_prompt", sa.Text(), nullable=True))
    op.add_column("generated_content", sa.Column("variant_a_text", sa.Text(), nullable=True))
    op.add_column("generated_content", sa.Column("variant_b_text", sa.Text(), nullable=True))
    op.add_column("generated_content", sa.Column("variant_a_eval_json", sa.JSON(), nullable=True))
    op.add_column("generated_content", sa.Column("variant_b_eval_json", sa.JSON(), nullable=True))
    op.add_column("generated_content", sa.Column("selected_variant", sa.String(length=1), nullable=True))

    connection = op.get_bind()
    rows = connection.execute(
        sa.text(
            """
            SELECT id, prompt, generated_text, tone, sentiment_score
            FROM generated_content
            """
        )
    ).fetchall()

    for row in rows:
        eval_payload = {"tone": row.tone, "score": row.sentiment_score}
        connection.execute(
            sa.text(
                """
                UPDATE generated_content
                SET
                    original_prompt = :original_prompt,
                    variant_a_text = :variant_a_text,
                    variant_b_text = :variant_b_text,
                    variant_a_eval_json = CAST(:variant_a_eval_json AS JSON),
                    variant_b_eval_json = CAST(:variant_b_eval_json AS JSON)
                WHERE id = :id
                """
            ),
            {
                "id": row.id,
                "original_prompt": row.prompt,
                "variant_a_text": row.generated_text,
                "variant_b_text": row.generated_text,
                "variant_a_eval_json": json.dumps(eval_payload),
                "variant_b_eval_json": json.dumps(eval_payload),
            },
        )

    with op.batch_alter_table("generated_content") as batch_op:
        batch_op.alter_column("original_prompt", nullable=False)
        batch_op.alter_column("variant_a_text", nullable=False)
        batch_op.alter_column("variant_b_text", nullable=False)
        batch_op.alter_column("variant_a_eval_json", nullable=False)
        batch_op.alter_column("variant_b_eval_json", nullable=False)

        batch_op.drop_column("prompt")
        batch_op.drop_column("generated_text")
        batch_op.drop_column("tone")
        batch_op.drop_column("sentiment_score")


def downgrade():
    op.add_column("generated_content", sa.Column("prompt", sa.Text(), nullable=True))
    op.add_column("generated_content", sa.Column("generated_text", sa.Text(), nullable=True))
    op.add_column("generated_content", sa.Column("tone", sa.String(length=20), nullable=True))
    op.add_column("generated_content", sa.Column("sentiment_score", sa.Float(), nullable=True))

    connection = op.get_bind()
    rows = connection.execute(
        sa.text(
            """
            SELECT id, original_prompt, variant_a_text, variant_a_eval_json
            FROM generated_content
            """
        )
    ).fetchall()

    for row in rows:
        eval_payload = row.variant_a_eval_json or {}
        connection.execute(
            sa.text(
                """
                UPDATE generated_content
                SET
                    prompt = :prompt,
                    generated_text = :generated_text,
                    tone = :tone,
                    sentiment_score = :sentiment_score
                WHERE id = :id
                """
            ),
            {
                "id": row.id,
                "prompt": row.original_prompt,
                "generated_text": row.variant_a_text,
                "tone": eval_payload.get("tone", "neutral"),
                "sentiment_score": eval_payload.get("score", 0.0),
            },
        )

    with op.batch_alter_table("generated_content") as batch_op:
        batch_op.alter_column("prompt", nullable=False)
        batch_op.alter_column("generated_text", nullable=False)
        batch_op.alter_column("tone", nullable=False)
        batch_op.alter_column("sentiment_score", nullable=False)

        batch_op.drop_column("original_prompt")
        batch_op.drop_column("variant_a_text")
        batch_op.drop_column("variant_b_text")
        batch_op.drop_column("variant_a_eval_json")
        batch_op.drop_column("variant_b_eval_json")
        batch_op.drop_column("selected_variant")
