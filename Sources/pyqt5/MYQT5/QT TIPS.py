현재 문제는 QPicture에 QPaint가 안 되는 것으로 보입니다.
Qt로 GUI를 구성하는 것은 완전 마트료시카입니다.
1. QMainWindow가 실행되고
2. QMainWindow를 QWidget으로 채워 넣는데
3. QWdiget안에서 QGrahpicView가 실행되고
4. QGraphicView안에 QGraphicScene가 있고
5. QGraphicsScene안에는 QgraphicsObject로 채워넣는 겁니다.
오브젝트 생성시 생성자 안에 넣는 오브젝트는 부모 윈도우를 뜻 하는 듯

QGrpaihcs
Item
중
하나로
QGraphicsObject가
있고
QGraphics
object는
아래의
paint와
boundingRect
메소드를
기본적으로
탑재해야
함