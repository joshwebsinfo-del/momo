from unittest.mock import patch

from django.test import SimpleTestCase

from config.settings.base import get_database_config


class DatabaseConfigTests(SimpleTestCase):
    def test_malformed_database_port_falls_back_to_env_default(self):
        with patch('config.settings.base.config') as mock_config:
            mock_config.side_effect = lambda name, default='', cast=None: {
                'DATABASE_URL': 'postgres://user:pass@localhost:Joshuamujakari6945/dbname',
                'SUPABASE_DB_NAME': 'postgres',
                'SUPABASE_DB_USER': 'postgres',
                'SUPABASE_DB_PASSWORD': 'secret',
                'SUPABASE_DB_HOST': 'db.example.com',
                'SUPABASE_DB_PORT': '5432',
                'SUPABASE_URL': '',
                'SECRET_KEY': 'test',
                'DEBUG': False,
                'ALLOWED_HOSTS': 'localhost',
            }.get(name, default)

            config = get_database_config()

            self.assertEqual(config['HOST'], 'localhost')
            self.assertEqual(config['PORT'], '5432')
            self.assertEqual(config['NAME'], 'dbname')
