import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.chosen_gene = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_crea_grafo(self, e):
        self.model.build_graph()
        self.view.txt_result.controls.clear()
        nodi, archi = self.model.get_graph_details()
        self.view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nodi} nodi e {archi} archi"))
        self.fill_dd()
        self.view.update_page()
        
    def fill_dd(self):
        for gene in self.model.graph.nodes:
            self.view.dd_geni.options.append(ft.dropdown.Option(data=gene, text=gene, on_click=self.choose_gene))
    
    def choose_gene(self, e):
        if e.control.data is None:
            self.chosen_gene = None
        self.chosen_gene = e.control.data

    def handle_adiacenti(self, e):
        if self.chosen_gene is None:
            self.view.create_alert("Selezionare un gene")
            return
        sorted_neighbors = self.model.get_sorted_neighbors(self.chosen_gene)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Adiacenti a {self.chosen_gene}:"))
        for n in sorted_neighbors:
            self.view.txt_result.controls.append(ft.Text(f"{n[0]}, {n[1]}"))
        self.view.update_page()

    def handle_simulazione(self, e):
        pass

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
