class ColorTheme:
    def __init__(
        self,
        modal_bg,
        modal_border,
        modal_shadow,
        text_color,
        button_bg,
        button_hover,
        button_pressed,
        slider_bg,
        slider_circle_hover,
        slider_circle,
    ):
        self.modal_bg = modal_bg
        self.modal_border = modal_border
        self.modal_shadow = modal_shadow
        self.text_color = text_color
        self.button_bg = button_bg
        self.button_hover = button_hover
        self.button_pressed = button_pressed
        self.slider_bg = slider_bg
        self.slider_hover = slider_circle_hover
        self.slider_pressed = slider_circle


BASIC_THEME = ColorTheme(
    modal_bg=(80, 100, 75),
    modal_border=(140, 165, 135),
    modal_shadow=(65, 85, 60),
    text_color=(255, 255, 255),
    button_bg=(70, 70, 80),
    button_hover=(230, 200, 100),
    button_pressed=(0, 0, 0),
    slider_bg=(65, 85, 60),
    slider_circle_hover=(230, 200, 100),
    slider_circle=(160, 170, 150),
)

MAIN_MENU_THEME = ColorTheme(
    modal_bg=(65, 50, 40),
    modal_border=(110, 100, 80),
    modal_shadow=(40, 30, 20),
    text_color=(255, 255, 255),
    button_bg=(40, 40, 40),
    button_hover=(230, 200, 100),
    button_pressed=(0, 0, 0),
    slider_bg=(47, 40, 35),
    slider_circle_hover=(100, 90, 70),
    slider_circle=(80, 70, 50),
)
