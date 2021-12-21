from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)	
