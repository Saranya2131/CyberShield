import sqlite3
from datetime import datetime


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DATABASE_NAME = "database/integrity.db"


# ==========================================
# CONNECT TO DATABASE
# ==========================================

def connect_database():
    """Connect to the SQLite database."""

    return sqlite3.connect(DATABASE_NAME)


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def create_table():
    """Create all required database tables."""

    connection = connect_database()
    cursor = connection.cursor()

    # ------------------------------------------
    # REGISTERED FILES TABLE
    # ------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registered_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL UNIQUE,
            baseline_hash TEXT NOT NULL,
            registered_at TEXT NOT NULL,
            status TEXT DEFAULT 'Not Scanned'
        )
    """)

    # ------------------------------------------
    # CHECK EXISTING COLUMNS
    # ------------------------------------------

    cursor.execute("""
        PRAGMA table_info(registered_files)
    """)

    columns = cursor.fetchall()

    column_names = [
        column[1]
        for column in columns
    ]

    # ------------------------------------------
    # ADD STATUS COLUMN IF MISSING
    # ------------------------------------------

    if "status" not in column_names:

        cursor.execute("""
            ALTER TABLE registered_files
            ADD COLUMN status TEXT DEFAULT 'Not Scanned'
        """)


    # ------------------------------------------
    # SECURITY ACTIVITY LOG TABLE
    # ------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity TEXT NOT NULL,
            file_name TEXT,
            status TEXT,
            activity_time TEXT NOT NULL
        )
    """)


    connection.commit()
    connection.close()


# ==========================================
# REGISTER FILE
# ==========================================

def register_file(
    file_name,
    file_path,
    baseline_hash
):
    """Register a file and store its baseline hash."""

    connection = connect_database()
    cursor = connection.cursor()


    registered_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute("""
        INSERT INTO registered_files
        (
            file_name,
            file_path,
            baseline_hash,
            registered_at,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        file_name,
        file_path,
        baseline_hash,
        registered_at,
        "Not Scanned"
    ))


    connection.commit()
    connection.close()


# ==========================================
# GET REGISTERED FILES
# ==========================================

def get_registered_files():
    """Return all registered files."""

    connection = connect_database()
    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            file_name,
            file_path,
            baseline_hash,
            registered_at,
            status
        FROM registered_files
        ORDER BY id DESC
    """)


    files = cursor.fetchall()

    connection.close()

    return files


# ==========================================
# UPDATE FILE STATUS
# ==========================================

def update_file_status(
    file_id,
    status
):
    """Update the status of a registered file."""

    connection = connect_database()
    cursor = connection.cursor()


    cursor.execute("""
        UPDATE registered_files
        SET status = ?
        WHERE id = ?
    """, (
        status,
        file_id
    ))


    connection.commit()
    connection.close()


# ==========================================
# ADD SECURITY ACTIVITY LOG
# ==========================================

def add_activity_log(
    activity,
    file_name=None,
    status=None
):
    """Add an activity to the security log."""

    connection = connect_database()
    cursor = connection.cursor()


    activity_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute("""
        INSERT INTO activity_logs
        (
            activity,
            file_name,
            status,
            activity_time
        )
        VALUES (?, ?, ?, ?)
    """, (
        activity,
        file_name,
        status,
        activity_time
    ))


    connection.commit()
    connection.close()


# ==========================================
# GET ACTIVITY LOGS
# ==========================================

def get_activity_logs(
    limit=20
):
    """Return recent security activities."""

    connection = connect_database()
    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            activity,
            file_name,
            status,
            activity_time
        FROM activity_logs
        ORDER BY id DESC
        LIMIT ?
    """, (
        limit,
    ))


    logs = cursor.fetchall()

    connection.close()

    return logs


# ==========================================
# GET SCAN HISTORY
# ==========================================

def get_scan_history(
    limit=50
):
    """Return previous file integrity scans."""

    connection = connect_database()
    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            file_name,
            status,
            activity_time
        FROM activity_logs
        WHERE activity = 'File Integrity Scan'
        ORDER BY id DESC
        LIMIT ?
    """, (
        limit,
    ))


    history = cursor.fetchall()

    connection.close()

    return history


# ==========================================
# UNREGISTER FILE
# ==========================================

def unregister_file(file_id):
    """
    Remove a file from CyberShield monitoring.

    This does NOT delete the actual file
    from the computer.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM registered_files
        WHERE id = ?
    """, (
        file_id,
    ))

    connection.commit()
    connection.close()