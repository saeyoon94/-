import random, math
from scipy.stats import norm
import xlsxwriter

WARM_UP_TIME = 900
sim_time = 0
total_queue = 0
total_delayTime = 0
max_time_sys = 0
total_time_sys = 0
next_event_type = 0
server1 = 0
server2 = 0
server3 = 0
time_in_system = []
time_last_event = 0
time_in_queue = []  # q에서 딜레이 시간들의 리스트
area_num_in_q = 0  # q 밑에 넓이
area_num_in_elv = [0, 0, 0]  # 엘베 밑의 넓이 0번은 1번것, 1번은 2번것, 2번은 3번 것.
area_elv_status = [0, 0, 0]  # 엘베 가동률
MOVING_TIME = 5
TIME_GATE_OPEN = 9  # 열리는 시간, 열려있는 시간, 닫히는 시간
MEAN_INTERARRIVAL = 30
END_TIME = 1800
FLOOR_PROB = [0.004, 0.099, 0.385, 0.396, 1]
POLICY = [[[1,2,3,4,5,6], [1,2,3,4,5,6], [1, 2, 3, 4, 5, 6]], [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 4,6]],
          [[1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6],[1,6]],[[1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6],[1,4,6]]
          ,[[1, 2, 3, 4, 5, 6],[1,3,5],[1,2,4,6]],[[1, 2, 3, 4, 5, 6],[1,3,5,6],[1,4,6]],[[1, 2, 3, 4, 5, 6],[1,3,4,5],[1,6]]
          ,[[1, 2, 3, 4, 5, 6],[1,4,6],[1,4,6]],[[1, 2, 3, 4, 5, 6],[1,6],[1,6]],[[1, 2, 3, 4, 5, 6],[1,3,4,5,6],[1,6]]]  # (인풋으로 받아야 함)
POLICY_NUM = 1
# 추가해야할 전역 변수 : 정책 리스트

# 이중 리스트로 학생을 추가하며 [[시간,층]] 으로 구성한다.
queue = []
# 이벤트 객체로 구성된 리스트
event_list = []
# 서버 객체로 된 리스트
server_list = []


class Server:
    def __init__(self, can_move_floor):
        self.can_move_floor = can_move_floor  # 이동할 수 있는 층을 리스트로 전달
        self.current_floor = 1  # 현재 층의 정보
        self.activation = 0  # 엘리베이터의 작동 여부
        self.switch_on = 0  # 스위치의 눌림 여부
        self.student_list = []


class Event:
    def __init__(self, type, invoke_time, elevator_num=1000, want_floor=1000):
        self.type = type  # 이벤트 타입
        self.invoke_time = invoke_time  # 발생 시간
        self.elevator_num = elevator_num  # 엘리베이터 번호
        self.want_floor = want_floor  # 내리고 싶은 층


def main():
    global sim_time
    global END_TIME
    global next_event_type
    # input값 받기
    # input값 쓰기
    for a in range(40):

        for i in POLICY:
            random.seed(44+a)
            initialize(i)  # i는 n번째 정책들
            while sim_time <= END_TIME:
                timing()
                update_time_avg_stats()

                if next_event_type.type == 1:
                    arrival()
                elif next_event_type.type == 2:
                    board()
                elif next_event_type.type == 3:
                    unboard()
                elif next_event_type.type == 4:
                    push_switch()
                elif next_event_type.type == 5:
                    end_warm_up()
            report()
        print(a+1,'번 째 입니다.')


def timing():
    global event_list
    global next_event_type
    global sim_time
    next_time = 999999  # 다음 시작할 event 발생 시간
    next_id = 1000
    for num_list, event_in_list in enumerate(event_list):
        if (event_in_list.invoke_time < next_time):
            next_time = event_in_list.invoke_time
            next_id = num_list
    next_event_type = event_list.pop(next_id)
    sim_time = next_time


def congestion():
     return math.e ** (1.0261 * norm.ppf(random.random()) + 0.71803)


def noncongestion():
    return 0.17606 + 11.329 * (math.log(1 / random.random()) ** (1 / 1.0981))


def initialize(i):
    global sim_time
    global total_queue
    global total_delayTime
    global max_time_sys
    global total_time_sys
    global server1
    global server2
    global server3
    global event_list
    global WARM_UP_TIME
    global END_TIME
    global time_last_event
    global queue
    global server_list
    global area_num_in_elv
    global area_elv_status
    global time_in_system
    global time_in_queue

    sim_time = 0
    time_last_event = 0
    server1 = Server(i[0])
    server2 = Server(i[1])
    server3 = Server(i[2])
    total_queue = 0
    total_delayTime = 0
    max_time_sys = 0
    total_time_sys = 0
    queue = []
    event_list = []
    server_list = [server1, server2, server3]
    area_num_in_elv = [0, 0, 0]
    area_elv_status = [0, 0, 0]
    time_in_system = []
    time_in_queue = []

    event_list.append(Event(1, sim_time + noncongestion()))
    event_list.append(Event(5, WARM_UP_TIME, 1000, 1000))
    # event_list.append(Event(5, END_TIME, 1000, 1000))
    # 초기에 발생시켜야 하는 arrival event와 end_sumulation event 발생

