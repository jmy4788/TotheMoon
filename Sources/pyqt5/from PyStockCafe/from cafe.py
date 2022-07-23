import time
import atexit

from PyQt5 import QtWidgets, QtCore, QAxContainer

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# 사용자 이벤트용 클래스
class SignalHandler(QtCore.QObject):
    '''
    QtWidgets 상속 클래스에서는 시그널을 생성하여 사용못한다.
    대신 시그널 생성 가능 객체를 만들어서 인스턴스 변수에 바인딩하여 사용한다.
    '''
    msg_data_received = QtCore.pyqtSignal(str, int, int, int)  # 데이터가 수신되었을 때 사용할 이벤트
    msg_draw_graph = QtCore.pyqtSignal(str)  # 그래프 그리기 이벤트


class MyWindow(QtWidgets.QMainWindow):
    '''
    메인 윈도우
    UI는 내부에서 직접 작성하여 대응함
    '''

    def __init__(self):
        super().__init__()

        self.tick_count = 0  # 참고용, 실행시킨 이후 수신받은 틱 수

        self.selectedRow = 0  # 테이블 위젯 항목 선택 위치 확인용, 초기값은 0

        # 확인하고 싶은 종목코드를 등록한다.
        self.codes = [
            "005930",
            "020760",
            "108230",
            "095270",
            "066570",
            "215600",
            "016920",
        ]

        self.names = []  # 종목코드에 대한 한글이름 저장용, 로그인 시점에서 작성됨
        self.datas = {}  # 실시간 수신 데이터 저장용

        # 각 종목코드 별로 리스트를 생성한다.
        for code in self.codes:
            self.datas[code] = []

        # 키움 객체 및 사용자 이벤트용 객체
        self.objKiwoom = QAxContainer.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.objSignal = SignalHandler()

        self.initUI()  # UI를 구성한다.
        self.initSignalSlot()  # 시그널/슬롯 설정

        atexit.register(self.__del__)  # 종료 버튼으로 종료할 때 실행시킨다. __del__ 실행을 보장하기 위해서 사용

        # 로그인을 실행한다.
        self.objKiwoom.dynamicCall("CommConnect()")

    def __del__(self):
        '''
        종료시 실행할 작업
        '''
        self.objKiwoom.dynamicCall("SetRealRemove(str, str)", "ALL", "ALL")

    ###############################################
    #
    # 사용자 함수
    #
    ###############################################

    def initUI(self):
        '''
        UI 생성 및 초기화
        '''
        # 메인 윈도우 설정 ---------------------------------------------
        self.setWindowTitle("Kiwoom Graph Sample")
        self.resize(350, 500)
        self.centralwidget = QtWidgets.QWidget(self)

        # 상태표시줄 설정 ---------------------------------------------
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready...")

        # 테이블 위젯 설정 ---------------------------------------------
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setMinimumSize(QtCore.QSize(0, 200))

        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        col_headers = ["종목명", "현재가", "전일대비", "거래량", ]  # 헤더 항목 설정

        self.table.setColumnCount(len(col_headers))
        self.table.setHorizontalHeaderLabels(col_headers)
        self.table.setRowCount(len(self.codes))
        self.table.setAlternatingRowColors(True)

        self.table.setColumnWidth(0, 100)  # 헤더 필드 폭 설정
        self.table.setColumnWidth(1, 60)
        self.table.setColumnWidth(2, 60)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)  # 마지막은 자동으로 조정
        self.table.resizeRowsToContents()

        # 버튼 설정 ---------------------------------------------
        # 버튼 왼쪽 스페이스
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # 현재가 요청 버튼 설정
        self.requestTrButton = QtWidgets.QPushButton("Get Price", self.centralwidget)
        # 로그인 전까지 버튼을 사용할 수 없게 한다.
        self.requestTrButton.setEnabled(False)

        # 종료 버튼 설정
        self.exitButton = QtWidgets.QPushButton("Exit", self.centralwidget)

        # 그래프 그리기 준비 ---------------------------------------------
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)

        # matplotlib에서 한글 처리를 위한 루틴
        font_name = matplotlib.font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        matplotlib.rc("font", family=font_name)

        # matplotlib에서 (-)표기를 위한 루틴
        matplotlib.rcParams['axes.unicode_minus'] = False

        # 레이아웃 배치 ---------------------------------------------
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.gridLayout.addWidget(self.table, 0, 0, 1, 3)  # addWidget(배치시킬 위젯, 행 위치, 열 위치, 행 폭, 열 폭)

        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.requestTrButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.exitButton, 1, 2, 1, 1)

        self.gridLayout.addWidget(self.canvas, 2, 0, 1, 3)

        # 레이아웃 설정
        self.gridLayout.setRowStretch(2, 1)
        self.setCentralWidget(self.centralwidget)

        self.canvas.draw()

    def initSignalSlot(self):
        '''
        시그널/슬롯 연결 설정
        '''
        # 수신 이벤트 연결
        self.objKiwoom.OnEventConnect.connect(self.myOnEventConnect)
        self.objKiwoom.OnReceiveTrData.connect(self.myOnReceiveTrData)
        self.objKiwoom.OnReceiveRealData.connect(self.myOnReceiveRealData)

        # 위젯 이벤트 연결
        self.table.cellClicked.connect(self.table_cell_clicked)
        self.requestTrButton.clicked.connect(self.requestTrButton_clicked)
        self.exitButton.clicked.connect(self.exitButton_clicked)

        # 사용자 이벤트 연결
        self.objSignal.msg_data_received.connect(self.myOnDataReceived)  # 데이터 수신시 이벤트
        self.objSignal.msg_draw_graph.connect(self.myOnDrawGraph)

    def regRealItem(self):
        '''
        self.codes에 저장되어 있는 종목코드를 실시간 등록한다.
        '''
        # 키움은 스크린번호당 100개까지 등록 가능
        # --> 한 스크린 번호당 100개씩 등록한다.
        nLength = len(self.codes)  # 전체 종목수
        nReqScrNo = int(nLength / 100) + 1  # 100개 단위 필요 스크린 수, +1 --> 100개 단위를 모으고 남은 자투리 항목용

        for i in range(nReqScrNo):
            sScreenNo = f"7{i:03}"  # 스크린 이름
            start = i * 100
            end = start + 100
            sCodes = ";".join(self.codes[start:end])  # 100개의 종목 문자열을 하나의 문자열로 만든다.
            self.objKiwoom.dynamicCall("SetRealReg(str, str, str, str)", sScreenNo, sCodes, "20;10;11;15",
                                       "0")  # 20:체결시간, 10:현재가, 11:전일대비, 15:거래량

        self.statusBar.showMessage("실시간 등록 완료")

    ###############################################
    #
    # 수신 Evnet 함수
    #
    ###############################################

    def myOnEventConnect(self, nErrCode):
        '''
        로그인 이벤트

        로그인 성공시 실시간 등록을 실행한다(실시간 등록 함수는 로그인 되어야 사용가능).
        로그인 실패시 종료한다.
        '''
        if nErrCode == 0:
            self.statusBar.showMessage("로그인 OK")

            self.requestTrButton.setEnabled(True)

            # 각 코드에 대한 종목명을 테이블 위젯에 입력한다.
            for code in self.codes:
                row = self.codes.index(code)
                hname = self.objKiwoom.dynamicCall("GetMasterCodeName(str)", code)  # 한글 종목명
                self.names.append(hname)  # 한글 종목명을 저장
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(hname))

            self.regRealItem()

        else:  # 로그인 실패시
            self.statusBar.showMessage(f"Error[{nErrCode}]")  # 오류 수정@2020.02.18

            QtCore.QCoreApplication.instance().quit()

    def myOnReceiveTrData(self, sScreenNo, sRqName, sTrCode, sRecordName, sPrevNext, *args):
        '''
        TR 수신 이벤트
        '''
        if sTrCode == "OPTKWFID":  # 관심종목정보요청
            nRow = self.objKiwoom.dynamicCall("GetRepeatCnt(str, str)", sTrCode, sRqName)

            for i in range(nRow):
                code = self.objKiwoom.dynamicCall("GetCommData(str, str, int, str)", sTrCode, "", i, "종목코드").strip()
                price = abs(int(self.objKiwoom.dynamicCall("GetCommData(str, str, int, str)", sTrCode, "", i, "현재가")))
                debi = int(self.objKiwoom.dynamicCall("GetCommData(str, str, int, str)", sTrCode, "", i, "전일대비"))
                volume = abs(int(self.objKiwoom.dynamicCall("GetCommData(str, str, int, str)", sTrCode, "", i, "거래량")))

                self.objSignal.msg_data_received.emit(code, price, debi, volume)  # 데이터 수신 완료 시그널 보내기

        self.statusBar.showMessage("TR 수신 완료")

    def myOnReceiveRealData(self, sCode, sRealType, sRealData):
        '''
        실시간 수신 이벤트
        '''
        if sRealType == "주식체결":
            try:
                code = sCode
                price = abs(int(self.objKiwoom.dynamicCall("GetCommRealData(str, int)", sCode, "10")))  # 현재가
                debi = int(self.objKiwoom.dynamicCall("GetCommRealData(str, int)", sCode, "11"))  # 전일대비
                volume = abs(int(self.objKiwoom.dynamicCall("GetCommRealData(str, int)", sCode, "15")))  # 거래량

                self.tick_count += 1
                self.statusBar.showMessage(f"수신 틱수: {self.tick_count}")

                self.datas[sCode].append(price)  # 데이터를 추가한다.

                self.objSignal.msg_data_received.emit(code, price, debi, volume)  # 데이터 수신 완료 시그널 보내기
                self.objSignal.msg_draw_graph.emit(code)  # code에 해당하는 그래프 그리기를 요청
            except:
                # 일반 TR을 전송해도 전송한 코드에 대해 실시간 등록을 하지 않아도 Real이벤트가 발생한다.
                # 따라서 해당 코드에 대해 처리되지 않으면 오류가 발생한다.
                # 이를 걸러 주기 위해 예외로 대응함
                pass

    ###############################################
    #
    # Slot 함수
    #
    ###############################################

    @QtCore.pyqtSlot(str, int, int, int)
    def myOnDataReceived(self, code, price, debi, volume):
        '''
        TR 또는 실시간 수신시 받은 데이터를 테이블 위젯에 기록한다.
        '''
        row = self.codes.index(code)

        item = QtWidgets.QTableWidgetItem(f"{price:,}")
        item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.table.setItem(row, 1, item)

        item = QtWidgets.QTableWidgetItem(f"{debi:,}")
        item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.table.setItem(row, 2, item)

        item = QtWidgets.QTableWidgetItem(f"{volume:,}")
        item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.table.setItem(row, 3, item)

    @QtCore.pyqtSlot(str)
    def myOnDrawGraph(self, sCode):
        '''
        그래프 그리기 요청에 대한 처리
        '''
        # print(f"{self.codes[self.selectedRow]}:{sCode}")
        if self.codes[self.selectedRow] == sCode:  # 테이블 위젯에서 선택된 종목코드와 실시간 수신된 종목코드가 같으면 그래프를 그린다.
            self.ax.clear()  # 그래프를 지운다.

            # 실시간 데이터 plot
            # x값은 생략, y값만 plot한다.
            self.ax.plot(self.datas[sCode], c='r', lw=0.5, label=self.names[self.codes.index(sCode)])

            self.ax.grid()  # 눈금 표시
            self.ax.legend(fontsize=8, loc="upper left")  # 범례 표시

            self.canvas.draw()  # 화면 갱신

    @QtCore.pyqtSlot()
    def requestTrButton_clicked(self):
        '''
        TR 조회 버튼 클릭시 실행

        주식기본정보요청("opt10001") 대신 관심종목정보요청("OPTKWFID") TR을 사용한다.
        수신 데이터 항목은 차이가 없지만 주식 기본정보요청 TR은 다종목 수신시 빈 데이터를 받는 오류가 자주 발생한다.
        다종목 수신시 관심종목정보요청 TR을 사용할 것

        ※ 참고)
        주식기본정보요청은 100종목 조회시 TR 100회 요청이 필요하지만 관심종목정보요청은 TR 1회로 요청할 수 있다.
        대신 CommKwRqData 전용함수를 사용한다. 수신 데이터는 multi 데이터임(주식기본정보요청 TR은 single 데이터)
        '''
        # 관심종목정보요청 : "OPTKWFID"
        # 한번에 100 종목 요청 가능
        # --> TR당 100개씩 요청한다.
        nLength = len(self.codes)  # 전체 종목수
        nReqScrNo = int(nLength / 100) + 1  # 100개 단위 필요 스크린 수, +1 --> 100개 단위를 모으고 남은 자투리 항목용

        for i in range(nReqScrNo):
            start = i * 100
            end = start + 100
            sCodes = ";".join(self.codes[start:end])  # 100개의 종목 문자열을 하나의 문자열로 만든다.
            self.objKiwoom.dynamicCall("CommKwRqData(str, int, int, int, str, str)", sCodes, 0, end - start, 0,
                                       "OPTKWFID_req", "RQTR")
            time.sleep(0.3)  # TR 연속 요청시 delay 0.3초

        self.statusBar.showMessage("TR조회 요청 완료")

    @QtCore.pyqtSlot()
    def exitButton_clicked(self):
        '''
        Exit 버튼을 클릭시 실행

        프로그램을 종료한다.
        '''
        QtCore.QCoreApplication.instance().quit()

    @QtCore.pyqtSlot(int, int)
    def table_cell_clicked(self, row, col):
        '''
        테이블 위젯에서 클릭이 되었을 때 실행
        '''
        if self.objKiwoom.dynamicCall("GetConnectState()") == 1:
            self.selectedRow = row

            self.objSignal.msg_draw_graph.emit(self.codes[self.selectedRow])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    myWindow = MyWindow()
    myWindow.show()

    app.exec_()