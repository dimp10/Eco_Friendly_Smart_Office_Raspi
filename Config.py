# Config to change how the Programme Works


# Login Credentials for Network
deviceType = "cisco_xe"
host = "100.71.10.5"
username_="gbadmin"
password_="gb_1nf0rmat"

# All the ports that you want to be closed to save electricity
interfaces = ["gigabitEthernet 1/0/29", "gigabitEthernet 1/0/30", "gigabitEthernet 1/0/31"]

# Starting working hours followed by the Ending working hours both in hours
minHours = 9
maxHours = 18

# Time that it Sleeps followed by amount of time it checks for movement for both in seconds
sleepTime = 600
checkTime = 300