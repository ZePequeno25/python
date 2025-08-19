from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton  # Import MDFloatingActionButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.toolbar import MDToolbar
import threading

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDToolbar:
        title: "App de Mídias"
        elevation: 10
    ScrollView:
        MDList:
            id: media_list
    MDFloatingActionButton:
        icon: "folder"
        pos_hint: {"center_x": .9, "center_y": .1}
        on_release: app.open_file_manager()
'''

class MediaApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        self.allow_ui_access = True  # Controle de acesso à thread principal
        return Builder.load_string(KV)

    def open_file_manager(self):
        self.file_manager.show('/')

    def select_path(self, path):
        self.exit_manager()
        # Exemplo: processamento em thread separada
        threading.Thread(target=self.process_media_item, args=(path,)).start()

    def process_media_item(self, path):
        # Simula processamento e tenta acessar a UI
        self.run_on_ui_thread(lambda: self.add_media_item(path))
        self.run_on_ui_thread(lambda: Snackbar(text=f"Arquivo selecionado: {path}").open())

    def run_on_ui_thread(self, func):
        # Só permite acesso se o controle estiver liberado
        if self.allow_ui_access:
            Clock.schedule_once(lambda dt: func())

    def block_ui_access(self):
        self.allow_ui_access = False

    def allow_ui_access_again(self):
        self.allow_ui_access = True

    def exit_manager(self, *args):
        self.file_manager.close()

    def add_media_item(self, path):
        media_list = self.root.ids.media_list
        media_list.add_widget(
            OneLineListItem(
                text=path,
                on_release=lambda x: self.show_media_dialog(path)
            )
        )

    def show_media_dialog(self, path):
        dialog = MDDialog(
            title="Arquivo de Mídia",
            text=f"Você selecionou:\n{path}",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

if __name__ == "__main__":
    MediaApp().run()