def random_integer():
    global FLOOR_PROB
    u = random.random()
    for d, prob in enumerate(FLOOR_PROB):
        if (u < prob):
            return d + 2


def arrival():
    global queue
    global sim_time
    global event_list
    global server1
    global server2
    global server3
    global server_list
    global WARM_UP_TIME
    switch_list = []
    student_want_floor = random_integer()  # 가고 싶은 층
    student = [sim_time, student_want_floor]  # 시간, 가고 싶은 층으로 만든 학생 리스트
    queue.append(student)  # 큐에 추가
    for num_server, i in enumerate(server_list):
        if student[1] in i.can_move_floor:
            if i.switch_on == 0:
                switch_list.append(num_server)
    if switch_list != [] :
        switch_click = Event(4, sim_time + 0.1, switch_list)
        event_list.append(switch_click)

    if sim_time > WARM_UP_TIME:
        student_arrive_time = sim_time + congestion()  # 다음 고객의 도착 시간
    else:
        student_arrive_time = sim_time + noncongestion()

    event_arrive = Event(1, student_arrive_time)  # 다음 도착 이벤트
    event_list.append(event_arrive)  # 이벤트 리스트에 추가


def push_switch():
    global next_event_type
    global server_list
    global MOVING_TIME
    global TIME_GATE_OPEN
    global event_list
    pushed_switch = next_event_type.elevator_num
    for i in pushed_switch:
        n = 0
        server_list[i].switch_on = 1
        t=0
        time_down_to=0
        if server_list[i].activation == 0:
            time_down_to = calculateMovingTime(server_list[i].current_floor - 1) + TIME_GATE_OPEN
            server_list[i].activation = 1
        else:
            for j in event_list:
                if j.type == 3 and j.elevator_num == i:
                    if n < j.want_floor:
                        n = j.want_floor
                    time_down_to = calculateMovingTime(n-server_list[i].current_floor) + TIME_GATE_OPEN + calculateMovingTime(n - 1)

        event_list.append(Event(2, sim_time + time_down_to, i))


def calculateMovingTime(difference):
    if (difference == 0):
        return 0
    movingTimelist = [8, 10, 11.5, 13, 14.5]
    return movingTimelist[difference - 1]






# 내려오는거 계산할 때 중간중간 멈췄을 때 시간도 고려해아 될 거 같음
def board():
    global next_event_type
    global server_list
    global queue
    global sim_time
    global event_list
    global time_in_queue
    unboardlist = []
    server_board = server_list[next_event_type.elevator_num]
    server_board.current_floor = 1
    server_board.switch_on = 0
    for student_board in queue:
        if student_board[1] in server_board.can_move_floor:
            server_board.student_list.append(student_board)
            delay_in_queue = sim_time - student_board[0]
            time_in_queue.append(delay_in_queue)
            # 그 후 학생을 제거
            queue.remove(student_board)
        if len(server_board.student_list) == 12:
            break
    # 탄 학생이 있다면
    if len(server_board.student_list) > 0:
        # 내리는 학생이 있는 층 정보 만들기
        for student_in_server in server_board.student_list:
            if student_in_server[1] in unboardlist:
                continue
            else:
                unboardlist.append(student_in_server[1])
        # 내리는 이벤트 만들기
        unboardlist.sort()
        # 문이 열리는 횟수(0부터 시작함으로 1을 더해서 계산), 내리는 층
        last_unboard = 1
        last_time = 0
        for stop_unboard, unboard_floor in enumerate(unboardlist):
            # 위로 올라가는 시간
            time_up_to = sim_time + last_time + calculateMovingTime(unboard_floor - last_unboard) + TIME_GATE_OPEN * (stop_unboard + 1)
            last_unboard = unboard_floor
            last_time += time_up_to - sim_time
            if len(queue) > 10 :
                lag = 1 + 2*random.random() # 줄에 사람이 많으면 1~3초 추가
            else :
                lag = random.random() #사람이 적으면 0~1초 추가
            unboard_event = Event(3, time_up_to + lag, next_event_type.elevator_num, unboard_floor)
            event_list.append(unboard_event)
    # 내리려는 학생이 없다면
    else:
        server_board.activation = 0
# 내려오는거 계산할 때 중간중간 멈췄을 때 시간도 고려해아 될 거 같음

