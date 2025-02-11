from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from assets.storage import salvar_dados, carregar_dados  # Importamos as funções de salvamento

class TelaHorario(Screen):
    dias_input = ObjectProperty(None)
    horas_input = ObjectProperty(None)
    resultado_label = ObjectProperty(None)
    
    def on_enter(self):
        """Carregar a carga horária salva ao entrar na tela."""
        carga_horaria, _ = carregar_dados()
        if carga_horaria > 0:
            self.resultado_label.text = f'Carga Horária Atual: {carga_horaria} horas'

    def aviso_popup(self, titulo, mensagem):
        """Exibe uma mensagem popup de aviso."""
        pop = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(None, None), size=(400, 100),
            padding=(10, 10, 10, 10)
        )
        pop.open()

    def calcular_ch(self):
        """Calcula a carga horária e a salva no arquivo JSON."""
        try:
            dia = int(self.dias_input.text)
            horas_minimas = int(self.horas_input.text)
            carga_horaria = dia * horas_minimas
            self.resultado_label.text = f'Carga Horária: {carga_horaria} horas'
            self.aviso_popup("Atualizado","Carga Horária Atualizada!")
            
            self.manager.get_screen('ciclo').carga_horaria = carga_horaria
            salvar_dados(carga_horaria, self.manager.get_screen("ciclo").materias)
            
        except ValueError:
            self.resultado_label.text = 'Por favor, insira valores válidos.'   
            self.aviso_popup('Error', 'Preencha todos os campos corretamente!')