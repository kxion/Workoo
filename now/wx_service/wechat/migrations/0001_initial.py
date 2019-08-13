# Generated by Django 2.1 on 2019-08-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('token', models.CharField(default=None, max_length=2048, verbose_name='token')),
                ('free', models.CharField(default=1, max_length=10, verbose_name='每日免费次数')),
                ('count', models.CharField(default=50, max_length=10, verbose_name='包月每日次数')),
                ('monthly', models.CharField(default=None, max_length=2048, verbose_name='包月配置')),
                ('event', models.CharField(default=None, max_length=2048, verbose_name='事件配置')),
            ],
            options={
                'verbose_name': '配置表',
                'db_table': 'config',
            },
        ),
        migrations.CreateModel(
            name='MonthInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('openid', models.CharField(max_length=50, verbose_name='用户名')),
                ('count', models.CharField(default=0, max_length=10, verbose_name='已查询次数')),
                ('type', models.CharField(default=0, max_length=10, verbose_name='类型')),
                ('months', models.CharField(default=0, max_length=10, verbose_name='包月')),
            ],
            options={
                'verbose_name': '包月信息',
                'db_table': 'month_info',
            },
        ),
        migrations.CreateModel(
            name='TransactionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('out_trade_no', models.CharField(max_length=32, unique=True, verbose_name='商户订单号')),
                ('openid', models.CharField(max_length=50, verbose_name='用户名')),
                ('amount', models.CharField(max_length=10, verbose_name='金额')),
                ('type', models.CharField(max_length=10, verbose_name='交易类型')),
                ('status', models.CharField(max_length=10, verbose_name='交易状态')),
            ],
            options={
                'verbose_name': '交易信息',
                'db_table': 'transaction_info',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('openid', models.CharField(max_length=50, unique=True, verbose_name='用户名')),
                ('balance', models.CharField(default=0, max_length=10, verbose_name='余额')),
                ('promoter', models.CharField(default='null', max_length=50, verbose_name='推广人')),
                ('promotions', models.CharField(default=0, max_length=10, verbose_name='推广人数')),
                ('current', models.CharField(default='null', max_length=50, verbose_name='当前查询项目')),
                ('guarantee', models.CharField(default=0, max_length=10, verbose_name='保修查询')),
                ('id_activate', models.CharField(default=0, max_length=10, verbose_name='ID 锁')),
                ('id_black_white', models.CharField(default=0, max_length=10, verbose_name='ID 黑白')),
            ],
            options={
                'verbose_name': '用户信息',
                'db_table': 'user_info',
            },
        ),
    ]
