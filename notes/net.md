# SSH: Конфигурация, ключи, передача файлов и туннели

## 1. Как настроен `~/.ssh/config`
Файл `~/.ssh/config` позволяет создавать алиасы (ярлыки) для SSH-подключений, чтобы не вводить каждый раз длинные команды. 

**Мой текущий конфиг:**
```text
Host myserver
    HostName 192.168.1.100      # IP-адрес или домен сервера
    User admin                  # Имя пользователя на сервере
    Port 22                     # Порт SSH (по умолчанию 22, можно не указывать)
    IdentityFile ~/.ssh/id_ed25519 # Путь к приватному ключу
    ServerAliveInterval 60      # Отправка keep-alive пакетов каждые 60 сек (защита от разрыва)

Туннель -L (Local Port Forwarding) — это проброс локального порта через зашифрованный SSH-канал на удаленный хост.
Синтаксис:
ssh -L [локальный_порт]:[целевой_хост]:[целевой_порт] [ssh_сервер]
Пример из практики:
ssh -L 9090:localhost:8080 myserver

SSH BatchMode (Пакетный режим)

### Что это и зачем нужно
По умолчанию, если SSH не может войти по ключу, он зависает и ждет, пока вы введете пароль в консоли. Также при первом подключении он спрашивает: *"Are you sure you want to continue connecting (yes/no)?"*.

Это отлично для ручной работы, но **смертельно для скриптов и cron-задач**. Если скрипт запущен в фоне (например, ночной бэкап через `rsync`), он зависнет навечно, ожидая ввода пароля, которого никто не введет.

**`BatchMode yes`** решает эту проблему. Он полностью отключает все интерактивные запросы:
1. Не будет запрашивать пароль или парольную фразу (passphrase) от ключа.
2. Не будет спрашивать подтверждение отпечатка хоста (fingerprint).

Если аутентификация по ключу невозможна, SSH **сразу же завершит работу с ошибкой** (вернет ненулевой код выхода), вместо того чтобы висеть и ждать.

### Как использовать

**Вариант 1: Прямо в команде (через флаг `-o`)**
Удобно для разовых скриптов:
```bash
# Попытается зайти по ключу. Если не получится - сразу упадет с ошибкой, не спрашивая пароль.
ssh -o BatchMode=yes myserver "echo 'Hello from script'"

# То же самое для rsync
rsync -avz -e "ssh -o BatchMode=yes" /local/dir/ myserver:/remote/dir/
-
-----------------
Session7

# UFW базовые команды 
1) sudo ufw status

```Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere                  
OpenSSH (v6)               ALLOW       Anywhere (v6)             
```
2) sudo ufw enable - включение 
3) sudo ufw reload - перезагрузка правил
4) sudo ufw reset - сброс дло заводскиз
5) sudo ufw allow 80 — разрешить входящие соединения на порт 80 (TCP и UDP).
6) sudo ufw allow 80/tcp — разрешить только TCP-трафик для порта
7) sudo ufw allow 53/udp — разрешить только UDP-трафик для порта
8) sudo ufw deny 8080 — заблокировать входящие подключения для порта 8080
9) sudo ufw allow 8000:9000/tcp — открыть диапазон портов
10) sudo ufw delete allow 80 — удалить разрешающее правило по его тексту
11) sudo ufw app list — показать список доступных профилей программ

Открытые правила на моей тачке 
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

Карта портов:
To                         Action      From
--                         ------      ----
22/tcp (OpenSSH)           ALLOW IN    Anywhere                  
22/tcp (OpenSSH (v6))      ALLOW IN    Anywhere (v6)             
Netid State  Recv-Q Send-Q Local Address:Port   Peer Address:PortProcess                                 
udp   UNCONN 0      0            0.0.0.0:mdns        0.0.0.0:*                                           
udp   UNCONN 0      0            0.0.0.0:56630       0.0.0.0:*                                           
udp   UNCONN 0      0            0.0.0.0:46572       0.0.0.0:*    users:(("syncthing",pid=1427813,fd=14))
udp   UNCONN 0      0            0.0.0.0:bootpc      0.0.0.0:*                                           
udp   UNCONN 0      0            0.0.0.0:21027       0.0.0.0:*    users:(("syncthing",pid=1427813,fd=22))
udp   UNCONN 0      0               [::]:mdns           [::]:*                                           
udp   UNCONN 0      0                  *:22000             *:*    users:(("syncthing",pid=1427813,fd=13))
udp   UNCONN 0      0               [::]:42485          [::]:*    users:(("syncthing",pid=1427813,fd=15))
udp   UNCONN 0      0               [::]:42747          [::]:*                                           
udp   UNCONN 0      0               [::]:21027          [::]:*    users:(("syncthing",pid=1427813,fd=23))
tcp   LISTEN 0      4096       127.0.0.1:8384        0.0.0.0:*    users:(("syncthing",pid=1427813,fd=26))
tcp   LISTEN 0      128          0.0.0.0:ssh         0.0.0.0:*                                           
tcp   LISTEN 0      511          0.0.0.0:http        0.0.0.0:*                                           
tcp   LISTEN 0      4096               *:22000             *:*    users:(("syncthing",pid=1427813,fd=11))
tcp   LISTEN 0      128             [::]:ssh            [::]:*                                           
tcp   LISTEN 0      511             [::]:http           [::]:*                                           



# FAIL2BAN
Устанавливаем, и настраиваем кофинг  /etc/fail2ban/jail.local. jail.local — это твой личный файл настроек, который переопределяет jail.conf. При обновлении пакета jail.conf может перезаписаться, а jail.local — никогда. Это стандартная практика в Fail2Ban.
[sshd]
enabled   = true
maxretry  = 6
findtime  = 1h
bantime   = 1d

Чтобы заработало, надо еще настроить sudo nano /etc/fail2ban/jail.d/defaults-debian.conf и добавить откуда читать логи 
[sshd]
enabled = true
backend = systemd
