from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from procurar_arquivo import ProcurarArquivoWidget

KV = '''
MDScreenManager:
    MenuScreen:
    ProcurarArquivoScreen:

<MenuScreen>:
    name: 'menu'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(40)
        MDLabel:
            text: 'Menu Principal'
            halign: 'center'
            font_style: 'H4'
        MDRaisedButton:
            text: 'Procurar Arquivo'
            pos_hint: {"center_x": .5}
            on_release: app.open_procurar_arquivo()

<ProcurarArquivoScreen>:
    name: 'procurar_arquivo'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'Procurar Arquivo'
            left_action_items: [["arrow-left", lambda x: app.voltar_menu()]]
        BoxLayout:
            orientation: 'vertical'
            id: procurar_arquivo_box
'''

class MenuScreen(MDScreen):
    pass

class ProcurarArquivoScreen(MDScreen):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm = Builder.load_string(KV)
        return self.sm

    def open_procurar_arquivo(self):
        box = self.sm.get_screen('procurar_arquivo').ids.procurar_arquivo_box
        box.clear_widgets()
        self.procurar_app = ProcurarArquivoWidget()
        box.add_widget(self.procurar_app)
        self.sm.current = 'procurar_arquivo'

    def voltar_menu(self):
        self.sm.current = 'menu'

if __name__ == "__main__":
    MainApp().run()