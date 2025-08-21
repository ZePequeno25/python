from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton 
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
import threading

KV = '''
<ProcurarArquivoWidget@BoxLayout>:
    orientation: 'vertical'
    ScrollView:
        MDList:
            id: media_list
    MDFloatingActionButton:
        icon: "folder"
        pos_hint: {"center_x": .9, "center_y": .1}
        on_release: root.open_file_manager()
'''

Builder.load_string(KV)

class ProcurarArquivoWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

    def open_file_manager(self):
        try:
            self.file_manager.show('/')
        except Exception as e:
            Clock.schedule_once(lambda dt: MDSnackbar(MDLabel(text=f"Erro ao abrir gerenciador: {e}")).open())

    def select_path(self, path):
        self.exit_manager()
        threading.Thread(target=self.process_media_item, args=(path,)).start()

    def process_media_item(self, path):
        Clock.schedule_once(lambda dt: self.add_media_item(path))
        Clock.schedule_once(lambda dt: MDSnackbar(MDLabel(text=f"Arquivo selecionado: {path}")).open())

    def exit_manager(self, *args):
        self.file_manager.close()

    def add_media_item(self, path):
        media_list = self.ids.media_list
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
    from kivy.base import runTouchApp
    runTouchApp(ProcurarArquivoWidget())