import mysql.connector
import random

con = mysql.connector.connect(host="localhost", user="root",
                              password="root", database="STUZHA")
cur = con.cursor()

states = ["IN TRANSIT", "OUT FOR DELIVERY", "DELIVERED", "CANCELLED"]

while True:
    print("\n===== STUZHA SHIPMENT MANAGEMENT =====")
    print("1. Add customer")
    print("2. Book shipment")
    print("3. Update status")
    print("4. Track shipment")
    print("5. Pay for shipment")
    print("6. Exit")
    ch = int(input("Enter choice: "))

    if ch == 1:
        name = input("Name: ")
        phone = input("Phone: ")
        city = input("City: ")
        cur.execute("INSERT INTO customers (name, phone, city) VALUES (%s,%s,%s)",
                    (name, phone, city))
        con.commit()
        print("Customer added. Customer id is", cur.lastrowid)

    elif ch == 2:
        cid = int(input("Customer id: "))
        cur.execute("SELECT name FROM customers WHERE cust_id=%s", (cid,))
        row = cur.fetchone()
        if row is None:
            print("No such customer")
        else:
            receiver = input("Receiver name: ")
            fcity = input("From city: ")
            tcity = input("To city: ")
            weight = float(input("Weight (kg): "))
            service = input("STANDARD or EXPRESS: ").upper()

            amt = 50 + 20 * weight
            if service == "EXPRESS":
                amt = amt * 1.5
            trk = "TRK" + str(random.randint(100000, 999999))

            cur.execute("INSERT INTO shipments (track_no, cust_id, receiver, "
                        "from_city, to_city, weight, service, book_date, status) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,CURDATE(),'BOOKED')",
                        (trk, cid, receiver, fcity, tcity, weight, service))
            sid = cur.lastrowid

            cur.execute("INSERT INTO tracking (ship_id, place, updated_on, remark) "
                        "VALUES (%s,%s,NOW(),'Shipment booked')", (sid, fcity))
            cur.execute("INSERT INTO payments (ship_id, amount, mode, status) "
                        "VALUES (%s,%s,'CASH','PENDING')", (sid, amt))
            con.commit()
            print("Shipment booked. Tracking no:", trk)
            print("Charge: Rs", amt)

    elif ch == 3:
        trk = input("Tracking no: ")
        cur.execute("SELECT ship_id FROM shipments WHERE track_no=%s", (trk,))
        row = cur.fetchone()
        if row is None:
            print("Shipment not found")
        else:
            for i in range(len(states)):
                print(i + 1, states[i])
            pick = int(input("Choose new status: "))
            place = input("Current place: ")
            st = states[pick - 1]
            cur.execute("UPDATE shipments SET status=%s WHERE ship_id=%s",
                        (st, row[0]))
            cur.execute("INSERT INTO tracking (ship_id, place, updated_on, remark) "
                        "VALUES (%s,%s,NOW(),%s)", (row[0], place, st))
            con.commit()
            print("Status updated")

    elif ch == 4:
        trk = input("Tracking no: ")
        cur.execute("SELECT ship_id, cust_id, from_city, to_city, status "
                    "FROM shipments WHERE track_no=%s", (trk,))
        s = cur.fetchone()
        if s is None:
            print("Shipment not found")
        else:
            cur.execute("SELECT name FROM customers WHERE cust_id=%s", (s[1],))
            c = cur.fetchone()
            print("\nSender  :", c[0])
            print("Route   :", s[2], "to", s[3])
            print("Status  :", s[4])

            cur.execute("SELECT amount, status FROM payments WHERE ship_id=%s",
                        (s[0],))
            p = cur.fetchone()
            print("Payment : Rs", p[0], "-", p[1])

            print("\nTracking history:")
            cur.execute("SELECT updated_on, place, remark FROM tracking "
                        "WHERE ship_id=%s ORDER BY updated_on", (s[0],))
            for r in cur.fetchall():
                print(r[0], "|", r[1], "|", r[2])

    elif ch == 5:
        trk = input("Tracking no: ")
        cur.execute("SELECT ship_id FROM shipments WHERE track_no=%s", (trk,))
        row = cur.fetchone()
        if row is None:
            print("Shipment not found")
        else:
            mode = input("Payment mode (UPI/CARD/CASH): ").upper()
            cur.execute("UPDATE payments SET mode=%s, status='PAID' "
                        "WHERE ship_id=%s", (mode, row[0]))
            con.commit()
            print("Payment received")

    elif ch == 6:
        print("Thank you!")
        break

    else:
        print("Wrong choice, try again")

con.close()
