MSSQL_CONFIG = {
    'driver': '{ODBC Driver 18 for SQL Server}',
    'server': '121.141.174.121,1433',
    'database': 'KIOSK',
    'username': 'nssdb',
    'password': 'nss2109',
    'trust_cert': 'yes'
}

def get_connection_string():
    c = MSSQL_CONFIG
    return (
        f"DRIVER={c['driver']};"
        f"SERVER={c['server']};"
        f"DATABASE={c['database']};"
        f"UID={c['username']};"
        f"PWD={c['password']};"
        f"TrustServerCertificate={c['trust_cert']};"
    )
