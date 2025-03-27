# Module Import
from flask import Flask, redirect, url_for, render_template, request
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


app = Flask(__name__)


@app.route("/")
def mainpage():
    conn = dbconnect()
    cur = conn.cursor()

    button_action = request.args.get("But")
    if button_action == "Create":
        add_contact(cur, request.args.get("fname"), request.args.get("lname"), request.args.get("email"))
        cur.close()
        conn.close()
        return render_template("CRUD.html", content="")

    if button_action == "Read":
        contacts = []
        cur.execute("SELECT id, first_name, last_name, email FROM public.contacts ORDER BY id DESC LIMIT 5")
        for id, fn, ln, em in cur.fetchall():
            contacts.append(f'<tr><td>{id}</td><td>{fn}</td><td>{ln}</td><td>{em}</td></tr>')
        cur.close()
        conn.close()
        return render_template("CRUD.html", content="\n".join(contacts))

    if button_action == "Update":
        replace_contact(cur, request.args.get("id"), request.args.get("fname"), request.args.get("lname"),
                        request.args.get("email"))
        cur.close()
        conn.close()
        return render_template("CRUD.html", content="")

    if button_action == "Delete":
        delete_contact(cur, request.args.get("id"))
        cur.close()
        conn.close()
        return render_template("CRUD.html", content="")

    cur.close()
    conn.close()
    return render_template("CRUD.html", content="")


if __name__ == "__main__":
    app.run()
