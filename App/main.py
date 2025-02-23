from kivy.core.window import Window
from screens.menu import Menu
from screens.input_materia import InputMateria
from screens.tela_horario import TelaHorario 
from screens.transition_horario import TransitionHorario
from screens.welcome import Welcome
from screens.ciclo import Ciclo
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock  # Importa o Clock para agendar o fechamento do popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget  # Importa o Widget

# Importa a função de carregar dados do JSON
from assets.storage import carregar_dados  

Config.set('graphics', 'height', '1920')
Config.set('graphics', 'width', '1080')

# ScreenManager
class Gerenciador(ScreenManager):
    pass

# App Principal
class MyCicleStudyApp(App):
    def build(self):
        Window.set_icon("App/img/logo.png")
        Builder.load_file('assets/Gerenciador.kv')

        # Criando o ScreenManager e adicionando a tela do menu
        sm = Gerenciador()
        sm.current = 'welcome'

        return sm

    def verificar_e_ir_para_materias(self):
        """Verifica se a carga horária foi definida antes de ir para a tela de matérias."""
        carga_horaria, _, _, _ = carregar_dados()  # Carregar os dados do JSON
        
        if carga_horaria > 0:
            self.root.current = 'materia'  # Vai para a tela de matérias
        else:
            self.mostrar_popup_carregar_horario()  # Exibe o aviso

    def mostrar_popup_carregar_horario(self):
        """Exibe um popup estilizado informando que a carga horária precisa ser definida primeiro."""
        
        # Layout principal do popup
        layout = BoxLayout(orientation="vertical", spacing=20, padding=[20, 20, 20, 20])

        # Mensagem principal
        label = Label(
            text="Antes de adicionar matérias, defina sua carga horária!",
            font_size=20,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=80
        )

        # Layout para centralizar o botão
        button_layout = BoxLayout(size_hint=(1, None), height=50)  # Ocupa toda a largura para centralizar

        # Botão para fechar o popup
        botao_fechar = Button(
            text="Entendido",
            font_size=18,
            size_hint=(None, None),
            size=(180, 50),
            background_color=(0.2, 0.6, 0.8, 1),  # Azul
            color=(1, 1, 1, 1)
        )

        button_layout.add_widget(BoxLayout(size_hint_x=0.5))  # Espaço antes do botão
        button_layout.add_widget(botao_fechar)  # O botão no centro
        button_layout.add_widget(BoxLayout(size_hint_x=0.5))  # Espaço depois do botão

        # Adiciona os widgets ao layout principal
        layout.add_widget(label)
        layout.add_widget(button_layout)

        # Criando o popup
        popup = Popup(
            title="Atenção",
            content=layout,
            size_hint=(None, None),
            size=(550, 250),
            auto_dismiss=True,
            title_align="center"
        )

        botao_fechar.bind(on_release=popup.dismiss)  # Fecha o popup ao clicar no botão

        popup.open()

# Executando o aplicativo
if __name__ == '__main__':
    MyCicleStudyApp().run()