# 내리는 이벤트
def unboard():
    global next_event_type
    global server_list
    global queue
    global sim_time
    global event_list
    global server_time
    global time_in_system
    server_unboard = server_list[next_event_type.elevator_num]
    unboard_floor = next_event_type.want_floor
    for unboard_student in server_unboard.student_list:
        if (unboard_student[1] == unboard_floor):
            time_in_system.append(sim_time - unboard_student[0])
            server_unboard.student_list.remove(unboard_student)
            server_list[next_event_type.elevator_num].current_floor = unboard_floor
    if len(server_unboard.student_list) == 0:
        if server_unboard.switch_on == 0:
            server_unboard.activation = 0


def update_time_avg_stats():
    global time_last_event
    global queue
    global area_num_in_q
    global area_num_in_elv
    global area_elv_status
    global sim_time
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time
    area_num_in_q += len(queue) * time_since_last_event
    for i, server in enumerate(server_list):
        area_num_in_elv[i] += len(server.student_list) * time_since_last_event
        area_elv_status[i] += server.activation * time_since_last_event


def report():
    global time_in_system
    global time_in_queue
    global sim_time
    global area_num_in_q
    global area_elv_status
    global area_num_in_elv
    global WARM_UP_TIME
    # 1 '평균 시스템 내 머문 시간은 : '  2 '시스템 내 머문 최대 시간은 : ' '3 최대 큐 대기 시간은 : '4'평균 큐 길이는 : ' +
    # 5. '서버' + str(i + 1) + '의 평균 탑승 인원수는 : ' + '6 서버' + str(i + 1) + '의 평균 가동률은 : ' +
    total_time_in_system = sum(time_in_system)
    total_time_in_queue = sum(time_in_queue)
    print(str(total_time_in_queue / len(time_in_queue)))
    print(str(max((time_in_system))))
    print(str(max(time_in_queue)))
    print(str(area_num_in_q / (sim_time - WARM_UP_TIME)))
    for i in range(3):
        print( str(area_num_in_elv[i] / (sim_time - WARM_UP_TIME)))
        print( str(area_elv_status[i] / (sim_time - WARM_UP_TIME)))
    print('////////////////////////////////////////////////////////////')
    #     #     # Area 들 출력해야 됨
    with xlsxwriter.Workbook('simul.xlsx') as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 2, "시스템 내 평균 대기 시간")
        worksheet.write(0, 3, "시스템 내 최대 대기")
        worksheet.write(0, 4, "평균 큐 대기시간")
        worksheet.write(0, 5, "최대 큐 대기시간")
        worksheet.write(0, 6, "평균 큐 인원")
        worksheet.write(0, 7, "엘베1 평균 탑승")
        worksheet.write(0, 8, "엘베2 평균 탑승")
        worksheet.write(0, 9, "엘베3 평균 탑승")
        worksheet.write(0, 10, "엘베1 평균 이용율")
        worksheet.write(0, 11, "엘베2 평균 이용율")
        worksheet.write(0, 12, "엘베3 평균 이용율")
        worksheet.write(0, 13, "이용한 고객")
        #     # 1 정보를 바꿔가면서 기록 하면 될 듯 정책 정보도 추가해야함
        worksheet.write(POLICY_NUM, 1, str(POLICY[POLICY_NUM-1]))
        worksheet.write(POLICY_NUM, 2, str(total_time_in_system / len(time_in_system)))
        worksheet.write(POLICY_NUM, 3, str(max((time_in_system))))
        worksheet.write(POLICY_NUM, 4, str(total_time_in_queue / len(time_in_queue)))
        worksheet.write(POLICY_NUM, 5, str(max(time_in_queue)))
        worksheet.write(POLICY_NUM, 6, str(area_num_in_q / sim_time))
        worksheet.write(POLICY_NUM, 7, str(area_num_in_elv[0] / sim_time))
        worksheet.write(POLICY_NUM, 8, str(area_num_in_elv[1] / sim_time))
        worksheet.write(POLICY_NUM, 9, str(area_num_in_elv[2] / sim_time))
        worksheet.write(POLICY_NUM, 10, str(area_elv_status[0] / sim_time))
        worksheet.write(POLICY_NUM, 11, str(area_elv_status[1] / sim_time))
        worksheet.write(POLICY_NUM, 12, str(area_elv_status[2] / sim_time))
        worksheet.write(POLICY_NUM, 13, len(time_in_system))


def end_warm_up():
    global time_in_system
    global time_in_queue
    global sim_time
    global area_num_in_q
    global area_elv_status
    global area_num_in_elv
    time_in_system = []
    time_in_queue = []
    area_num_in_q = 0
    area_elv_status = [0, 0, 0]
    area_num_in_elv = [0, 0, 0]



main()