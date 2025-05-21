from graphics import Text, Point
from Button import Button

class GameOver():
    def __init__(self):

        self.gameOverText = Text(Point(400, 400), "GameOver")
        self.gameOverText.setSize(36)
        self.gameOverText.setStyle("bold")
        self.gameOverText.setFill("white")

        self.returnTitleButton = Button(Point(250, 250), 150, 50, "Return to the title")
        self.quitButton = Button(Point(550, 250), 150, 50, "Exit the game")

        self.isReturnTitleClicked = False

    def showGameOver(self, win):
        # ゲームオーバーの文字とボタンを表示
        self.gameOverText.draw(win)
        self.returnTitleButton.drawButton(win)
        self.quitButton.drawButton(win)

        # ボタンが押されるまで待機
        pt = win.getMouse()
        while True:
            if(self.quitButton.isclicked(pt)): # quitButtonが押されたらゲームを終了する
                break
            if(self.returnTitleButton.isclicked(pt)):
                self.isReturnTitleClicked = True
                break

            pt = win.getMouse()
        
        # テキストやボタンを消す
        self.returnTitleButton.undrawButton()
        self.quitButton.undrawButton()
        self.gameOverText.undraw()