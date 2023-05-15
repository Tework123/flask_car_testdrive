"""Initial migration.

Revision ID: 02212c3db272
Revises: 
Create Date: 2023-05-13 13:45:56.805369

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '02212c3db272'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews_photo')
    op.drop_table('cars')
    op.drop_table('photos')
    op.drop_table('reviews')
    op.drop_table('brands')
    op.drop_table('main_menu')
    op.drop_table('test_drive')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id_user', sa.INTEGER(), server_default=sa.text("nextval('users_id_user_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('profile_pic', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('text', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_user', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('test_drive',
    sa.Column('id_order', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id_user', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id_car', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date_start', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('date_end', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_car'], ['cars.id_car'], name='test_drive_id_car_fkey'),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], name='test_drive_id_user_fkey'),
    sa.PrimaryKeyConstraint('id_order', name='test_drive_pkey')
    )
    op.create_table('main_menu',
    sa.Column('head_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('head_id', name='main_menu_pkey'),
    sa.UniqueConstraint('text', name='main_menu_text_key'),
    sa.UniqueConstraint('url', name='main_menu_url_key')
    )
    op.create_table('brands',
    sa.Column('id_brand', sa.INTEGER(), server_default=sa.text("nextval('brands_id_brand_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name_brand', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name_photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_brand', name='brands_pkey'),
    sa.UniqueConstraint('name_brand', name='brands_name_brand_key'),
    sa.UniqueConstraint('name_photo', name='brands_name_photo_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('reviews',
    sa.Column('id_review', sa.INTEGER(), server_default=sa.text("nextval('reviews_id_review_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('id_user', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id_car', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('text', sa.VARCHAR(length=5000), autoincrement=False, nullable=True),
    sa.Column('degree', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_car'], ['cars.id_car'], name='reviews_id_car_fkey'),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], name='reviews_id_user_fkey'),
    sa.PrimaryKeyConstraint('id_review', name='reviews_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('photos',
    sa.Column('id_photo', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_car', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name_photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_car'], ['cars.id_car'], name='photos_id_car_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_photo', name='photos_pkey'),
    sa.UniqueConstraint('name_photo', name='photos_name_photo_key')
    )
    op.create_table('cars',
    sa.Column('id_car', sa.INTEGER(), server_default=sa.text("nextval('cars_id_car_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name_car', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.Column('id_brand', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('url_video', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_brand'], ['brands.id_brand'], name='cars_id_brand_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_car', name='cars_pkey'),
    sa.UniqueConstraint('name_car', name='cars_name_car_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('reviews_photo',
    sa.Column('id_review', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id_photo', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['id_review'], ['reviews.id_review'], name='reviews_photo_id_review_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_photo', name='reviews_photo_pkey')
    )
    # ### end Alembic commands ###
