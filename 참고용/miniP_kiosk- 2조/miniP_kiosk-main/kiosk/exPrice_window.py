from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import cx_Oracle as oci

expPrice_form = uic.loadUiType("ui/exp_price.ui")[0]

# DB 연결 정보
sid = 'XE'
# host = '210.119.14.76'
host = '210.119.14.76'
port = 1521
username = 'kiosk'
password = '12345'

class expriceWindow(QMainWindow, expPrice_form):
    def __init__(self, menu_id, parent=None):
        super().__init__(parent)  # 부모 창 설정
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img/coffee-cup.png"))

        self.loadData(menu_id)
        self.add_btn.clicked.connect(self.add_btn_clicked)
        self.cancel_btn.clicked.connect(self.close)  # 취소 버튼 클릭 시 창 닫기

    def loadData(self, menu_id):
        """
        데이터베이스에서 menu_id에 해당하는 메뉴 데이터를 가져와 UI에 표시
        """
        # DB 연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        # menu_id에 해당하는 메뉴 데이터 가져오기
        query = '''
            SELECT menu_name, menu_info, menu_price, category, image
            FROM MENU
            WHERE menu_id = :menu_id
        '''
        cursor.execute(query, {'menu_id': menu_id})

        # 데이터 가져오기
        row = cursor.fetchone()
        if row:
            menu_name, menu_info, menu_price, category, image = row

            # QLabel에 데이터 설정
            self.menu_name.setText(menu_name)  # 메뉴 이름 설정
            self.exp_label.setText(menu_info)  # 메뉴 설명 설정
            self.price_label.setText(f"가격: {menu_price}원")  # 가격 설정
            self.exp_label.setWordWrap(True)  # 텍스트 줄바꿈 활성화

        else:
            print(f"menu_id {menu_id}에 해당하는 데이터를 찾을 수 없습니다.")

        # DB 연결 닫기
        cursor.close()
        conn.close()

    def add_btn_clicked(self):
        # 수량 선택 후 추가 버튼 클릭 시 동작
        quantity = int(self.countBox.value())  # SpinBox에서 수량 가져오기
        menu_name = self.menu_name.text()
        menu_price_text = self.price_label.text()  # 가격 레이블에서 가격 텍스트 가져오기

        # 가격에서 숫자만 추출 (가격이 "가격: 1500원" 형태일 경우)
        menu_price = int(menu_price_text.split(" ")[1].replace("원", ""))  # "1500"만 추출

        # 수량과 가격을 곱해서 총 가격 계산
        total_price = menu_price * quantity

        # 테이블에 데이터를 추가
        self.window_4 = self.parent()  # 부모 창 가져오기
        self.window_4.addMenuTable(menu_name, quantity, total_price)  # 메뉴명, 수량, 계산된 총 가격 추가

        self.close()




