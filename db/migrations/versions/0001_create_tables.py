from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'images',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('file_path', sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        'characters',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        'image_author',
        sa.Column('image_id', sa.Integer(), sa.ForeignKey('images.id'), primary_key=True),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('authors.id'), primary_key=True),
    )
    op.create_table(
        'image_tag',
        sa.Column('image_id', sa.Integer(), sa.ForeignKey('images.id'), primary_key=True),
        sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tags.id'), primary_key=True),
    )
    op.create_table(
        'image_character',
        sa.Column('image_id', sa.Integer(), sa.ForeignKey('images.id'), primary_key=True),
        sa.Column('character_id', sa.Integer(), sa.ForeignKey('characters.id'), primary_key=True),
    )

def downgrade():
    op.drop_table('image_character')
    op.drop_table('image_tag')
    op.drop_table('image_author')
    op.drop_table('characters')
    op.drop_table('tags')
    op.drop_table('authors')
    op.drop_table('images')
