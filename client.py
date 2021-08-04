import socket
import time


def read_file(status):
# A function that is read lines from a file and check if data correct
# @status: is a handler of a file
        id_station = status.readline()
        if not id_station[:-1].isdigit():
            print("Station ID must be number")
            return ""

        alarm1 = status.readline()
        if not (alarm1[:-1] == "1" or alarm1[:-1] == "0"):
            print("Alarm 1 must be 1 or 0")
            return ""

        alarm2 = status.readline()
        if len(alarm2) == 2 and alarm2[1] == "\n": #check if has end-line on the end of line alarm-2
            alarm2 = alarm2[:-1]
        if not (alarm2 == "1" or alarm2 == "0"):
            print("Alarm 2 must be 1 or 0")
            return ""

        return id_station + alarm1 + alarm2


#----------------------------------------------------------------------------
if __name__ == "__main__":

    print("To stop connection press ctrl+c")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            while True: # Conecting
                try:
                    sock.connect(("127.0.0.1", 54321))
                    print("Connected")
                    break
                except ConnectionRefusedError as e:
                    print(e)
                    print("Trying to connect...")
                    time.sleep(3)

            while True: # Read from file and send
                with open("status.txt", "r") as status:
                    str = read_file(status)
                    if str == "":
                        status.close()
                        time.sleep(3)
                        continue

                    print("[{} {} {}]".format(*str.split("\n")))
                    
                    sock.sendall(str.encode()) # sending data: "id_station\nalarm1\nalarm2"
                    status.close()
                    time.sleep(3)

    except KeyboardInterrupt:
        print("  Goodbye!")
        exit()
    except Exception as e:
        print(e)
        exit()