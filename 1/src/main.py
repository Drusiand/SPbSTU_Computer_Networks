import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
from gbn import *
from srp import *
from utils import MessageQueue

send_msg_queue = MessageQueue()
answer_msg_queue = MessageQueue()

posted_msgs = []
received_msgs = []


def losing_test():
    global send_msg_queue
    global answer_msg_queue
    global posted_msgs
    global received_msgs

    window_size = 3
    timeout = 0.2
    max_number = 100
    loss_probability_arr = np.linspace(0, 0.9, 9)
    protocol_arr = ["GBN", "SRP"]

    print("p    | GBN             |SRP")
    print("     | t     |k        |t    |  k")

    gbn_time = []
    srp_time = []
    gbn_k = []
    srp_k = []
    for p in loss_probability_arr:
        table_row = f"{p:.1f}\t"
        send_msg_queue = MessageQueue(p)
        answer_msg_queue = MessageQueue(p)
        posted_msgs = []
        received_msgs = []

        for protocol in protocol_arr:
            if protocol == "GBN":
                sender_th = Thread(target=GBN_sender, args=(window_size, max_number, timeout,
                                                            answer_msg_queue, send_msg_queue, posted_msgs))
                receiver_th = Thread(target=GBN_receiver, args=(window_size, send_msg_queue,
                                                                answer_msg_queue, received_msgs))
            elif protocol == "SRP":
                sender_th = Thread(target=SRP_sender, args=(window_size, max_number, timeout,
                                                            answer_msg_queue, send_msg_queue, posted_msgs))
                receiver_th = Thread(target=SRP_receiver, args=(send_msg_queue, answer_msg_queue, received_msgs))

            timer_start = time.time()
            sender_th.start()
            receiver_th.start()

            sender_th.join()
            receiver_th.join()
            timer_end = time.time()

            k = len(received_msgs) / len(posted_msgs)
            elapsed = timer_end - timer_start

            table_row += f" | {elapsed:2.2f}  | {k:.2f}   "
            if protocol == "GBN":
                gbn_time.append(elapsed)
                gbn_k.append(k)
            else:
                srp_time.append(elapsed)
                srp_k.append(k)

        print(table_row)

    fig, ax = plt.subplots()
    ax.plot(loss_probability_arr, gbn_k, label="Go-Back-N")
    ax.plot(loss_probability_arr, srp_k, label="Selective repeat")
    ax.set_xlabel('вероятность потери пакета')
    ax.set_ylabel('коэф. эффективности')
    ax.legend()
    ax.grid()
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(loss_probability_arr, gbn_time, label="Go-Back-N")
    ax.plot(loss_probability_arr, srp_time, label="Selective repeat")
    ax.set_xlabel('вероятность потери пакета')
    ax.set_ylabel('время передачи, с')
    ax.legend()
    ax.grid()
    fig.show()

    print("p")
    print(loss_probability_arr)
    print("GBN")
    print(gbn_time)
    print("time")
    print("k")
    print(gbn_k)

    print("SRP")
    print(srp_time)
    print("time")
    print("k")
    print(srp_k)


def window_test():
    global send_msg_queue
    global answer_msg_queue
    global posted_msgs
    global received_msgs

    window_size_arr = range(2, 11)
    timeout = 0.2
    max_number = 100
    loss_probability_arr = 0.2
    send_msg_queue = MessageQueue(loss_probability_arr)
    answer_msg_queue = MessageQueue(loss_probability_arr)
    protocol_arr = ["GBN", "SRP"]

    print("w    | GBN             |SRP")
    print("     | t     |k        |t    |  k")

    gbn_time = []
    srp_time = []
    gbn_k = []
    srp_k = []
    for window_size in window_size_arr:
        table_row = f"{window_size:}\t"

        posted_msgs = []
        received_msgs = []

        for protocol in protocol_arr:
            if protocol == "GBN":
                sender_th = Thread(target=GBN_sender, args=(window_size, max_number, timeout,
                                                            answer_msg_queue, send_msg_queue, posted_msgs))
                receiver_th = Thread(target=GBN_receiver, args=(window_size, send_msg_queue,
                                                                answer_msg_queue, received_msgs))
            elif protocol == "SRP":
                sender_th = Thread(target=SRP_sender, args=(window_size, max_number, timeout,
                                                            answer_msg_queue, send_msg_queue, posted_msgs))
                receiver_th = Thread(target=SRP_receiver, args=(send_msg_queue, answer_msg_queue, received_msgs))

            timer_start = time.time()
            sender_th.start()
            receiver_th.start()

            sender_th.join()
            receiver_th.join()
            timer_end = time.time()

            k = len(received_msgs) / len(posted_msgs)
            elapsed = timer_end - timer_start

            table_row += f" | {elapsed:2.2f}  | {k:.2f}   "
            if protocol == "GBN":
                gbn_time.append(elapsed)
                gbn_k.append(k)
            else:
                srp_time.append(elapsed)
                srp_k.append(k)

        print(table_row)

    fig, ax = plt.subplots()
    ax.plot(window_size_arr, gbn_k, label="Go-Back-N")
    ax.plot(window_size_arr, srp_k, label="Selective repeat")
    ax.set_xlabel('размер окна')
    ax.set_ylabel('коэф. эффективности')
    ax.legend()
    ax.grid()
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(window_size_arr, gbn_time, label="Go-Back-N")
    ax.plot(window_size_arr, srp_time, label="Selective repeat")
    ax.set_xlabel('размер окна')
    ax.set_ylabel('время передачи, с')
    ax.legend()
    ax.grid()
    fig.show()

    print("w")
    print(window_size_arr)
    print("GBN")
    print(gbn_time)
    print("time")
    print("k")
    print(gbn_k)

    print("SRP")
    print(srp_time)
    print("time")
    print("k")
    print(srp_k)


def main():
    global send_msg_queue
    global answer_msg_queue

    window_size = 2
    max_number = 100
    timeout = 0.5
    loss_probability = 0.3
    protocol = "GBN"
    send_msg_queue = MessageQueue(loss_probability)
    answer_msg_queue = MessageQueue(loss_probability)

    for p in np.linspace(0, 1, 10):
        window_size = 3

    if protocol == "GBN":
        sender_th = Thread(target=GBN_sender, args=(window_size, max_number, timeout,
                                                    answer_msg_queue, send_msg_queue, posted_msgs))
        receiver_th = Thread(target=GBN_receiver, args=(window_size, send_msg_queue,
                                                        answer_msg_queue, received_msgs))
    elif protocol == "SRP":
        sender_th = Thread(target=SRP_sender, args=(window_size, max_number, timeout,
                                                    answer_msg_queue, send_msg_queue, posted_msgs))
        receiver_th = Thread(target=SRP_receiver, args=(send_msg_queue, answer_msg_queue, received_msgs))
    else:
        print("unknown protocol: ", protocol)
        return

    sender_th.start()
    receiver_th.start()

    sender_th.join()
    receiver_th.join()

    print(f"posted ({len(posted_msgs)}): \t", posted_msgs)
    print(f"received ({len(received_msgs)}):\t", received_msgs)


if __name__ == '__main__':
    # print("------------------------------------------")
    # print("losing")
    # print("------------------------------------------")
    # losing_test()

    print("------------------------------------------")
    print("window")
    print("------------------------------------------")
    window_test()

    plt.show()
