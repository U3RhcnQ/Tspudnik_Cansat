import serial, time, csv, os, math
from datetime import datetime




def serialListen(filename):

    print("function running..")

    val = bytes("loging" + "", encoding="utf-8")
    s.write(val)

    # 00001101
    while True:

        try:
            data = s.readline()
            # Data Cleanup
            data = data.strip()
            data = data.decode("utf-8")
            list1 = str(data).split(",")
            
            # Variable Creation
            ID = list1[0]
            PR = list1[1]
            TMP = list1[2]
            TMP2 = list1[3]
            HUM = list1[4]
            LL = list1[5]
            NL = list1[6]
            SO = list1[7]
            CO = list1[8]
            X = list1[9]
            Y = list1[10]
            Z = list1[11]
            STR = list1[12]
            TMS = list1[13]
            
        except:
            print("Garbage Data: " + str(data))
            continue



        now = datetime.now()
        time_now = now.strftime("%H:%M:%S")
        ALT = height_from_pressure(float(PR))
        list1.append(ALT)
        list1.append(time_now)

        if ID == "ID1234":
            if filename != "null":
                log_data_to_csv(list1, filename)
            print(list1)


def height_from_pressure(P):
    P = P*100
    """
    Computes the height above sea level in meters corresponding to the given atmospheric pressure in Pascals.
    Assumes a standard atmosphere.
    """
    p0 = 101325.0 # standard sea level pressure in Pascals
    gamma = 5.25588
    R = 8.31447 # universal gas constant in J/mol/K
    M = 0.0289644 # molar mass of dry air in kg/mol
    g0 = 9.80665 # standard acceleration due to gravity in m/s^2

    h = (1 - math.exp(math.log(P/p0)/gamma)) * (R * 288.15) / (g0 * M)
    return h


def log_data_to_csv(data_list, filename):
    # Open the file in append mode
    with open(filename, "a", newline="") as file:

        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the data rows
        writer.writerow(data_list)


#  print('Data has been logged into', filename)


def ping():

    print(ping_helper())
    start()


def ping_helper():
    s.timeout=2
    global Ping
    global connected
    
    val = bytes("ping" + "", encoding="utf-8")
    start_time = time.perf_counter()
    s.write(val)
    data = ""
    
    while data != "pong":
        try:
            data = s.readline()
            # Data Cleanup
            data = data.strip()
            data = data.decode("utf-8")
        except:
            pass
        if ((time.perf_counter() - start_time) * 1000) > 1000:
            connected = "False"
            Ping = str(0.0)+"ms"
            s.timeout=None
            return 
            
        
    ping = round((time.perf_counter() - start_time) * 1000, 2)
    Ping = str(ping)+"ms"
    connected = "True"
    return ping


def csv_setup():
    # Set the directory where you want to save the CSV file
    directory = ""

    # Set the base name for the CSV file
    base_filename = "Data"

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Combine the base filename and timestamp to get the full filename
    full_filename = base_filename + "_" + timestamp + ".csv"

    # Check if the file already exists
    if os.path.isfile(directory + full_filename):
        # File already exists, do nothing
        print("File already exists:", full_filename)
    else:
        # File does not exist, create a new file
        with open(directory + full_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Can ID", "Pressure", "Temperature 1","Temperature 2","Humidity","Light Level","Noise Level","Sound Level","Compass heading","X","Y","Z","Strenght","Runtime"])  # Add header row
        print("New file created:", full_filename)
        return full_filename


commands = [1, 2, 3, 4, 5, 6]

admin_pannel_message = """


 1 - Ping Can
 2 - Connection Manager
 3 - Dry run (Test)
 4 - Start Session
 5 - reports
 6 - refresh

 """

def statusbar():
    print(
        "####################################### Can Control Terminal ################################\n"
    )
    print(
        "Status: "
        + "  Conected:"
        + connected
        + "  Ping:"
        + str(ping_helper())
        + "  Systems:"
        + Systems
    )


def start():
    statusbar()
    print(admin_pannel_message)
    print("\n\nWhat operation would you like to perform ?")
    commandinput()


def refresh():
    os.system("cls")
    


def commandinput():
    while True:
        # Get user input and validate it
        while True:
            user_input = input("Enter command number (1-6): ")
            if user_input.isdigit() and int(user_input) in commands:
                break
            else:
                refresh()
                print("Invalid input. Please enter a number between 1 and 6.")

        # Trigger function based on user input
        if user_input == "1":
            # Execute function for command 1
            print("Executing command 1 - Ping Can")
            ping()
        elif user_input == "2":
            # Execute function for command 2
            print("Executing command 2 - Connection Manager")
        elif user_input == "3":
            # Execute function for command 3
            print("Executing command 3 - Dry run (Test)")
            serialListen("null")
        elif user_input == "4":
            # Execute function for command 4
            serialListen(csv_setup())
            print("Executing command 4 - Start Session")
        elif user_input == "5":
            # Execute function for command 5
            print("Executing command 5 - reports")
        elif user_input == "6":
            # Execute function for command 6
            print("Executing command 6 - refresh")
            refresh()
            statusbar()
            continue



try:
    s = serial.Serial("COM12")
    s.baudrate = 9600
    s.setRTS(0)
    s.timeout=None
except Exception as e:
    print("Communications Failure")
    print(e)
    time.sleep(1)


connected = "False"
Ping = "0.0ms"
Systems = "N/A"


start()
