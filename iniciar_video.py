# iniciar_video.py
# Programa Python usando KivyMD para reproduzir um vídeo automaticamente após seleção via file chooser,
# com interface responsiva que se adapta à tela.
# Quando o vídeo é selecionado, realiza um pré-processamento em uma thread secundária (simulado com delay e verificação).
# Após conclusão, executa o vídeo no player na thread principal usando Clock.schedule_once.
# Usa Clock para pausar o vídeo após 10 segundos de reprodução.

import threading
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

class IniciarVideoApp(MDApp):
    def build(self):
        # Configurar tema do KivyMD
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        # Layout principal responsivo
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Botão para selecionar o vídeo
        select_button = MDRaisedButton(
            text="Selecionar Vídeo",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5},
            on_press=self.abrir_file_chooser
        )
        self.layout.add_widget(select_button)

        # Label para status
        self.status_label = MDLabel(
            text="Aguardando seleção do vídeo...",
            size_hint=(1, 0.1),
            halign="center"
        )
        self.layout.add_widget(self.status_label)

        # Área para o VideoPlayer (inicialmente vazio)
        self.player = None
        self.video_container = BoxLayout(size_hint=(1, 0.8))
        self.layout.add_widget(self.video_container)

        # Tornar a janela responsiva
        Window.bind(on_resize=self.on_window_resize)

        return self.layout

    def abrir_file_chooser(self, instance):
        # Criar o conteúdo do popup com FileChooser
        content = GridLayout(cols=1, spacing=10, padding=10)
        file_chooser = FileChooserListView(filters=['*.mp4', '*.avi', '*.mkv'])  # Filtrar por formatos de vídeo comuns
        content.add_widget(file_chooser)

        # Botão para confirmar seleção
        confirm_button = MDRaisedButton(text="OK", size_hint=(1, 0.1))
        content.add_widget(confirm_button)

        # Popup
        self.popup = Popup(title="Selecione um vídeo", content=content, size_hint=(0.9, 0.9))
        confirm_button.bind(on_press=lambda x: self.selecionar_video(file_chooser.path, file_chooser.selection))
        self.popup.open()

    def selecionar_video(self, path, selection):
        self.popup.dismiss()
        if selection:
            video_path = selection[0]  # Pega o primeiro arquivo selecionado
            self.status_label.text = f"Vídeo selecionado: {video_path}. Iniciando pré-processamento..."
            
            # Iniciar thread secundária para pré-processamento
            thread = threading.Thread(target=self.pre_processamento, args=(video_path,))
            thread.daemon = True
            thread.start()
        else:
            self.status_label.text = "Nenhum vídeo selecionado."

    def pre_processamento(self, video_path):
        # Simular pré-processamento (ex: verificação de arquivo, extração de metadata, etc.)
        # Aqui, usamos time.sleep para simular um processo demorado.
        # Em um caso real, poderia usar libraries como opencv-python para processar frames.
        import time
        time.sleep(5)  # Simula pré-processamento de 5 segundos
        
        # Após conclusão, agendar na thread principal para executar o vídeo
        Clock.schedule_once(lambda dt: self.executar_video(video_path))

    def executar_video(self, video_path):
        # Limpar o container anterior
        self.video_container.clear_widgets()

        try:
            self.player = VideoPlayer(
                source=video_path,
                state='play',  # Inicia automaticamente
                options={'allow_stretch': True, 'keep_ratio': True},
                size_hint=(1, 1)
            )
            self.video_container.add_widget(self.player)

            # Agendar pausa com Clock após 10 segundos
            Clock.schedule_once(self.pausar_video, 10)

            self.status_label.text = "Pré-processamento concluído. Reproduzindo vídeo..."
        except Exception as e:
            self.status_label.text = f"Erro ao carregar o vídeo: {str(e)}"

    def pausar_video(self, dt):
        if self.player:
            self.player.state = 'pause'
            self.status_label.text = "Vídeo pausado após 10 segundos."

    def on_window_resize(self, window, width, height):
        # Ajustar layout para redimensionamento (já responsivo)
        pass

if __name__ == '__main__':
    IniciarVideoApp().run()