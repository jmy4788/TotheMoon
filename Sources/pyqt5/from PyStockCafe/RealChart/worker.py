import sys
import time
import zipfile
import datetime
import pythoncom
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QAxContainer import QAxWidget
from threading import Timer
app = QtWidgets.QApplication(sys.argv)


class Worker:
    def __init__(self, dataQ, tranQ):
        self.dataQ = dataQ
        self.tranQ = tranQ
        self.df_min = None
        self.df_trdata = None
        self.list_tritems = None
        self.list_trrecord = None
        self.bool_conn = False
        self.bool_received = False
        self.bool_trremained = False
        self.time_loop = datetime.datetime.now()
        self.time_upct = datetime.datetime.now()
        self.time_tran = datetime.datetime.now()
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._h_login)
        self.ocx.OnReceiveTrData.connect(self._h_tran_data)
        self.ocx.OnReceiveRealData.connect(self._h_real_data)
        self.RealChartStart()

    def RealChartStart(self):
        self.CommConnect()
        self.EventLoop()

    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        while not self.bool_conn:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.0001)
        self.dataQ.put(f"키움 OpenAPI 로그인 완료")

    def EventLoop(self):
        while True:
            if not self.tranQ.empty():
                data = self.tranQ.get()
                if type(data) == str:
                    self.SearchChart(data)
                elif type(data) == list:
                    self.UpdateRealreg(data)
            self.time_loop = datetime.datetime.now() + datetime.timedelta(seconds=+0.25)
            while datetime.datetime.now() < self.time_loop:
                pythoncom.PumpWaitingMessages()
                time.sleep(0.0001)

    def SearchChart(self, code):
        name = self.GetMasterCodeName(code)
        if self.df_min is not None and name == self.df_min['종목명'][0]:
            return
        if not self.TrtimeCondition:
            self.dataQ.put(f"해당 명령은 {self.RemainedTrtime}초 후에 실행됩니다.")
            Timer(self.RemainedTrtime, self.tranQ.put, args=[code]).start()
            return
        self.GetMinChart(code, name)

    def UpdateRealreg(self, rreg):
        name = self.GetMasterCodeName(rreg[1])
        if len(rreg) == 4:
            ret = self.ocx.dynamicCall(
                "SetRealReg(QString, QString, QString, QString)", rreg[0], rreg[1], rreg[2], rreg[3])
            self.dataQ.put(f"실시간 알림 등록 완료 {ret} {name}")
        else:
            ret = self.ocx.dynamicCall("SetRealRemove(QString, QString)", rreg[0], rreg[1])
            self.dataQ.put(f"실시간 알림 중단 완료 {ret} {name}")

    def GetMinChart(self, code, name):
        self.dataQ.put(f"{name}의 분봉차트를 조회 중입니다.")
        start = datetime.datetime.now()
        df = self.Block_Request("opt10080", 종목코드=code, 틱범위=5, 수정주가구분=0, output="주식분봉차트조회", next=0)
        try:
            self.df_min = self.UpdateChartDataFrame(df, code, name)
        except Exception as e:
            self.dataQ.put(f"[{self.strtime}] GetMinDayChart 주식분봉차트조회 {e}")
        else:
            self.PutChartDataFrame(self.df_min)
        self.UpdateTrtime(start, 1)
        self.tranQ.put(["ALL", "ALL"])
        self.tranQ.put(["0103", code, "10;12;14;30;228", 1])

    def UpdateChartDataFrame(self, df, code, name):
        df = df.set_index('체결시간')
        df_ = pd.DataFrame(columns=['현재가', '시가', '고가', '저가', '거래량',
                                    '지수이평05', '지수이평10', '지수이평20', '전일종가', '종목명'])
        df = df[::-1]
        df['현재가'] = df['현재가'].apply(self.text2int)
        df['시가'] = df['시가'].apply(self.text2int)
        df['고가'] = df['고가'].apply(self.text2int)
        df['저가'] = df['저가'].apply(self.text2int)
        df['거래량'] = df['거래량'].apply(self.text2int)
        pc = self.GetMasterLastPrice(code)
        for i, index in enumerate(df.index):
            c = df['현재가'][index]
            o = df['시가'][index]
            h = df['고가'][index]
            ll = df['저가'][index]
            v = df['거래량'][index]
            if i == 0:
                ema05 = c
                ema10 = c
                ema20 = c
            else:
                ema05 = int(df_['지수이평05'][i - 1] * 4 / 6 + 2 / 6 * c)
                ema10 = int(df_['지수이평10'][i - 1] * 9 / 11 + 2 / 11 * c)
                ema20 = int(df_['지수이평20'][i - 1] * 19 / 21 + 2 / 21 * c)
            df_ = df_.append(pd.DataFrame({
                '현재가': [c], '시가': [o], '고가': [h], '저가': [ll], '거래량': [v], '지수이평05': [ema05],
                '지수이평10': [ema10], '지수이평20': [ema20], '전일종가': [pc], '종목명': [name]}, index=[index]))
        if len(df_) > 78:
            df_ = df_[-78:]
        for index in df_.index:
            if int(index[:8]) < int(df_.index[-1][:8]) and int(index[8:]) <= int(df_.index[-1][8:]):
                df_.drop(index=index, inplace=True)
        df_['체결시간'] = df_.index
        df_['체결시간'] = df_['체결시간'].apply(self.ymdhms2hms)
        df_ = df_.set_index('체결시간')
        return df_

    def UpdateTrtime(self, start: datetime.datetime, trcount):
        self.time_tran = start + datetime.timedelta(seconds=+trcount * 3.35)
        remaintime = (self.time_tran - datetime.datetime.now()).total_seconds()
        if remaintime > 1:
            self.dataQ.put(f"TR 조회 재요청까지 남은 시간은 {round(remaintime, 2)}초입니다.")

    def Block_Request(self, *args, **kwargs):
        trcode = args[0].lower()
        liness = self.read_enc(trcode)
        self.list_tritems = self.parse_dat(trcode, liness)
        self.list_trrecord = kwargs["output"]
        nnext = kwargs["next"]
        for i in kwargs:
            if i.lower() != "output" and i.lower() != "next":
                self.ocx.dynamicCall("SetInputValue(QString, QString)", i, kwargs[i])
        self.bool_received = False
        self.bool_trremained = False
        if trcode == "optkwfid":
            codelist = args[1]
            ccount = args[2]
            self.ocx.dynamicCall("CommKwRqData(QString, bool, int, int, QString, QString)",
                                 codelist, 0, ccount, "0", self.list_trrecord, "0100")
        else:
            self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)",
                                 self.list_trrecord, trcode, nnext, "0100")
        time.sleep(0.25)
        while not self.bool_received:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.0001)
        return self.df_trdata

    def _h_login(self, err_code):
        if err_code == 0:
            self.bool_conn = True

    def _h_tran_data(self, screen, rqname, trcode, record, nnext):
        if screen == "" and record == "":
            return
        items = None
        if nnext == '2':
            self.bool_trremained = True
        else:
            self.bool_trremained = False
        for output in self.list_tritems['output']:
            record = list(output.keys())[0]
            items = list(output.values())[0]
            if record == self.list_trrecord:
                break
        rows = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        if rows == 0:
            rows = 1
        df2 = []
        for row in range(rows):
            row_data = []
            for item in items:
                data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, row, item)
                row_data.append(data.strip())
            df2.append(row_data)
        df = pd.DataFrame(data=df2, columns=items)
        self.df_trdata = df
        self.bool_received = True

    def _h_real_data(self, code, realtype, realdata):
        if realdata == "":
            return
        if realtype == "주식체결":
            try:
                c = abs(int(self.GetCommRealData(code, 10)))
                v = int(self.GetCommRealData(code, 15))
                d = self.GetCommRealData(code, 20)
                name = self.GetMasterCodeName(code)
            except Exception as e:
                self.dataQ.put(f"[{self.strtime}] _h_real_data 주식체결 {e}")
            else:
                self.UpdateJusicchegeolData(d, c, v, name)

    def UpdateJusicchegeolData(self, d, c, v, name):
        if self.df_min is not None and name == self.df_min['종목명'][0]:
            self.UpdateMinchart(d, c, v, name)
        if datetime.datetime.now() > self.time_upct:
            if self.df_min is not None:
                self.PutChartDataFrame(self.df_min)
            self.time_upct = datetime.datetime.now() + datetime.timedelta(seconds=+1)

    def UpdateMinchart(self, d, c, v, name):
        if int(d) >= int(self.df_min.index[0]):
            pc = self.df_min['전일종가'][0]
            ema05 = int(self.df_min['지수이평05'][-1] * 4 / 6 + 2 / 6 * c)
            ema10 = int(self.df_min['지수이평10'][-1] * 9 / 11 + 2 / 11 * c)
            ema20 = int(self.df_min['지수이평20'][-1] * 19 / 21 + 2 / 21 * c)
            self.df_min.drop(index=self.df_min.index[0], inplace=True)
            self.df_min = self.df_min.append(pd.DataFrame({
                '현재가': [c], '시가': [c], '고가': [c], '저가': [c], '거래량': [abs(v)], '지수이평05': [ema05],
                '지수이평10': [ema10], '지수이평20': [ema20], '전일종가': [pc], '종목명': [name]}, index=[d]))
        elif int(d) < int(self.df_min.index[0]):
            d = self.df_min.index[-1]
            o = self.df_min['시가'][d]
            h = self.df_min['고가'][d]
            ll = self.df_min['저가'][d]
            v = self.df_min['거래량'][d] + abs(v)
            pc = self.df_min['전일종가'][0]
            if c > h:
                h = c
            if c < ll:
                ll = c
            ema05 = int(self.df_min['지수이평05'][-2] * 4 / 6 + 2 / 6 * c)
            ema10 = int(self.df_min['지수이평10'][-2] * 9 / 11 + 2 / 11 * c)
            ema20 = int(self.df_min['지수이평20'][-2] * 19 / 21 + 2 / 21 * c)
            self.df_min.drop(index=self.df_min.index[-1], inplace=True)
            self.df_min = self.df_min.append(pd.DataFrame({
                '현재가': [c], '시가': [o], '고가': [h], '저가': [ll], '거래량': [v], '지수이평05': [ema05],
                '지수이평10': [ema10], '지수이평20': [ema20], '전일종가': [pc], '종목명': [name]}, index=[d]))

    def PutChartDataFrame(self, df):
        df['일자'] = df.index
        df['일자'] = df['일자'].apply(self.hms2hm)
        df = df.set_index('일자')
        df['직전지수이평05'] = df['지수이평05'].shift(1, fill_value=0)
        df['직전지수이평10'] = df['지수이평10'].shift(1, fill_value=0)
        df['직전지수이평20'] = df['지수이평20'].shift(1, fill_value=0)
        df['직전현재가'] = df['현재가'].shift(1, fill_value=0)
        df['직전거래량'] = df['거래량'].shift(1, fill_value=0)
        df['추세05'] = df['지수이평05'] > df['직전지수이평05']
        df['추세10'] = df['지수이평10'] > df['직전지수이평10']
        df['추세20'] = df['지수이평20'] > df['직전지수이평20']
        df['시종차'] = df['현재가'] - df['시가']
        self.dataQ.put(df)

    def GetCommRealData(self, code, fid):
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid)
        return data

    def GetMasterLastPrice(self, code):
        data = self.ocx.dynamicCall("GetMasterLastPrice(QString)", code)
        return int(data)

    def GetMasterCodeName(self, code):
        return self.ocx.dynamicCall("GetMasterCodeName(QString)", code)

    @property
    def TrtimeCondition(self):
        return datetime.datetime.now() > self.time_tran

    @property
    def RemainedTrtime(self):
        return round((self.time_tran - datetime.datetime.now()).total_seconds(), 2)

    @property
    def strtime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # noinspection PyMethodMayBeStatic
    def text2int(self, text):
        return abs(int(float(text)))

    # noinspection PyMethodMayBeStatic
    def ymdhms2hms(self, text):
        return text[8:]

    # noinspection PyMethodMayBeStatic
    def hms2hm(self, text):
        return f"{text[:2]}:{text[2:4]}"

    # noinspection PyMethodMayBeStatic
    def read_enc(self, opt_fname):
        fpath = "C:/OpenAPI/data/" + "{}.enc".format(opt_fname)
        enc = zipfile.ZipFile(fpath)
        dat_name = opt_fname.upper() + ".dat"
        liness = enc.read(dat_name).decode("cp949")
        return liness

    # noinspection PyMethodMayBeStatic
    def parse_block(self, data):
        block_info = data[0]
        if 'INPUT' in block_info:
            block_type = 'input'
        else:
            block_type = 'output'
        record_line = data[1]
        tokens = record_line.split('_')[1].strip()
        record = tokens.split("=")[0]
        fields = data[2:-1]
        field_name = []
        for line in fields:
            field = line.split("=")[0].strip()
            field_name.append(field)
        ret_data = {record: field_name}
        return block_type, ret_data

    def parse_dat(self, trcode, liness):
        liness = liness.split('\n')
        start_indices = [i for i, x in enumerate(liness) if x.startswith("@START")]
        end_indices = [i for i, x in enumerate(liness) if x.startswith("@END")]
        block_indices = zip(start_indices, end_indices)
        enc_data = {"trcode": trcode, "input": [], "output": []}
        for start, end in block_indices:
            block_data = liness[start - 1:end + 1]
            block_type, fields = self.parse_block(block_data)
            if block_type == "input":
                enc_data["input"].append(fields)
            else:
                enc_data["output"].append(fields)
        return enc_data
