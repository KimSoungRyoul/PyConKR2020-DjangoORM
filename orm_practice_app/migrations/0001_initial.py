# Generated by Django 3.1 on 2020-08-17 07:31

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AAB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='dsfsdf', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('tel_num', models.CharField(max_length=128, null=True)),
                ('address', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateTimeField(auto_created=True)),
                ('descriptions', models.CharField(default='비어있음..', max_length=128)),
                ('order_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel_num', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(help_text='서울시,안양시,...', max_length=128)),
                ('gu', models.CharField(default='', help_text='서초구, 강남구,...,', max_length=128)),
                ('detail', models.CharField(default='', help_text='104동 101호', max_length=128)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orm_practice_app.useraddress')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.PositiveIntegerField(default=0)),
                ('product_owned_company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orm_practice_app.company')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_cnt', models.PositiveIntegerField(default=1)),
                ('amount_of_credited_mileage', models.PositiveIntegerField()),
                ('related_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orm_practice_app.order')),
                ('related_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orm_practice_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product_set_included_order',
            field=models.ManyToManyField(related_name='ordered_product_set', through='orm_practice_app.OrderedProduct', to='orm_practice_app.Product'),
        ),
        migrations.CreateModel(
            name='Mileage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=0)),
                ('descriptions', models.CharField(max_length=128, null=True)),
                ('owned_userinfo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('related_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orm_practice_app.order')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='aab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orm_practice_app.aab'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='userinfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orm_practice_app.userinfo'),
        ),
    ]
