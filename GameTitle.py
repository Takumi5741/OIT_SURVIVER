from graphics import Image, Point
from Button import Button

class GameTitle():
    def __init__(self):

        self.gametitle_background = Image(Point(400,300), "img/title.png")

        self.playGameButton = Button(Point(250, 200), 150, 50, "Start game")
        self.quitButton = Button(Point(520, 200), 150, 50, "Exit the game")

        self.isContinueClicked = False

    def showGameStart(self, win):
        #スタート画面とボタンの表示
        self.gametitle_background.draw(win)
        self.playGameButton.drawButton(win)
        self.quitButton.drawButton(win)

        # ボタンが押されるまで待機
        pt = win.getMouse()
        while True:
            if(self.quitButton.isclicked(pt)): # quitButtonが押されたらゲームを終了する
                break
            if(self.playGameButton.isclicked(pt)):
                self.isContinueClicked = True
                break

            pt = win.getMouse()
        
        # テキストやボタンを消す
        self.playGameButton.undrawButton()
        self.quitButton.undrawButton()
        self.gametitle_background.undraw()