# @Time : 2019/12/12 15:02 
# @Author : Junjie He

import random


class PCB:
    page_number = 0
    list_page = list()

    def __init__(self, id, arrive_time=1, serve_time=1, priority=1):
        self.id = id
        self.arrive_time = arrive_time
        self.serve_time = serve_time
        self.priority = priority
        self.list_save = []
        self.list_page = []
        for i in range(serve_time):
            r = random.randint(1, 10)
            s = random.randint(1, 200)
            for j in range(len(self.list_page)):
                if s == self.list_page[j]:
                    s = random.randint(1, 200)

            self.list_page.append(r)

    def run(self):
        print(self.id + "正在运行！")
        self.serve_time -= 1


# 按照到达时间进行排序
def sort(list_arrive):
    for i in range(len(list_arrive) - 1):
        for j in range(i + 1, len(list_arrive)):
            if list_arrive[i].arrive_time > list_arrive[j].arrive_time:
                list_arrive[i], list_arrive[j] = list_arrive[j], list_arrive[i]
    return list_arrive


if __name__ == "__main__":
    n = int(input("请输入进程数："))
    list1 = []
    id = 1
    # list4 = []
    for i in range(n):
        a = int(input("请输入第" + str(id) + "个进程的到达时间："))
        b = int(input("请输入第" + str(id) + "个进程的服务时间："))
        print()
        name = "进程" + str(id)
        list1.append(PCB(name, a, b))
        id += 1
        # print(PCB(name, a, b).list_page)
    sort(list1)
    # for i in range(len(list1)):
    #     print(list1[i].id)
    real_time = 0
    list2 = []
    while 1:
        print("时间：", real_time)
        if list1:
            # 当进程到达时间相同时还需进行改善
            for i in range(len(list1)):
                if real_time == list1[0].arrive_time:
                    list2.append(list1[0])
                    list1.remove(list1[0])

        # 当进程的服务时间为0时，进程退出
        if list2:
            if len(list2) == 1 and list1 == []:
                if list2[0].serve_time == 0:
                    print(list2[0].id, "运行结束。    所有进程运行结束")
                    break
            if list2[0].serve_time == 0:
                print(list2[0].id, "运行结束")
                list2.remove(list2[0])
                continue
            pid = list2[0].id
        # 按照高响应比作为优先级进行排序
        for i in range(len(list2) - 1):
            for j in range(i + 1, len(list2)):
                if list2[i].priority < list2[j].priority:
                    list2[i], list2[j] = list2[j], list2[i]
        # 运行就绪队列的进程
        if list2:
            print("当前已有" + str(len(list2)) + "个进程到达。")
            if pid != list2[0].id:
                print(list2[0].id + "抢占了" + pid)
            list4 = list2[0].list_save
            print("到达进程的优先级分别为：")
            for i in range(len(list2)):
                print("  ", list2[i].id + "的优先级为：", list2[i].priority)
            list2[0].run()
            # 查看进程的请求页面时是所有进程的页面，改成该进程的页面
            print(list2[0].id, "访问的页面的页面序号为：", list2[0].list_page)
            print(list2[0].id, "本次访问的页面号为：", list2[0].list_page[0])
            # list4 = list2[0].list_save
            if list4:
                if len(list4) == 5:
                    state_1 = True
                    for h in range(len(list4)):
                        if list2[0].list_page[0] == list4[h]:
                            for n in range(h, 0, -1):
                                list4[n], list4[n - 1] = list4[n - 1], list4[n]
                            list2[0].list_page.remove(list2[0].list_page[0])
                            state_1 = False
                            break
                    if state_1:
                        pre_lasted = list4[4]
                        list4[4] = list2[0].list_page[0]
                        for m in range(4, 0, -1):
                            list4[m], list4[m - 1] = list4[m - 1], list4[m]
                        print("发生了缺页中断，页面" + str(pre_lasted) + "是最近最久未被访问的页，被置换出去")
                        list2[0].list_page.remove(list2[0].list_page[0])
                    print("栈中的页面号为：", list4)
                if len(list4) < 5:
                    state_2 = True
                    for j in range(len(list4)):
                        if list2[0].list_page[0] == list4[j]:
                            for n in range(j, 0, -1):
                                list4[n], list4[n - 1] = list4[n - 1], list4[n]
                            list2[0].list_page.remove(list2[0].list_page[0])
                            state_2 = False
                            break
                    if state_2:
                        list4.append(list2[0].list_page[0])
                        for n in range(len(list4) - 1, 0, -1):
                            list4[n], list4[n - 1] = list4[n - 1], list4[n]
                        list2[0].list_page.remove(list2[0].list_page[0])
                    print("栈中的页面号为：", list4)
            if not list4:
                list4.append(list2[0].list_page[0])
                list2[0].list_page.remove(list2[0].list_page[0])
                print("栈中的页面号为：", list4)
        if len(list2) >= 2:
            for i in range(1, len(list2)):
                list2[i].priority = (real_time - list2[i].arrive_time + list2[i].serve_time) / list2[i].serve_time
        # 当就绪队列和所有进程队列中都为空时，结束
        # if list1 == [] and list2 == []:
        #     print("\n所有进程运行结束！")
        #     break
        # 时间+1
        real_time += 1
        print("-------------------------------------------------------------------------")
