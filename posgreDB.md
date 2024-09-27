# Dokumentace k připojení k PostgreSQL databázi

Tento dokument popisuje kroky potřebné k nastavení a připojení k PostgreSQL databázi, včetně instalace ODBC ovladače pro přístup z SQL Server Management Studio (SSMS).

## Krok 1: Instalace PostgreSQL

1. **Instalace PostgreSQL**:
   Na svém serveru nebo Raspberry Pi spusťte následující příkaz:

   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```

2. **Spuštění služby PostgreSQL**:
   Ujisti se, že služba PostgreSQL běží:

   ```bash
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

## Krok 2: Vytvoření databáze a uživatelského účtu

1. **Otevři PostgreSQL shell**:
   Přihlas se do PostgreSQL pomocí uživatelského jména `postgres`:

   ```bash
   sudo -u postgres psql
   ```

2. **Vytvoření uživatelského účtu**:

   ```sql
   CREATE USER su WITH PASSWORD 'tvé_heslo';
   ```

3. **Vytvoření databáze**:

   ```sql
   CREATE DATABASE Portfolio OWNER su;
   ```

4. **Povolení uživateli přístup k databázi**:

   ```sql
   GRANT ALL PRIVILEGES ON DATABASE Portfolio TO su;
   ```

5. **Odhlášení z PostgreSQL shellu**:

   ```sql
   \q
   ```

## Krok 3: Nastavení připojení

### 1. Konfigurace `pg_hba.conf`

Otevři konfigurační soubor `pg_hba.conf`:

```bash
sudo nano /etc/postgresql/{verze}/main/pg_hba.conf
```

Přidej následující řádek pro povolení přístupu:

```plaintext
host    all             all             0.0.0.0/0               md5
```

### 2. Konfigurace `postgresql.conf`

Otevři konfigurační soubor `postgresql.conf`:

```bash
sudo nano /etc/postgresql/{verze}/main/postgresql.conf
```

Najdi a změň řádek:

```plaintext
listen_addresses = '*'
```

## Krok 4: Restart PostgreSQL

Restartuj PostgreSQL, aby se změny projevily:

```bash
sudo systemctl restart postgresql
```

## Krok 5: Instalace ODBC ovladače

1. **Stáhni a nainstaluj ODBC ovladač**:
   - Stáhni si ODBC ovladač pro PostgreSQL z [oficiálních stránek PostgreSQL](https://www.postgresql.org/ftp/odbc/versions/msi/).
   - Nainstaluj ovladač podle pokynů.

2. **Nastavení ODBC datového zdroje**:
   - Otevři **Ovládací panely** > **Nástroje pro správu** > **ODBC Data Sources (32-bit nebo 64-bit)**.
   - Vyber „User DSN“ nebo „System DSN“ a klikni na „Add“.
   - Vyber „PostgreSQL Unicode“ nebo „PostgreSQL ANSI“ a klikni na „Finish“.
   - Vyplň potřebné informace:
     - **Data Source Name**: `PostgreSQL_DB`
     - **Server**: IP adresa serveru s PostgreSQL
     - **Database**: `Portfolio`
     - **Port**: 5432
     - **Username**: `su`
     - **Password**: `tvé_heslo`

3. **Test ODBC připojení**:
   - Klikni na „Test“ a ověř, zda je připojení úspěšné.

## Krok 6: Připojení v SSMS

1. **Otevři SQL Server Management Studio (SSMS)**.
2. **Vyber "Connect" > "Database Engine"**.
3. **V okně pro připojení**:
   - **Server name**: `192.168.88.158,5432` (nebo název datového zdroje).
   - **Authentication**: `SQL Server Authentication`.
   - **User name**: `su`.
   - **Password**: `tvé_heslo`.
4. **Klikni na "Connect"**.

## Krok 7: Ověření připojení

Pokud se připojení podařilo, měl bys vidět databázi `Portfolio` a mohl bys provádět SQL dotazy.

## Krok 8: Zálohování struktury databáze

Pokud chceš vytvořit zálohu struktury databáze (bez dat), můžeš použít následující skript:

Pokud chcete vytvořit skript, který vygeneruje pouze strukturu tabulek a funkcí bez dat, můžete použít nástroj pg_dump z příkazového řádku:

```bash
pg_dump -U username -h hostname -s -d database_name > schema_backup.sql
```

## Závěr

Nyní bys měl být schopen připojit se k PostgreSQL databázi jak z Pythonu, tak z SQL Server Management Studio (SSMS).
