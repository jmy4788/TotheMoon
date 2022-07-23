import csv

with open(('꺼져.csv'), 'a', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # header 없으면 header 기록해줍니다.
    if head_exist is False:
        writer.writerow('안녕')
        head_exist = True
    # 이 부분 round함수 이용하는 것에서 f 포매팅으로 소수점 첫째자리까지만 표현하는 것으로 바꿨습니다.
