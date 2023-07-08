from kivy.app import App


from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from src.game import Game


class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set the orientation and padding of the BoxLayout
        self.orientation = "vertical"
        self.padding = 50

        # add the Game title
        title = Label(text="A BRICKS GAME", font_size=50, size_hint=(1, 0.5))
        self.add_widget(title)

        # add the play button
        play_button = Button(text="PLAY", font_size=30, size_hint=(1, 0.3), background_color=[0, 1, 0, 1])
        play_button.bind(on_release=self.start_game)
        self.add_widget(play_button)

        # add the quit button
        quit_button = Button(text="QUIT", font_size=30, size_hint=(1, 0.2), background_color=[1, 0, 0, 1])
        quit_button.bind(on_release=self.quit_game)
        self.add_widget(quit_button)

    def start_game(self, *args):
        game = Game()
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(game)
        game.start_game()

    def quit_game(self, *args):
        App.get_running_app().stop()


class BricksApp(App):
    def build(self):
        menu = MainMenu()
        return menu


if __name__ == "__main__":
    BricksApp().run()
