import socket
import threading
import datetime
import sqlite3

mutex = threading.Lock()

def create_database():
# A function that is building a database.
    try:
        conn = sqlite3.connect("data.sqlite")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS station_status (
                station_id INT,
                last_data TEXT,
                alarm1 INT,
                alarm2 INT,
                PRIMARY KEY(station_id)
                )""")
        conn.commit()

    except Exception as e:
        print(e)
        conn.close()
        raise Exception("Can't create database")
    finally:
        conn.close()



def save_to_database(data):
# A function that change row of given data.
# @data: is a list [id_station, alarm1, alarm2]
    try:
        time_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        conn = sqlite3.connect("data.sqlite")
        c = conn.cursor()
        c.execute("REPLACE INTO station_status VALUES (?, ?, ?, ?)",
                (int(data[0]), time_date, int(data[1]), int(data[2])))
        conn.commit()

    except Exception as e:
        print(e)
    finally:
        conn.close()


def on_new_client(client, ip):
# A function that is working in a new thread and receiving new data from a client.
# @client: is a socket
# @is: is a list [ip_client, port]
    global mutex
    print("Client connected -> ip: {} port: {}".format(ip[0], ip[1]))
    print("Waiting for connections...")
    try:
        while True:
            msg = client.recv(1024) # receiving data: "id_station\nalarm1\nalarm2"
            if msg.decode() == "": # Given client has stopped connection (return value is "")
                break
            mutex.acquire()
            save_to_database(msg.decode().split("\n"))
            mutex.release()

    except Exception as e:
        print(e)
    finally:
        print("Client disconnected -> ip: {} port: {}".format(ip[0], ip[1]))
        print("Waiting for connections...")
        client.close()


#----------------------------------------------------------------------------
if __name__ == "__main__":

    try:
        create_database()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 54321))
            sock.listen(5)
            print("To stop connection press ctrl+c")
            print("But first, close all clients connections (preference)\n")
            print("Waiting for connections...")
            
            while True:
                client, ip = sock.accept()
                threading._start_new_thread(on_new_client, (client, ip)) #Start a new section

    except KeyboardInterrupt:
        print("  Goodbye!")
        exit()
    except Exception as e:
        print(e)
        exit()

