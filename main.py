from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ReferenceListProperty

from kivy.vector import Vector
from kivy.clock import Clock


class PaddleLR(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            self.score += 1

            vx, vy = ball.vel
            offset = (ball.center_y - self.center_y) / (self.height/2)
            bounced = Vector(-1*vx, vy)
            vel = bounced * 1.05
            ball.vel = vel.x, vel.y + offset


class PaddleTB(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            self.score += 1

            vx, vy = ball.vel
            offset = (ball.center_x - self.center_x) / (self.width/2)
            bounced = Vector(vx, -1*vy)
            vel = bounced * 1.05
            ball.vel = vel.x + offset, vel.y


class Ball(Widget):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    vel = ReferenceListProperty(vel_x, vel_y)

    def move(self):
        self.pos = Vector(*self.vel) + self.pos


class MainWindow(Widget):
    ball = ObjectProperty(None)
    player_left = ObjectProperty(None)
    player_top = ObjectProperty(None)
    player_right = ObjectProperty(None)
    player_bottom = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.vel = vel

    def update(self, dt):
        self.ball.move()

        self.player_left.bounce_ball(self.ball)
        self.player_top.bounce_ball(self.ball)
        self.player_right.bounce_ball(self.ball)
        self.player_bottom.bounce_ball(self.ball)

        # Conditions
        if self.ball.x + 20 > self.width:
            self.player_right.score -= 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x < self.x:
            self.player_left.score -= 1
            self.serve_ball(vel=(0, 4))
        if self.ball.y +20 > self.top:
            self.player_bottom.score -= 1
            self.serve_ball(vel=(-4, 0))
        if self.ball.y < self.y:
            self.player_top.score -= 1
            self.serve_ball(vel=(0, -4))

    def on_touch_move(self, touch):
        if (self.player_left.x < touch.x < self.player_left.x + 30) and \
                (self.player_left.y < touch.y < self.player_left.y + 100):
            self.player_left.center_y = touch.y

        if (self.player_right.x < touch.x < self.player_right.x + 30) and \
                (self.player_right.y < touch.y < self.player_right.y + 100):
            self.player_right.center_y = touch.y

        if (self.player_top.x < touch.x < self.player_top.x + 100) and \
                (self.player_top.y < touch.y < self.player_top.y + 30):
            self.player_top.center_x = touch.x

        if (self.player_bottom.x < touch.x < self.player_bottom.x + 100) and \
                (self.player_bottom.y < touch.y < self.player_bottom.y + 30):
            self.player_bottom.center_x = touch.x


class GameApp(App):
    def build(self):
        game = MainWindow()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == "__main__":
    GameApp().run()
