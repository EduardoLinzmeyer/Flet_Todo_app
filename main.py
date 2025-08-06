import flet as ft


# Classe para criar as tarefas
class Tarefa(ft.Column):
    def __init__(self, nome_tarefa, alt_status_tarefa, del_tarefa):
        super().__init__()
        self.concluida = False
        self.nome_tarefa = nome_tarefa
        self.alt_status_tarefa = alt_status_tarefa
        self.del_tarefa = del_tarefa

        # Cria os controles
        self.exibir_tarefa = ft.Checkbox(
            value=False,
            label=self.nome_tarefa,
            on_change=self.status_alterado
        )

        self.nome_edit = ft.TextField(expand=1, on_submit=self.click_save)

        self.exibir_visual = ft.Row(
            controls=[
                self.exibir_tarefa,
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Editar tarefa",
                            on_click=self.click_edit,
                            icon_color=ft.Colors.GREEN,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            tooltip="Deletar tarefa",
                            on_click=self.click_del,
                            icon_color=ft.Colors.RED,
                        ),
                    ],
                    spacing=0
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.edit_visual = ft.Row(
            visible=False,
            controls=[
                self.nome_edit,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    tooltip="Atualizar tarefa",
                    on_click=self.click_save,
                    icon_color=ft.Colors.GREEN,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Adiciona os controles à coluna principal
        self.controls = [self.exibir_visual, self.edit_visual]
        self.spacing = 10


    def status_alterado(self, e):
        self.concluida = self.exibir_tarefa.value
        self.alt_status_tarefa(self)


    def click_save(self, e):
        if not self.nome_edit.value.strip():
            self.nome_edit.focus()
            return

        self.exibir_tarefa.label = self.nome_edit.value
        self.exibir_visual.visible = True
        self.edit_visual.visible = False
        self.update()


    def click_edit(self, e):
        self.nome_edit.value = self.exibir_tarefa.label
        self.edit_visual.visible = True
        self.nome_edit.focus()
        self.exibir_visual.visible = False
        self.update()


    def click_del(self, e):
        self.del_tarefa(self)



# Classe de criação do app
class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.botao_tema = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            on_click=self.alt_tema,
            tooltip="Alterar Tema",
        )

        self.cor_fundo = ft.Colors.SURFACE
        self.cor_texto = ft.Colors.ON_SURFACE

        # Configuração dos controles
        self.nova_tarefa = ft.TextField(
            hint_text="Qual tarefa deverá ser feita?",
            text_size=16,
            expand=True,
            autofocus=True,
            on_submit=self.add_tarefa
        )

        self.tarefas_listview = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False,
        )

        self.tarefas_container = ft.Container(
            content=self.tarefas_listview,
            height=300,
            expand=True,
        )

        self.filtro = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.alt_tabs,
            tabs=[
                ft.Tab(text="Todas"),
                ft.Tab(text="Ativas"),
                ft.Tab(text="Concluídas")
            ],
            expand=True,
        )

        self.itens_restantes = ft.Text("0 tarefa(s) pendente(s)", opacity=0.5)

        self.selecionar_tudo = ft.Checkbox(
            label="Selecionar tudo",
            on_change=self.alternar_tudo_selecionado,
        )

        self.botao_apagar_tudo = ft.OutlinedButton(
            text="Apagar todas as tarefas concluídas".upper(),
            on_click=self.del_tarefas_concluidas,
            disabled=True
        )

        # Configuração da coluna principal
        self.spacing = 20
        self.expand=True
        self.controls = [
            # Título da aplicação
            ft.Row(
                controls=[
                    ft.Text(value="Tarefas",
                        size=24,
                        weight="bold",
                        expand=True,
                        text_align="center"
                    ),
                    self.botao_tema,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            # Inserção de novas tarefas
            ft.Row(
                controls=[
                    self.nova_tarefa,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        on_click=self.add_tarefa
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            # Filtros e contagem
            ft.Row(
                controls=[
                    ft.Container(
                        content=self.filtro,
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),

            ft.Row(
                controls=[
                    self.selecionar_tudo,
                    self.itens_restantes,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),

            # Lista de tarefas
            self.tarefas_container,

            ft.Row(
                controls=[
                    ft.Container(expand=True),  # Espaço à esquerda
                    self.botao_apagar_tudo,
                    ft.Container(expand=True)  # Espaço à direita
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]


    def alternar_tudo_selecionado(self, e):
        selecionar_tudo = self.selecionar_tudo.value

        for tarefa in self.tarefas_listview.controls:
            if isinstance(tarefa, Tarefa):
                tarefa.exibir_tarefa.value = selecionar_tudo
                tarefa.concluida = selecionar_tudo

                tarefa.update()

        self.atualizar_interface()


    def did_mount(self):
        self.atualizar_cores()


    def atualizar_cores(self):
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.cor_fundo = ft.Colors.SURFACE
            self.cor_texto = ft.Colors.ON_SURFACE
        else:
            self.cor_fundo = ft.Colors.SURFACE
            self.cor_texto = ft.Colors.ON_SURFACE

        self.bgcolor = self.cor_fundo
        self.atualizar_interface()


    def atualizar_interface(self):
        status_filtro = self.filtro.tabs[self.filtro.selected_index].text
        tarefas_pend = 0
        tem_tarefas_visiveis = False
        tem_tarefas_concluidas = False

        # Remove mensagem de lista vazia
        if hasattr(self, 'mensagem_vazia'):
            if self.mensagem_vazia in self.tarefas_listview.controls:
                self.tarefas_listview.controls.remove(self.mensagem_vazia)

        for tarefa in self.tarefas_listview.controls:
            if not isinstance(tarefa, Tarefa):
                continue

            if status_filtro == "Todas":
                tarefa.visible = True
            elif status_filtro == "Ativas":
                tarefa.visible = not tarefa.concluida
            elif status_filtro == "Concluídas":
                tarefa.visible = tarefa.concluida

            if not tarefa.concluida:
                tarefas_pend += 1
            else:
                tem_tarefas_concluidas = True

            if tarefa.visible:
                tem_tarefas_visiveis = True

        # Desabilita botão caso não tenha tarefa concluída
        self.botao_apagar_tudo.disabled = not tem_tarefas_concluidas

        # Adicionar mensagem quando não tem tarefas
        if not tem_tarefas_visiveis:
            self.mensagem_vazia = ft.Text(
                "Nenhuma tarefa nesta aba",
                color=self.cor_texto,
                size=16,
                weight=ft.FontWeight.W_500
            )
            self.tarefas_listview.controls.append(self.mensagem_vazia)

        self.itens_restantes.value = f"{tarefas_pend} tarefa(s) pendente(s)"
        self.update()


    def alt_tema(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.botao_tema.icon = (
            ft.Icons.LIGHT_MODE
            if self.page.theme_mode == ft.ThemeMode.DARK
            else ft.Icons.DARK_MODE
        )
        self.atualizar_cores()
        self.page.update()


    def alt_tabs(self, e):
        self.atualizar_interface()


    def add_tarefa(self, e):
        if not self.nova_tarefa.value.strip():
            self.nova_tarefa.focus()
            return

        if self.nova_tarefa.value:
            tarefa = Tarefa(self.nova_tarefa.value, self.alt_status_tarefa, self.del_tarefa)
            self.tarefas_listview.controls.append(tarefa)
            self.nova_tarefa.value = ''
            self.nova_tarefa.focus()

            self.atualizar_cores()
            self.atualizar_interface()


    def del_tarefas_concluidas(self, e):
        tarefas_para_remover = []

        for tarefa in self.tarefas_listview.controls:
            if isinstance(tarefa, Tarefa) and tarefa.concluida:
                tarefas_para_remover.append(tarefa)

        for tarefa in tarefas_para_remover:
            self.del_tarefa(tarefa)


    def alt_status_tarefa(self, tarefa):
        self.atualizar_interface()


    def del_tarefa(self, tarefa):
        self.tarefas_listview.controls.remove(tarefa)
        self.atualizar_interface()


def main(page: ft.Page):
    page.title = "To Do Tasks"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 550
    page.window.height = 700
        # Permitir/Bloquear maximizar a tela
    page.window.maximizable = False
        # Permitir/Bloquear redimensionamento da janela pelo usuário
    page.window.resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(top=20, bottom=20, left=10, right=10)
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = ft.Colors.SURFACE

    app = TodoApp()
    page.add(app)

    app.atualizar_cores()
    page.update()


ft.app(target=main)
