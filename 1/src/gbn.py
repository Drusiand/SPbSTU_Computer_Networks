import time

from utils import Message, MessageStatus


def GBN_sender(window_size, max_number, timeout, answer_msg_queue, send_msg_queue, posted_msgs):
    curr_number = 0
    last_ans_number = -1
    start_time = time.time()
    while last_ans_number < max_number:
        expected_number = (last_ans_number + 1) % window_size

        if answer_msg_queue.has_msg():
            ans = answer_msg_queue.get_message()
            if ans.number == expected_number:
                # последовательное подтверждение пакетов - всё ок
                last_ans_number += 1
                start_time = time.time()
            else:
                # произошёл сбой, нужно повторить отправку сообщений с последнего подтверждённого
                curr_number = last_ans_number + 1

        # долго нет ответа с последнего подтверждения
        if time.time() - start_time > timeout:
            # произошёл сбой, нужно повторить отправку сообщений с последнего подтверждённого
            curr_number = last_ans_number + 1
            start_time = time.time()

        if (curr_number < last_ans_number + window_size) and (curr_number <= max_number):
            #   отправляем не более window_size сообщений наперёд
            k = curr_number % window_size
            msg = Message()
            msg.number = k
            msg.real_number = curr_number
            send_msg_queue.send_message(msg)
            posted_msgs.append(f"{curr_number}({k})")

            curr_number += 1

    msg = Message()
    msg.data = "STOP"
    send_msg_queue.send_message(msg)


def GBN_receiver(window_size, send_msg_queue, answer_msg_queue, received_msgs):
    expected_number = 0
    while True:
        if send_msg_queue.has_msg():
            curr_msg = send_msg_queue.get_message()
            # print(f"res: {curr_msg} | {expected_number}")
            if curr_msg.data == "STOP":
                break

            if curr_msg.status == MessageStatus.LOST:
                continue

            if curr_msg.number == expected_number:
                ans = Message()
                ans.number = curr_msg.number
                answer_msg_queue.send_message(ans)

                received_msgs.append(f"{curr_msg.real_number}({curr_msg.number})")
                expected_number = (expected_number + 1) % window_size

            else:
                continue
