#!/bin/bash
# Включаем запись в конфигурационный файл pg_hba.conf для разрешения всех подключений
echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf

# Включаем запись в конфигурационный файл postgresql.conf для прослушивания всех адресов
echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf