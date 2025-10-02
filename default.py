import xmlrpc.client

# Dati di connessione
HOST = "localhost"
PORT = 8069
DB = "odoo"
USER = "f.cresci.behomecasa@gmail.com"
PASS = "fede2004"

# Connessione
root = f'http://{HOST}:{PORT}/xmlrpc/'
uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)
sock = xmlrpc.client.ServerProxy(root + 'object')

# Legge tutti i prodotti
templates = sock.execute(DB, uid, PASS, 'product.template', 'search_read', [], ['id','default_code','name'])

print("🔹 Tutti i default_code presenti in Odoo:")
for t in templates:
    code = t['default_code'] or "(nessun codice)"
    print(f"ID {t['id']}: {code} - {t['name']}")
