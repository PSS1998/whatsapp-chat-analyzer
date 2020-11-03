from datetime import datetime, timedelta
import numpy as np

from draw import draw


my_username = "Parsa Sadri"
username = input("Enter the name of file containing the chats\n")
message_times = []
time_diffrence = timedelta(hours = 3)
receive_response_count = 0
receive_total_response_time = 0
sent_response_count = 0
sent_total_response_time = 0
num_sent_start_conversation = 0
num_receive_start_conversation = 0
num_total_sent = 0
num_total_receive = 0
count_conversation = 0
last_msg_date = 0
last_msg_id = 0
with open(username+'.txt', 'r') as msg_file:
    lines = msg_file.readlines()
    for i, line in enumerate(lines):
        if " - "+my_username in line:
            num_total_sent += 1
            line_split = line.split(" - ")
            msg_date = line_split[0]
            msg_date = datetime.strptime(msg_date, '%m/%d/%y, %I:%M %p')
            message_times.append([msg_date, True])
            new_msg_time = msg_date
            new_msg_id = True
            if i != 0:
                if (new_msg_time > last_msg_date+time_diffrence):
                    num_sent_start_conversation += 1
                    count_conversation += 1
                else:
                    if last_msg_id != new_msg_id:
                        receive_response_count += 1
                        receive_response_time = (new_msg_time - last_msg_date).total_seconds()
                        receive_total_response_time += receive_response_time
            last_msg_date = new_msg_time
            last_msg_id = new_msg_id
        elif " - "+username in line:
            num_total_receive += 1
            line_split = line.split(" - ")
            msg_date = line_split[0]
            msg_date = datetime.strptime(msg_date, '%m/%d/%y, %I:%M %p')
            message_times.append([msg_date, False])
            new_msg_time = msg_date
            new_msg_id = False
            if i != 1:
                if (new_msg_time > last_msg_date+time_diffrence):
                    num_receive_start_conversation += 1
                    count_conversation += 1
                else:
                    if last_msg_id != new_msg_id:
                        sent_response_count += 1
                        sent_response_time = (new_msg_time - last_msg_date).total_seconds()
                        sent_total_response_time += sent_response_time
            last_msg_date = new_msg_time
            last_msg_id = new_msg_id


avg_sent_response_time = sent_total_response_time / sent_response_count
avg_receive_response_time = receive_total_response_time / receive_response_count

print('')
with open(str(username)+"_analysis.txt", "w") as text_file:
    print("Number of total messages : "+str(num_total_receive+num_total_sent), file=text_file)
    print("Number of total messages sent : "+str(num_total_sent), file=text_file)
    print("Number of total messages received : "+str(num_total_receive), file=text_file)
    print("Number of total conversations : "+str(count_conversation), file=text_file)
    print("Number of total conversations sender started : "+str(num_sent_start_conversation), file=text_file)
    print("Number of total conversations receiver started : "+str(num_receive_start_conversation), file=text_file)
    print("Average response time of sender : "+str(avg_sent_response_time), file=text_file)
    print("Average response time of reciver : "+str(avg_receive_response_time), file=text_file)


file_path = str(username) + "_times.npy"
np.save(file_path, np.array(message_times))
draw(file_path, True)
