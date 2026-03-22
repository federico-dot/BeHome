import xmlrpc.client
import csv

# 🔹 Dati di connessione
HOST = "localhost"
PORT = 8069
DB = "your db"
USER = "Email valida"
PASS = "********"

# 🔹 Connessione Odoo
root = f'http://{HOST}:{PORT}/xmlrpc/'
uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)
print(f"Logged in as {USER} (uid: {uid})")
sock = xmlrpc.client.ServerProxy(root + 'object')

def normalize_name(name):
    return name.lower().capitalize()

# 🔹 Lettura CSV e raggruppamento per prodotto
products = {}
with open("C:\\Users\\fcres\\Desktop\\behome\\prodotti_odoo_clean.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        default_code = row['default_code'].strip()
        name_norm = normalize_name(row['name'])
        attr_name = row.get('attribute_name', '')
        attr_value = row.get('attribute_value', '')

        key = (default_code, name_norm)
        if key not in products:
            products[key] = {
                'row': row,
                'attributes': {}
            }
        if attr_name:
            if attr_name not in products[key]['attributes']:
                products[key]['attributes'][attr_name] = set()
            products[key]['attributes'][attr_name].add(attr_value)

# 🔹 Creazione/aggiornamento prodotti
for (default_code, name), info in products.items():
    row = info['row']
    attributes = info['attributes']

    # Controlla se esiste un prodotto con lo stesso default_code
    existing_variant = sock.execute(DB, uid, PASS, 'product.product', 'search', [('default_code', '=', default_code)])
    if existing_variant:
        print(f"⚠️ Prodotto con default_code {default_code} già esistente → nessuna creazione")
        continue

    # Cerca template per nome
    existing_templates = sock.execute(DB, uid, PASS, 'product.template', 'search', [('name','=',name)])
    if existing_templates:
        template_id = existing_templates[0]
        print(f"⚠️ Template esistente: {name} (ID {template_id})")
    else:
        # Crea il template con i nuovi campi dal CSV
        template_vals = {
            'name': name,
            'type': 'consu',
            'list_price': float(row.get('list_price', 0) or 0),
            'standard_price': float(row.get('standard_price', 0) or 0),
            'uom_id': int(row['uom_id']),
            'uom_po_id': int(row['uom_po_id']),
            'categ_id': int(row['categ_id']),
            'description_sale': row.get('descrizione', ''),     # descrizione
            'description_purchase': row.get('note', ''),        # note acquisto
        }
        if not attributes:  # Nessun attributo → default_code direttamente sul template
            template_vals['default_code'] = default_code
        template_id = sock.execute(DB, uid, PASS, 'product.template', 'create', template_vals)
        print(f"✅ Prodotto creato: {name} (ID {template_id})")

    # 🔹 Gestione fornitore (solo nome)
    supplier_name = row.get('supplier')
    if supplier_name:
        # Cerca partner esistente o crea uno nuovo
        supplier_ids = sock.execute(DB, uid, PASS, 'res.partner', 'search', [('name', '=', supplier_name)])
        if supplier_ids:
            supplier_id = supplier_ids[0]
        else:
            supplier_id = sock.execute(DB, uid, PASS, 'res.partner', 'create', {'name': supplier_name})

        # Controlla se esiste già supplierinfo per questo template e fornitore
        existing_supplierinfo = sock.execute(DB, uid, PASS, 'product.supplierinfo', 'search', [
            ('product_tmpl_id', '=', template_id),
            ('partner_id', '=', supplier_id)
        ])
        if not existing_supplierinfo:
            supplierinfo_vals = {
                'partner_id': supplier_id,
                'product_tmpl_id': template_id
            }
            sock.execute(DB, uid, PASS, 'product.supplierinfo', 'create', supplierinfo_vals)

    # 🔹 Aggiunge attributi e valori
    for attr_name, values in attributes.items():
        attr_ids = sock.execute(DB, uid, PASS, 'product.attribute', 'search', [('name','=',attr_name)])
        if attr_ids:
            attr_id = attr_ids[0]
        else:
            attr_id = sock.execute(DB, uid, PASS, 'product.attribute', 'create', {
                'name': attr_name,
                'create_variant': 'always'
            })

        value_ids = []
        for val in values:
            val_ids = sock.execute(DB, uid, PASS, 'product.attribute.value', 'search', [
                ('name','=',val), ('attribute_id','=',attr_id)
            ])
            if val_ids:
                val_id = val_ids[0]
            else:
                val_id = sock.execute(DB, uid, PASS, 'product.attribute.value', 'create', {
                    'name': val,
                    'attribute_id': attr_id
                })
            value_ids.append(val_id)

        # Collega attributo e valori al template
        existing_lines = sock.execute(DB, uid, PASS, 'product.template.attribute.line', 'search', [
            ('product_tmpl_id','=',template_id),
            ('attribute_id','=',attr_id)
        ])
        if existing_lines:
            sock.execute(DB, uid, PASS, 'product.template.attribute.line', 'write', existing_lines, {
                'value_ids': [(6, 0, value_ids)]
            })
        else:
            sock.execute(DB, uid, PASS, 'product.template.attribute.line', 'create', {
                'product_tmpl_id': template_id,
                'attribute_id': attr_id,
                'value_ids': [(6, 0, value_ids)]
            })

    # 🔹 Dopo la creazione delle varianti, assegna default_code univoco
    variant_ids = sock.execute(DB, uid, PASS, 'product.product', 'search', [('product_tmpl_id','=',template_id)])
    variant_codes = []
    for vid in variant_ids:
        variant_data = sock.execute(DB, uid, PASS, 'product.product', 'read', [vid], ['product_template_attribute_value_ids'])
        attr_values = []
        if variant_data and variant_data[0]['product_template_attribute_value_ids']:
            value_recs = sock.execute(DB, uid, PASS, 'product.template.attribute.value', 'read',
                                      variant_data[0]['product_template_attribute_value_ids'], ['name'])
            attr_values = [v['name'] for v in value_recs]
        if attr_values:
            variant_code = f"{default_code}-{'-'.join(attr_values)}"
        else:
            variant_code = default_code
        sock.execute(DB, uid, PASS, 'product.product', 'write', [vid], {
            'default_code': variant_code
        })
        variant_codes.append(variant_code)

    if variant_codes:
        print(f"💠 Varianti create per {name}: {', '.join(variant_codes)}")
