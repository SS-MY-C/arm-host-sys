import os
import threading  # 多线程库
import time  # 时间库
from time import sleep
import serial  # 串口通讯库 备注:pyserial库不是serial库
import serial.tools.list_ports  # 查看所有com口库
from PySide2.QtWidgets import QApplication, QMessageBox,QMainWindow,QPushButton,QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import  QIcon
from PySide2.QtCore import QTimer
import config
import PyHook3 as pyHook
import pythoncom

envpath = r'G:\python\Lib\site-packages\PySide2\plugins\platforms'
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = envpath

#class Config(object):
#    def __init__(self):
#        _moter_state = "no"

mousedown = 0
motor1 = 0
_moter1_data = ""
_moter2_data = ""
_moter3_data = ""
_moter4_data = ""
_moter5_data = ""
_moter6_data = ""

class Interface(object):
    def __init__(self):
        super().__init__()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = QUiLoader().load('second.ui')

        #控制界面将connectCom函数跟连接按钮绑定,连接机械臂
        self.ui.pushButtonConnect.clicked.connect(self.connectCom)
        # 控制界面将connectCom函数跟连接按钮绑定，断开机械臂
        self.ui.pushButtonClose.clicked.connect(self.connectClose)
        #电机加速度+ - 确定
        self.ui.pushButton_15.clicked.connect(self.accelerateAdd)
        self.ui.pushButton_16.clicked.connect(self.accelerateReduce)
        self.ui.pushButton_3.clicked.connect(self.accConfirm)
        #电机行程大中小 2000 500 100
        self.ui.pushButton_11.clicked.connect(self.motorTravelBig)
        self.ui.pushButton_12.clicked.connect(self.motorTravelMid)
        self.ui.pushButton_13.clicked.connect(self.motorTravelSml)
        #1轴电机 +
        self.ui.pushButton_17.clicked.connect(self.motor1Add)
        # 1轴电机 -
        self.ui.pushButton_18.clicked.connect(self.motor1Red)
        # 1轴电机 确定
        self.ui.pushButton_19.clicked.connect(self.motor1Confirm)
        #2轴电机 +
        self.ui.pushButton_7.clicked.connect(self.motor2Add)
        # 2轴电机 -
        self.ui.pushButton_8.clicked.connect(self.motor2Red)
        # 2轴电机确定按钮
        self.ui.pushButton_5.clicked.connect(self.motor2Confirm)
        # 3轴电机 +
        self.ui.pushButton_9.clicked.connect(self.motor3Add)
        # 3轴电机 -
        self.ui.pushButton_10.clicked.connect(self.motor3Red)
        # 3轴电机确定按钮
        self.ui.pushButton_6.clicked.connect(self.motor3Confirm)
        # 4轴电机 +
        self.ui.pushButton_20.clicked.connect(self.motor4Add)
        # 4轴电机 -
        self.ui.pushButton_23.clicked.connect(self.motor4Red)
        # 4轴电机确定按钮
        self.ui.pushButton_26.clicked.connect(self.motor4Confirm)
        # 5轴电机 +
        self.ui.pushButton_21.clicked.connect(self.motor5Add)
        # 5轴电机 -
        self.ui.pushButton_24.clicked.connect(self.motor5Red)
        # 5轴电机确定按钮
        self.ui.pushButton_27.clicked.connect(self.motor5Confirm)
        # 6轴电机 +
        self.ui.pushButton_22.clicked.connect(self.motor6Add)
        # 6轴电机 -
        self.ui.pushButton_25.clicked.connect(self.motor6Red)
        # 6轴电机确定按钮
        self.ui.pushButton_28.clicked.connect(self.motor6Confirm)
        #home 点
        self.ui.pushButton_48.clicked.connect(self.runHome1)
        #工作的
        self.ui.pushButton_58.clicked.connect(self.workPosition)
        #输入指令发送绑定
        self.ui.pushButton_14.clicked.connect(self.sendControl)

        #写入位置到面板按钮
        self.ui.pushButton_47.clicked.connect(self.writeCommand)
        #记录位置一
        self.ui.pushButton_29.clicked.connect(self.recPosition1)
        #记录位置二
        self.ui.pushButton_30.clicked.connect(self.recPosition2)
        # 记录位置三
        self.ui.pushButton_31.clicked.connect(self.recPosition3)
        # 记录位置四
        self.ui.pushButton_32.clicked.connect(self.recPosition4)
        # 记录位置五
        self.ui.pushButton_33.clicked.connect(self.recPosition5)
        #记录位置六
        self.ui.pushButton_34.clicked.connect(self.recPosition6)

        #写入位置一
        self.ui.pushButton_50.clicked.connect(self.wriPosition1)
        # 写入位置2
        self.ui.pushButton_51.clicked.connect(self.wriPosition2)
        # 写入位置3
        self.ui.pushButton_52.clicked.connect(self.wriPosition3)
        # 写入位置4
        self.ui.pushButton_53.clicked.connect(self.wriPosition4)
        # 写入位置5
        self.ui.pushButton_54.clicked.connect(self.wriPosition5)
        # 写入位置6
        self.ui.pushButton_55.clicked.connect(self.wriPosition6)
        #取消位置一
        self.ui.pushButton_35.clicked.connect(self.delPosition1)
        # 取消位置一
        self.ui.pushButton_36.clicked.connect(self.delPosition2)
        # 取消位置一
        self.ui.pushButton_37.clicked.connect(self.delPosition3)
        # 取消位置一
        self.ui.pushButton_38.clicked.connect(self.delPosition4)
        # 取消位置一
        self.ui.pushButton_39.clicked.connect(self.delPosition5)
        # 取消位置一
        self.ui.pushButton_40.clicked.connect(self.delPosition6)

        #运行位置一
        self.ui.pushButton_41.clicked.connect(self.runPosision1)
        # 运行位置2
        self.ui.pushButton_42.clicked.connect(self.runPosision2)
        # 运行位置3
        self.ui.pushButton_43.clicked.connect(self.runPosision3)
        # 运行位置4
        self.ui.pushButton_44.clicked.connect(self.runPosision4)
        # 运行位置5
        self.ui.pushButton_45.clicked.connect(self.runPosision5)
        # 运行位置6
        self.ui.pushButton_46.clicked.connect(self.runPosision6)
        #执行面板多行指令
        self.ui.pushButton_49.clicked.connect(self.runExecute_thread)
        #情空面板
        self.ui.pushButton_56.clicked.connect(self.clearBoard)
        #刷新主页面步进值
        self.ui.pushButton_57.clicked.connect(self.ref)

        #一轴正转动
        self.ui.pushButton.clicked.connect(self.run_thread1)
        #一轴反转
        self.ui.pushButton_59.clicked.connect(self.nirun_thread1)
        # 停止
        self.ui.pushButton_2.clicked.connect(self.stop_thread1)
        #二轴正转
        self.ui.pushButton_66.clicked.connect(self.run_thread2)
        # 二轴反转
        self.ui.pushButton_67.clicked.connect(self.nirun_thread2)
        #2tingzhi
        self.ui.pushButton_68.clicked.connect(self.stop_thread2)
        # 3轴正转
        self.ui.pushButton_60.clicked.connect(self.run_thread3)
        # 3轴反转
        self.ui.pushButton_61.clicked.connect(self.nirun_thread3)
        # 3tingzhi
        self.ui.pushButton_62.clicked.connect(self.stop_thread3)
        # 4轴正转
        self.ui.pushButton_69.clicked.connect(self.run_thread4)
        # 4轴反转
        self.ui.pushButton_70.clicked.connect(self.nirun_thread4)
        # 4tingzhi
        self.ui.pushButton_71.clicked.connect(self.stop_thread4)
        # 5轴正转
        self.ui.pushButton_63.clicked.connect(self.run_thread5)
        # 5轴反转
        self.ui.pushButton_64.clicked.connect(self.nirun_thread5)
        # 5tingzhi
        self.ui.pushButton_65.clicked.connect(self.stop_thread5)
        # 6轴正转
        self.ui.pushButton_72.clicked.connect(self.run_thread6)
        # 6轴反转
        self.ui.pushButton_73.clicked.connect(self.nirun_thread6)
        # 6tingzhi
        self.ui.pushButton_74.clicked.connect(self.stop_thread6)

    # 串口接收单片机数据，判断是否需要发送指令
    def uart_recv_thread(self):
        #循环
        while True:
            try:
                #按行读取串口数据 readline读取数据包括 \n 字符
                data = self.uart.readline()
                # 发送数据需要 encode编码，接收数据需要decode解码
                # 将readline读取到的 \n 字符串替换为空字符
                data = data.decode().replace("\n", "")
                #打印接受的数据
                print("Arduino发送:", data)
                # 界面写入日志
                self.ui.plainTextEdit_py.insertPlainText(str(data) + '\n')

                global _moter1_data
                global _moter2_data
                global _moter3_data
                global _moter4_data
                global _moter5_data
                global _moter6_data
                # 每发送6个指令会询问Arduino当前电机是否静止状态
                # 判断串口收到的字符串是否包含 yes 用于是否继续发送G指令代码
                # readline()函数串口接收的数据是读一行 字符串末尾自动添加\r\n隐形字符 使用逗号切割字符串才能看见
                # Arduino发送来的yes会产生5个字符 yes/r/n
                if "yes" in data:
                   config._moter_state = "yes"

                # 判断串口收到的字符串是否包含 sign
                if "sign" in data:
                    # 字符串剔除多余字符 字母 空格符合 换行符合
                    # readline()串口接收的数据末尾自动添加\r\n隐形字符
                    g_code_str = data.replace("sign,", "").replace("\r", "").replace("\n", "").replace("--", "")
                    g_code_list = g_code_str.split(",")  # 字符串通过逗号切割成列表类型

                    # 刷新界面电机步进值 遍历列表提前指令关键字 将replace剔除关键字后数值写入界面
                    for i in g_code_list:
                        if i.find("MA") == 0:
                            _moter1_data = i.replace('MA', '', )
                            self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                        elif i.find("MB") == 0:
                            _moter2_data = i.replace('MB', '', )
                            self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                        elif i.find("MC") == 0:
                            _moter3_data = i.replace('MC', '', )
                            self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                        elif i.find("MD") == 0:
                            _moter4_data = i.replace('MD', '', )
                            self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                        elif i.find("ME") == 0:
                            _moter5_data =  i.replace('ME', '', )
                            self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                        elif i.find("MF") == 0:
                            _moter6_data = i.replace('MF', '', )
                            self.ui.lineEdit_8.setText(i.replace('MF', '', ))

            except Exception as e:
                print("接收Arduino数据函数异常!")
                self.ui.plainTextEdit_py.insertPlainText("接收Arduino数据函数异常!" + '\n')  # ui界面多行文本编辑框插入python日志
                return None
    #接收数据改为多线程
    def run(self):
        # 接收数据函数封装成多线程 参数作用:主线程退出后多线程也退出 防止僵尸线程
        thread = threading.Thread(target=self.uart_recv_thread, daemon=True)
        # 启动接收数据多线程
        thread.start()

    #连接机械臂
    def connectCom(self):
        #获取控制器界面的com参数
        com = self.ui.comboBox_com.currentText()
        #获取控制器界面的波特率值
        baud = self.ui.comboBox_baud.currentText()
        try:
            #连接串口
            self.uart = serial.Serial(com, baud)
            #连接成功写入日志
            self.ui.plainTextEdit_py.insertPlainText("串口连接成功!" + '\n')
            self.run()
            self.ui.plainTextEdit_py.insertPlainText("接收Arduino返回数据多线程开启!" + '\n')
            data01 = "Mo"
            # 串口指令写入
            self.uart.write(data01.encode())
            self.ui.plainTextEdit.setPlainText("机械臂连接成功" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText("界面连接设备函数异常!" + '\n')

    #断开机械臂连接
    def connectClose(self):
        try:
            #串口关闭
            self.uart.close()
            #写入日志
            self.ui.plainTextEdit_py.insertPlainText("关闭串口连接!" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText("界面断开按钮函数异常!!" + '\n')
    #刷新步进值
    def ref(self):
        try:
            # 刷新1-6轴步进值
            data01 = "Mo"
            self.uart.write(data01.encode())
            print("发送刷新步进电机步进值指令 ", data01)
            self.ui.plainTextEdit_py.insertPlainText("发送刷新步进电机步进值指令 " + str(data01) + '\n')  # ui界面多行文本编辑框插入python日志

        except:
            pass

    #界面控制机械臂指令发送
    def sendControl(self):
        try:
            # 获取输入框的指令
            data1 = self.ui.lineEdit_5.text()
            #串口发送，指令需要编码
            self.uart.write(data1.encode())
            #写入日志
            self.ui.plainTextEdit_py.insertPlainText("发送指令:" + str(data1) + '\n')
            #情空
            self.ui.lineEdit_5.setText('')
            # 逗号分割发送的指令 转换成列表类型
            data2 = data1.split(",")
            # 刷新界面电机步进值数值
            # 遍历列表，逐个找到对应指令前缀
            for i in data2:
                if i.find("MP") == 0:
                    # 刷新界面电机步进数值，判断前缀替换为空
                    self.ui.lineEdit.setText(i.replace('MP', '', ))
                elif i.find("MA") == 0:
                    self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                elif i.find("MB") == 0:
                    self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                elif i.find("MC") == 0:
                    self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                elif i.find("MD") == 0:
                    self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                elif i.find("ME") == 0:
                    self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                elif i.find("MF") == 0:
                    self.ui.lineEdit_8.setText(i.replace('MF', '', ))

            self.ui.plainTextEdit.insertPlainText("发送修改机械臂指令" + data1 + '\n')

        except:
            self.ui.plainTextEdit_py.insertPlainText("界面串口发送字符串函数异常!" + '\n')
    #加速度+
    def accelerateAdd(self):
        # 获取电机加速度的值
        num01 = self.ui.lineEdit.text()
        num01 = int(num01)
        # 判断加速度是否超过最大加速度
        if num01 + 500 <= 12000:
            # 未超过最大加速度则加500
            num01 += 500
            #更新输入框电机加速度
            self.ui.lineEdit.setText(str(num01))

    # 加速度-
    def accelerateReduce(self):
        #获取电机加速度的值
        num02 = self.ui.lineEdit.text()
        #字符串转整数
        num02 = int(num02)
        #判断加速度减小是否小于0
        if num02 - 500 >0 :
            #未小于0则减小
            num02 -= 500
            # 更新输入框电机加速度
            self.ui.lineEdit.setText(str(num02))
    # 加速度确认
    def accConfirm(self):
        try:
            # 获取电机加速度的值
            dataAcc = self.ui.lineEdit.text()
            # 合成指令
            dataAccS = "MP" + dataAcc
            self.uart.write(dataAccS.encode())
            self.ui.plainTextEdit_py.insertPlainText("发送修改步进电机加速度指令 = " + str(dataAccS) + '\n')
            self.ui.plainTextEdit.insertPlainText("机械臂电机加速度修改为" + dataAcc + '\n')

        except:
            self.ui.plainTextEdit_py.insertPlainText("界面电机加速度发送按钮函数异常! " + '\n')
            self.ui.plainTextEdit.insertPlainText("指令未发送! " + '\n')

    #电机行程按钮 大 设置为2000
    def motorTravelBig(self):
        self.ui.lineEdit_2.setText("2000")
        self.ui.plainTextEdit.insertPlainText("电机行程修改为2000" + '\n')

    # 电机行程按钮 中 500
    def motorTravelMid(self):
        self.ui.lineEdit_2.setText("500")
        self.ui.plainTextEdit.insertPlainText("电机行程修改为500" + '\n')

    # 电机行程按钮 小 100
    def motorTravelSml(self):
        self.ui.lineEdit_2.setText("100")
        self.ui.plainTextEdit.insertPlainText("电机行程修改为100" + '\n')

    #一轴+按钮，电机步进值+++
    def motor1Add(self):
        try:
            # 获取一轴电机步进值
            data1 = self.ui.lineEdit_6.text()
            # 获取行程
            dataTra = self.ui.lineEdit_2.text()
            # 计算电机新的步进值
            dataRun = int(data1) + int(dataTra)
            # 给定电机限位
            if dataRun >= 0 and dataRun <=20000:
                # 发送命令到单片机，合成指令代码
                dataS = "MA" + str(dataRun)
                # 串口发送指令，指令需要编码
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令'+str(dataS)+'\n')
                # 更新电机输入框的数值
                self.ui.lineEdit_6.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴一指令!" + dataS + '\n' + '轴一实时步进值为' + str(dataRun) + '\n')
            else:
                # 判断电机过限位的情况
                if dataRun > 20000:
                    # 计算电机超出限位的范围
                    num = dataRun - 20000
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun<0:
                    # 计算电机超出限位的范围
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('一轴电机值+按钮异常'+'\n')

    # 一轴-按钮，电机步进值---
    def motor1Red(self):
        try:
            # 获取一轴电机步进值
            data1 = self.ui.lineEdit_6.text()
            # 获取行程
            dataTra = self.ui.lineEdit_2.text()
            # 计算电机新的步进值
            dataRun = int(data1) - int(dataTra)
            # 给定电机限位
            if dataRun >= 0 and dataRun <=20000:
                # 发送命令到单片机，合成指令代码
                dataS = "MA" + str(dataRun)
                # 串口发送指令，指令需要编码
                self.uart.write(dataS.encode())
                # 指令发送成功写入日志
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令'+str(dataS)+'\n')
                # 更新电机输入框的数值
                self.ui.lineEdit_6.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴一指令!" + dataS + '\n' + '轴一实时步进值为' + str(dataRun) + '\n')
            else:
                # 判断电机过限位的情况
                if dataRun > 20000:
                    # 计算电机超出限位的范围
                    num = dataRun - 20000
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun<0:
                    # 计算电机超出限位的范围
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('一轴电机值-按钮异常'+'\n')

    # 一轴确认按钮，驱动电机到指定的步进值
    def motor1Confirm(self):
        try:
            # 获取输入框电机的步进值
            data = self.ui.lineEdit_6.text()
            # 合成指令
            dataS = "MA" + str(data)
            # 发送指令，指令需要编码
            self.uart.write(dataS.encode())
            self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
            self.ui.plainTextEdit.insertPlainText("发送修改轴一指令!" + dataS + '\n' + '轴一实时步进值为' + data + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('二轴电机值确定按钮异常' + '\n')

    # 二轴 + 按钮，二轴电机值++
    def motor2Add(self):
        try:
            data2 = self.ui.lineEdit_3.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data2) + int(dataTra)
            if dataRun >= 0 and dataRun <= 12800:
                dataS = "MB" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令'+str(dataS)+'\n')
                self.ui.lineEdit_3.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴二指令!" + dataS + '\n' + '轴二实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun>12800:
                    num = dataRun-12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num)+'\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun<0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('二轴电机值+按钮异常'+'\n')

    # 二轴 - 按钮，二轴电机值--
    def motor2Red(self):
        try:
            data2 = self.ui.lineEdit_3.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data2) - int(dataTra)
            if dataRun>=0 and dataRun <=12800:
                dataS = "MB" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
                self.ui.lineEdit_3.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴二指令!" + dataS + '\n' + '轴二实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun > 12800:
                    num = dataRun - 12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun < 0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('二轴电机值-按钮异常'+'\n')

    # 二轴 确认 按钮，移动到指定值
    def motor2Confirm(self):
        try:
            data = self.ui.lineEdit_3.text()
            dataS = "MB" + str(data)
            self.uart.write(dataS.encode())
            self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
            self.ui.plainTextEdit.insertPlainText("发送修改轴二指令!" + dataS + '\n' + '轴二实时步进值为' + data + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('二轴电机值确定按钮异常'+'\n')

    # 三轴 + 按钮
    def motor3Add(self):
        try:
            data3 = self.ui.lineEdit_4.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data3) + int(dataTra)
            if dataRun >= 0 and dataRun <= 12800:
                dataS = "MC" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令'+str(dataS)+'\n')
                self.ui.lineEdit_4.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴三指令!" + dataS + '\n' + '轴三实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun>12800:
                    num = dataRun-12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num)+'\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun<0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('三轴电机值+按钮异常'+'\n')

    # 三轴 - 按钮
    def motor3Red(self):
        try:
            data3 = self.ui.lineEdit_4.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data3) - int(dataTra)
            if dataRun>=0 and dataRun <=12800:
                dataS = "MC" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
                self.ui.lineEdit_4.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴三指令!" + dataS + '\n' + '轴三实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun > 12800:
                    num = dataRun - 12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun < 0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('三轴电机值-按钮异常'+'\n')

    # 三轴 确认 按钮
    def motor3Confirm(self):
        try:
            data = self.ui.lineEdit_4.text()
            dataS = "MC" + str(data)
            self.uart.write(dataS.encode())
            self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
            self.ui.plainTextEdit.insertPlainText("发送修改轴三指令!" + dataS + '\n' + '轴三实时步进值为' + data + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('三轴电机值确定按钮异常'+'\n')

    # 四轴 + 按钮
    def motor4Add(self):
        try:
            data4 = self.ui.lineEdit_7.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data4) + int(dataTra)
            if dataRun >= 0 and dataRun <= 12800:
                dataS = "MD" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令'+str(dataS)+'\n')
                self.ui.lineEdit_7.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴四指令!" + dataS + '\n' + '轴四实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun>12800:
                    num = dataRun-12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num)+'\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun<0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('四轴电机值+按钮异常'+'\n')

    # 四轴 - 按钮
    def motor4Red(self):
        try:
            data4 = self.ui.lineEdit_7.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data4) - int(dataTra)
            if dataRun>=0 and dataRun <=12800:
                dataS = "MD" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
                self.ui.lineEdit_7.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴四指令!" + dataS + '\n' + '轴四实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun > 12800:
                    num = dataRun - 12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun < 0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('四轴电机值-按钮异常'+'\n')

    # 四轴 确认 按钮
    def motor4Confirm(self):
        try:
            data = self.ui.lineEdit_7.text()
            dataS = "MD" + str(data)
            self.uart.write(dataS.encode())
            self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
            self.ui.plainTextEdit.insertPlainText("发送修改轴四指令!" + dataS + '\n' + '轴四实时步进值为' + data + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('四轴电机值确定按钮异常'+'\n')

    # 五轴 + 按钮
    def motor5Add(self):
        try:
            data5 = self.ui.lineEdit_9.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data5) + int(dataTra)
            if dataRun >= 0 and dataRun <= 12800:
                dataS = "ME" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令'+str(dataS)+'\n')
                self.ui.lineEdit_9.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴五指令!" + dataS + '\n' + '轴五实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun>12800:
                    num = dataRun-12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num)+'\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun<0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('五轴电机值+按钮异常'+'\n')

    # 五轴 - 按钮
    def motor5Red(self):
        try:
            data5 = self.ui.lineEdit_9.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data5) - int(dataTra)
            if dataRun>=0 and dataRun <=12800:
                dataS = "ME" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
                self.ui.lineEdit_9.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴五指令!" + dataS + '\n' + '轴五实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun > 12800:
                    num = dataRun - 12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun < 0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('五轴电机值-按钮异常'+'\n')

    # 五轴 确认 按钮
    def motor5Confirm(self):
        try:
            data = self.ui.lineEdit_9.text()
            dataS = "ME" + str(data)
            self.uart.write(dataS.encode())
            self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
            self.ui.plainTextEdit.insertPlainText("发送修改轴五指令!" + dataS + '\n' + '轴五实时步进值为' + data + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('五轴电机值确定按钮异常'+'\n')

    # 六轴 + 按钮
    def motor6Add(self):
        try:
            data6 = self.ui.lineEdit_8.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data6) + int(dataTra)
            if dataRun >= 0 and dataRun <= 12800:
                dataS = "MF" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令'+str(dataS)+'\n')
                self.ui.lineEdit_8.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴六指令!" + dataS + '\n' + '轴六实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun>12800:
                    num = dataRun-12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num)+'\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun<0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('六轴电机值+按钮异常'+'\n')

    # 六轴 - 按钮
    def motor6Red(self):
        try:
            data6 = self.ui.lineEdit_8.text()
            dataTra = self.ui.lineEdit_2.text()
            dataRun = int(data6) - int(dataTra)
            if dataRun>=0 and dataRun <=12800:
                dataS = "MF" + str(dataRun)
                self.uart.write(dataS.encode())
                self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
                self.ui.lineEdit_8.setText(str(dataRun))
                self.ui.plainTextEdit.insertPlainText("发送修改轴六指令!" + dataS + '\n' + '轴六实时步进值为' + str(dataRun) + '\n')
            else:
                if dataRun > 12800:
                    num = dataRun - 12800
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
                elif dataRun < 0:
                    num = abs(dataRun)
                    self.ui.plainTextEdit_py.insertPlainText('步进电机过限位小于零，超出范围' + str(num) + '\n')
                    self.ui.plainTextEdit.insertPlainText("电机运行位置异常" + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('六轴电机值-按钮异常'+'\n')

    # 六轴 确认 按钮
    def motor6Confirm(self):
        try:
            data = self.ui.lineEdit_8.text()
            dataS = "MF" + str(data)
            self.uart.write(dataS.encode())
            self.ui.plainTextEdit_py.insertPlainText('发送驱动指令' + str(dataS) + '\n')
            self.ui.plainTextEdit.insertPlainText("发送修改轴六指令!" + dataS + '\n' + '轴六实时步进值为' + data + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('六轴电机值确定按钮异常'+'\n')

    #home1 run
    def runHome1(self):
        try:
            data = config._home_data
            self.uart.write(data.encode())
            self.ui.plainTextEdit_py.insertPlainText('点击home点，机械臂运动至home点' + '\n')
            data2 = data.split(",")
            for i in data2:
                if i.find("MP") == 0:
                    # 刷新界面电机步进数值，判断前缀替换为空
                    self.ui.lineEdit.setText(i.replace('MP', '', ))
                elif i.find("MA") == 0:
                    self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                elif i.find("MB") == 0:
                    self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                elif i.find("MC") == 0:
                    self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                elif i.find("MD") == 0:
                    self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                elif i.find("ME") == 0:
                    self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                elif i.find("MF") == 0:
                    self.ui.lineEdit_8.setText(i.replace('MF', '', ))
        except:
            self.ui.plainTextEdit_py.insertPlainText('home点异常' + '\n')

    #work position
    def workPosition(self):
        try:
            data = config._work_data
            self.uart.write(data.encode())
            self.ui.plainTextEdit_py.insertPlainText('点击home点，机械臂运动至home点' + '\n')
            data2 = data.split(",")
            for i in data2:
                if i.find("MP") == 0:
                    # 刷新界面电机步进数值，判断前缀替换为空
                    self.ui.lineEdit.setText(i.replace('MP', '', ))
                elif i.find("MA") == 0:
                    self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                elif i.find("MB") == 0:
                    self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                elif i.find("MC") == 0:
                    self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                elif i.find("MD") == 0:
                    self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                elif i.find("ME") == 0:
                    self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                elif i.find("MF") == 0:
                    self.ui.lineEdit_8.setText(i.replace('MF', '', ))
        except:
            self.ui.plainTextEdit_py.insertPlainText('home点异常' + '\n')

    #写入位置按钮
    def writeCommand(self):
        try:
            data = self.ui.lineEdit_10.text()
            self.ui.lineEdit_10.setText("")
            self.ui.plainTextEdit_4.insertPlainText(data + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('写入位置异常'+'\n')

    #记录位置一
    def recPosition1(self):
        try:
            data = self.ui.lineEdit_10.text()
            config.position_data1 = data
            self.ui.lineEdit_10.setText("")

        except:
            self.ui.plainTextEdit_py.insertPlainText('记录异常'+'\n')
    #记录位置二
    def recPosition2(self):
        try:
            data = self.ui.lineEdit_10.text()
            config.position_data2 = data
            self.ui.lineEdit_10.setText("")

        except:
            self.ui.plainTextEdit_py.insertPlainText('记录异常'+'\n')
    #记录位置三
    def recPosition3(self):
        try:
            data = self.ui.lineEdit_10.text()
            config.position_data3 = data
            self.ui.lineEdit_10.setText("")

        except:
            self.ui.plainTextEdit_py.insertPlainText('记录异常'+'\n')
    #记录位置四
    def recPosition4(self):
        try:
            data = self.ui.lineEdit_10.text()
            config.position_data4 = data
            self.ui.lineEdit_10.setText("")

        except:
            self.ui.plainTextEdit_py.insertPlainText('记录异常'+'\n')
    #记录位置五
    def recPosition5(self):
        try:
            data = self.ui.lineEdit_10.text()
            config.position_data5 = data
            self.ui.lineEdit_10.setText("")

        except:
            self.ui.plainTextEdit_py.insertPlainText('记录异常'+'\n')
    #记录位置六
    def recPosition6(self):
        try:
            data = self.ui.lineEdit_10.text()
            config.position_data6 = data
            self.ui.lineEdit_10.setText("")

        except:
            self.ui.plainTextEdit_py.insertPlainText('记录异常'+'\n')

    #写入一面板
    def wriPosition1(self):
        try:
            if(config.position_data1):
                self.ui.plainTextEdit_4.insertPlainText(config.position_data1 + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('写入异常' + '\n')

    # 写入2面板
    def wriPosition2(self):
        try:
            if (config.position_data2):
                self.ui.plainTextEdit_4.insertPlainText(config.position_data2 + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('写入异常' + '\n')

    # 写入3面板
    def wriPosition3(self):
        try:
            if (config.position_data3):
                self.ui.plainTextEdit_4.insertPlainText(config.position_data3 + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('写入异常' + '\n')

    def wriPosition4(self):
        try:
            if (config.position_data4):
                self.ui.plainTextEdit_4.insertPlainText(config.position_data4 + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('写入异常' + '\n')

    def wriPosition5(self):
        try:
            if (config.position_data5):
                self.ui.plainTextEdit_4.insertPlainText(config.position_data5 + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('写入异常' + '\n')

    def wriPosition6(self):
        try:
            if (config.position_data6):
                self.ui.plainTextEdit_4.insertPlainText(config.position_data6 + '\n')
        except:
            self.ui.plainTextEdit_py.insertPlainText('写入异常' + '\n')

    #删除位置一记录
    def delPosition1(self):
        try:
            if (config.position_data1):
                config.position_data1 = ""

        except:
            self.ui.plainTextEdit_py.insertPlainText('删除位置一异常' + '\n')

    # 删除位置2记录
    def delPosition2(self):
        try:
            if (config.position_data2):
                config.position_data2 = ""

        except:
            self.ui.plainTextEdit_py.insertPlainText('删除位置一异常' + '\n')

        # 删除位置3记录
    def delPosition3(self):
        try:
            if (config.position_data3):
                config.position_data3 = ""

        except:
            self.ui.plainTextEdit_py.insertPlainText('删除位置一异常' + '\n')
    # 删除位置4记录
    def delPosition4(self):
        try:
            if (config.position_data4):
                config.position_data4 = ""

        except:
            self.ui.plainTextEdit_py.insertPlainText('删除位置一异常' + '\n')
    #删除记录5
    def delPosition5(self):
        try:
            if (config.position_data5):
                config.position_data5 = ""
        except:
            self.ui.plainTextEdit_py.insertPlainText('删除位置一异常' + '\n')
    #删除记录6
    def delPosition6(self):
        try:
            if (config.position_data6):
                config.position_data6 = ""

        except:
            self.ui.plainTextEdit_py.insertPlainText('删除位置一异常' + '\n')
    #运行到位置一
    def runPosision1(self):
        try:
            if(config.position_data1):
                data = config.position_data1
                while True:
                    # 发送字符Mw给Arduino询问6个电机是否停止状态
                    gcode = "Mw"
                    self.uart.write(gcode.encode())
                    sleep(0.2)

                    # 串口接收数据设置全局变量保存moter_state的值
                    if (config._moter_state == "yes"):
                        # 更改电机状态为非yes
                        config._moter_state = "no"
                        # 退出循环
                        break
                self.uart.write(data.encode())
                for i in data:
                    if i.find("MP") == 0:
                        # 刷新界面电机步进数值，判断前缀替换为空
                        self.ui.lineEdit.setText(i.replace('MP', '', ))
                    elif i.find("MA") == 0:
                        self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                    elif i.find("MB") == 0:
                        self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                    elif i.find("MC") == 0:
                        self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                    elif i.find("MD") == 0:
                        self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                    elif i.find("ME") == 0:
                        self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                    elif i.find("MF") == 0:
                        self.ui.lineEdit_8.setText(i.replace('MF', '', ))
        except:
            self.ui.plainTextEdit_py.insertPlainText('运行位置1异常' + '\n')
    #运行到位置二
    def runPosision2(self):
        try:
            if(config.position_data2):
                data = config.position_data2
                while True:
                    # 发送字符Mw给Arduino询问6个电机是否停止状态
                    gcode = "Mw"
                    self.uart.write(gcode.encode())
                    sleep(0.2)

                    # 串口接收数据设置全局变量保存moter_state的值
                    if (config._moter_state == "yes"):
                        # 更改电机状态为非yes
                        config._moter_state = "no"
                        # 退出循环
                        break
                self.uart.write(data.encode())
                for i in data:
                    if i.find("MP") == 0:
                        # 刷新界面电机步进数值，判断前缀替换为空
                        self.ui.lineEdit.setText(i.replace('MP', '', ))
                    elif i.find("MA") == 0:
                        self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                    elif i.find("MB") == 0:
                        self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                    elif i.find("MC") == 0:
                        self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                    elif i.find("MD") == 0:
                        self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                    elif i.find("ME") == 0:
                        self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                    elif i.find("MF") == 0:
                        self.ui.lineEdit_8.setText(i.replace('MF', '', ))
        except:
            self.ui.plainTextEdit_py.insertPlainText('运行位置2异常' + '\n')
    #运行位置3
    def runPosision3(self):
        try:
            if(config.position_data3):
                data = config.position_data3
                while True:
                    # 发送字符Mw给Arduino询问6个电机是否停止状态
                    gcode = "Mw"
                    self.uart.write(gcode.encode())
                    sleep(0.2)

                    # 串口接收数据设置全局变量保存moter_state的值
                    if (config._moter_state == "yes"):
                        # 更改电机状态为非yes
                        config._moter_state = "no"
                        # 退出循环
                        break
                self.uart.write(data.encode())
                for i in data:
                    if i.find("MP") == 0:
                        # 刷新界面电机步进数值，判断前缀替换为空
                        self.ui.lineEdit.setText(i.replace('MP', '', ))
                    elif i.find("MA") == 0:
                        self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                    elif i.find("MB") == 0:
                        self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                    elif i.find("MC") == 0:
                        self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                    elif i.find("MD") == 0:
                        self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                    elif i.find("ME") == 0:
                        self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                    elif i.find("MF") == 0:
                        self.ui.lineEdit_8.setText(i.replace('MF', '', ))
        except:
            self.ui.plainTextEdit_py.insertPlainText('运行位置一异常' + '\n')
    #运行位置4
    def runPosision4(self):
        try:
            if(config.position_data4):
                data = config.position_data4
                while True:
                    # 发送字符Mw给Arduino询问6个电机是否停止状态
                    gcode = "Mw"
                    self.uart.write(gcode.encode())
                    sleep(0.2)

                    # 串口接收数据设置全局变量保存moter_state的值
                    if (config._moter_state == "yes"):
                        # 更改电机状态为非yes
                        config._moter_state = "no"
                        # 退出循环
                        break
                self.uart.write(data.encode())
                for i in data:
                    if i.find("MP") == 0:
                        # 刷新界面电机步进数值，判断前缀替换为空
                        self.ui.lineEdit.setText(i.replace('MP', '', ))
                    elif i.find("MA") == 0:
                        self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                    elif i.find("MB") == 0:
                        self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                    elif i.find("MC") == 0:
                        self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                    elif i.find("MD") == 0:
                        self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                    elif i.find("ME") == 0:
                        self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                    elif i.find("MF") == 0:
                        self.ui.lineEdit_8.setText(i.replace('MF', '', ))
        except:
            self.ui.plainTextEdit_py.insertPlainText('运行位置一异常' + '\n')
    #运行位置5
    def runPosision5(self):
        try:
            if(config.position_data5):
                data = config.position_data5
                while True:
                    # 发送字符Mw给Arduino询问6个电机是否停止状态
                    gcode = "Mw"
                    self.uart.write(gcode.encode())
                    sleep(0.2)

                    # 串口接收数据设置全局变量保存moter_state的值
                    if (config._moter_state == "yes"):
                        # 更改电机状态为非yes
                        config._moter_state = "no"
                        # 退出循环
                        break
                self.uart.write(data.encode())
                for i in data:
                    if i.find("MP") == 0:
                        # 刷新界面电机步进数值，判断前缀替换为空
                        self.ui.lineEdit.setText(i.replace('MP', '', ))
                    elif i.find("MA") == 0:
                        self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                    elif i.find("MB") == 0:
                        self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                    elif i.find("MC") == 0:
                        self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                    elif i.find("MD") == 0:
                        self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                    elif i.find("ME") == 0:
                        self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                    elif i.find("MF") == 0:
                        self.ui.lineEdit_8.setText(i.replace('MF', '', ))
        except:
            self.ui.plainTextEdit_py.insertPlainText('运行位置一异常' + '\n')
    #运行位置6
    def runPosision6(self):
        try:
            if(config.position_data6):
                data = config.position_data6
                while True:
                    # 发送字符Mw给Arduino询问6个电机是否停止状态
                    gcode = "Mw"
                    self.uart.write(gcode.encode())
                    sleep(0.2)

                    # 串口接收数据设置全局变量保存moter_state的值
                    if (config._moter_state == "yes"):
                        # 更改电机状态为非yes
                        config._moter_state = "no"
                        # 退出循环
                        break
                self.uart.write(data.encode())
                for i in data:
                    if i.find("MP") == 0:
                        # 刷新界面电机步进数值，判断前缀替换为空
                        self.ui.lineEdit.setText(i.replace('MP', '', ))
                    elif i.find("MA") == 0:
                        self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                    elif i.find("MB") == 0:
                        self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                    elif i.find("MC") == 0:
                        self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                    elif i.find("MD") == 0:
                        self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                    elif i.find("ME") == 0:
                        self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                    elif i.find("MF") == 0:
                        self.ui.lineEdit_8.setText(i.replace('MF', '', ))
        except:
            self.ui.plainTextEdit_py.insertPlainText('运行位置一异常' + '\n')

    #情空面板
    def clearBoard(self):
        try:
            self.ui.plainTextEdit_4.setPlainText("")
        except:
            self.ui.plainTextEdit_py.insertPlainText('清空面板异常' + '\n')

    #执行指令
    def runExecute(self):
        try:
            # 获取ui界面循环次数数值
            count1 = self.ui.lineEdit_11.text()
            # 获取ui界面累计次数数值
            count2 = self.ui.lineEdit_12.text()
            count1 = int(count1)
            count2 = int(count2)
            while True:
                if count2 == count1:
                    break
                count2 += 1
                #判断电机是否处于停止状态
                while (config._moter_state == "no"):
                    config._moter_state = "no"
                    break

                #读取面板指令
                text = self.ui.plainTextEdit_4.toPlainText()
                #切割
                text_list = text.split("\n")

                if text_list[-1] == "":
                    #删除最后一个元素
                    text_list.pop()
                data1 = text
                for n in text_list:
                    while True:
                        print("正在判断6个电机是否驱动完毕...")
                        # 发送字符Mw给Arduino询问6个电机是否停止状态
                        gcode = "Mw"
                        self.uart.write(gcode.encode())
                        sleep(0.2)

                        # 串口接收数据设置全局变量保存moter_state的值
                        if (config._moter_state == "yes"):
                            print("电机停止状态 = " + config._moter_state + " 继续发送G代码!")
                            # 更改电机状态为非yes
                            config._moter_state = "no"
                            # 退出循环
                            break
                    self.uart.write(n.encode())  # 串口发送数据 字符串需要转换数据格式 <class 'bytes'>格式
                    print("串口发送的指令:", n)
                    self.ui.lineEdit_12.setText(str(count2))  # 获取ui界面累计次数数值
                    data2 = data1.split(",")
                    # 刷新界面电机步进值数值
                    # 遍历列表，逐个找到对应指令前缀
                    for i in data2:
                        if i.find("MP") == 0:
                            # 刷新界面电机步进数值，判断前缀替换为空
                            self.ui.lineEdit.setText(i.replace('MP', '', ))
                        elif i.find("MA") == 0:
                            self.ui.lineEdit_6.setText(i.replace('MA', '', ))
                        elif i.find("MB") == 0:
                            self.ui.lineEdit_3.setText(i.replace('MB', '', ))
                        elif i.find("MC") == 0:
                            self.ui.lineEdit_4.setText(i.replace('MC', '', ))
                        elif i.find("MD") == 0:
                            self.ui.lineEdit_7.setText(i.replace('MD', '', ))
                        elif i.find("ME") == 0:
                            self.ui.lineEdit_9.setText(i.replace('ME', '', ))
                        elif i.find("MF") == 0:
                            self.ui.lineEdit_8.setText(i.replace('MF', '', ))


            self.ui.lineEdit_12.setText("0")
            self.ui.plainTextEdit_py.insertPlainText("执行指令完成!" + '\n')



        except:
            self.ui.plainTextEdit_py.insertPlainText('执行按钮异常' + '\n')
    def runExecute_thread(self):
        thread = threading.Thread(target=self.runExecute, daemon=True)
        thread.start()


    def motor1Run(self):
        try:
            data = "MIR"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def run_thread1(self):
        thread = threading.Thread(target=self.motor1Run, daemon=True)
        thread.start()

    def nimotor1Run(self):
        try:
            data = "MIT"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def nirun_thread1(self):
        thread = threading.Thread(target=self.nimotor1Run, daemon=True)
        thread.start()
    def stopMotor1(self):
        try:
            data = "MIRS"
            self.uart.write(data.encode())
        except:
            pass
    def stop_thread1(self):
        thread = threading.Thread(target=self.stopMotor1, daemon=True)
        thread.start()

    def motor2Run(self):
        try:
            data = "MIV"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def run_thread2(self):
        thread = threading.Thread(target=self.motor2Run, daemon=True)
        thread.start()


    def nimotor2Run(self):
        try:
            data = "MIB"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def nirun_thread2(self):
        thread = threading.Thread(target=self.nimotor2Run, daemon=True)
        thread.start()
    def stopMotor2(self):
        try:
            data = "MIVS"
            self.uart.write(data.encode())
        except:
            pass
    def stop_thread2(self):
        thread = threading.Thread(target=self.stopMotor2, daemon=True)
        thread.start()

    def motor3Run(self):
        try:
            data = "MIH"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def run_thread3(self):
        thread = threading.Thread(target=self.motor3Run, daemon=True)
        thread.start()


    def nimotor3Run(self):
        try:
            data = "MIJ"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def nirun_thread3(self):
        thread = threading.Thread(target=self.nimotor3Run, daemon=True)
        thread.start()
    def stopMotor3(self):
        try:
            data = "MIHS"
            self.uart.write(data.encode())
        except:
            pass
    def stop_thread3(self):
        thread = threading.Thread(target=self.stopMotor3, daemon=True)
        thread.start()


    def motor4Run(self):
        try:
            data = "MIK"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def run_thread4(self):
        thread = threading.Thread(target=self.motor4Run, daemon=True)
        thread.start()


    def nimotor4Run(self):
        try:
            data = "MIL"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def nirun_thread4(self):
        thread = threading.Thread(target=self.nimotor4Run, daemon=True)
        thread.start()
    def stopMotor4(self):
        try:
            data = "MIKS"
            self.uart.write(data.encode())
        except:
            pass
    def stop_thread4(self):
        thread = threading.Thread(target=self.stopMotor4, daemon=True)
        thread.start()


    def motor5Run(self):
        try:
            data = "MIG"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def run_thread5(self):
        thread = threading.Thread(target=self.motor5Run, daemon=True)
        thread.start()


    def nimotor5Run(self):
        try:
            data = "MIU"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def nirun_thread5(self):
        thread = threading.Thread(target=self.nimotor5Run, daemon=True)
        thread.start()
    def stopMotor5(self):
        try:
            data = "MIGS"
            self.uart.write(data.encode())
        except:
            pass
    def stop_thread5(self):
        thread = threading.Thread(target=self.stopMotor5, daemon=True)
        thread.start()


    def motor6Run(self):
        try:
            data = "MIQ"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def run_thread6(self):
        thread = threading.Thread(target=self.motor6Run, daemon=True)
        thread.start()


    def nimotor6Run(self):
        try:
            data = "MIW"
            self.uart.write(data.encode())
        except:
            self.ui.plainTextEdit_py.insertPlainText('实时控制一轴正转按钮异常' + '\n')
    def nirun_thread6(self):
        thread = threading.Thread(target=self.nimotor6Run, daemon=True)
        thread.start()
    def stopMotor6(self):
        try:
            data = "MIQS"
            self.uart.write(data.encode())
        except:
            pass
    def stop_thread6(self):
        thread = threading.Thread(target=self.stopMotor6, daemon=True)
        thread.start()


if __name__ == '__main__':


    app = QApplication([])
    app.setWindowIcon(QIcon('logo.jpg'))
    stats = Interface()
    stats.ui.show()


    app.exec_()
