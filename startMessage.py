from graphics import *
import time
from msvcrt import getch       # キーボード入力

def main():
    win = GraphWin("Test",1280, 640)
    win.setCoords(0.0,0.0,3.0,4.0)
    
    # ゲーム開始時に表示するメッセージ
    enterText = Text(Point(1.5,2),"Press Enter")
    enterText.setSize(20)
    enterText.setTextColor("red")
    enterText.draw(win)

    while True:
        key = win.checkKey()

        # Enterキーの入力を検知
        if(key == "Return"):

            # メッセージを"Start"に変えて2秒間表示
            enterText.setText("Start")
            time.sleep(2)
            enterText.setText("")
            break
    
    # ここは消去
    win.getMouse()

main()

# def startWin(self):

#     Text(Point(1,1),"Press Enter").draw(self.win)

#     outputText = Text(Point(2.25,1),"")
#     outputText.draw(self.win)
#     button = Text(Point(1.5,2.0), "it")
#     button.draw(self.win)
    
#     self.win.getMouse()

#     button.setText("Quit")

#     self.win.getMouse()
#     self.win.close()