import sys


first_row_list = ['심볼', '사이즈', '진입 가격', '시장 평균가', '청산 가격', '마진 비율', '마진', 'PNL(ROE %)',
                  'ADL', '전체 포지션 종료', '전체 포지션 이익실현(TP) / 스탑 로스(SL)']
for index, content in enumerate(first_row_list):
    setattr(thismodule, f'label{index}', content)

print(label1, label2, label3)

self.layout.addWidget(QtWidgets.QLabel(f'{pos.symbol}'), 1, 0)
self.layout.addWidget(QtWidgets.QLabel(f'{pos.positionAmt}'), 1, 1)
self.layout.addWidget(QtWidgets.QLabel(f'{pos.entryPrice}'), 1, 2)
self.layout.addWidget(QtWidgets.QLabel(f'{pos.markPrice}'), 1, 3)


def set_table(self, songs_table):
    if self.songs_table:
        self._layout.replaceWidget(self.songs_table, songs_table)
        self.songs_table.close()
        del self.songs_table
    else:
        self._layout.addWidget(songs_table)
        self._layout.addSpacing(10)
    self.songs_table = songs_table


