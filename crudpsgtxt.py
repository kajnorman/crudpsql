# Module Import
import psycopg2
import sys


def add_contact(cur, first_name, last_name, email):
    cur.execute("INSERT INTO public.contacts(first_name, last_name, email) VALUES (%s, %s, %s)",
                (first_name, last_name, email))


# Add Multiple Rows
def add_multiple_contacts(cur, data):
    cur.executemany("INSERT INTO public.contacts(first_name, last_name, email) VALUES (%s, %s, %s)", data)


# Replace Contact
def replace_contact(cur, contact_id, first_name, last_name, email):
    cur.execute("INSERT INTO public.contacts(id, first_name, last_name, email) VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (id) DO UPDATE SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name, email = EXCLUDED.email",
                (contact_id, first_name, last_name, email))


# Print List of Contacts
def print_contacts(cur):
    contacts = []
    cur.execute("SELECT id, first_name, last_name, email FROM public.contacts")
    for id, first_name, last_name, email in cur.fetchall():
        contacts.append(f"{id} {first_name} {last_name} <{email}>")
    print("\n".join(contacts))


# Delete Contact
def delete_contact(cur, id):
    cur.execute("DELETE FROM public.contacts WHERE id = %s", (id,))


# Instantiate Connection
def dbconnect():
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="SuPost",  #"password1",
            host="localhost",
            port=5432,
            database="MinDatabase"
        )
        conn.autocommit = True
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        sys.exit(1)
    return conn


def mainpage():
    #forbind til database
    conn = dbconnect()
    cur = conn.cursor()
    #print kontaktlisten
    print_contacts(cur)

    #konverter til html-tabel
    contacts = []
    cur.execute("SELECT id, first_name, last_name, email FROM public.contacts ORDER BY id DESC LIMIT 5")
    for id, fn, ln, em in cur.fetchall():
        contacts.append(f'<tr><td>{id}</td><td>{fn}</td><td>{ln}</td><td>{em}</td></tr>')

    #luk forbindelsen
    cur.close()
    conn.close()
    print("\n".join(contacts))


mainpage()
