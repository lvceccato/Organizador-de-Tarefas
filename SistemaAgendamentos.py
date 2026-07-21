from datetime import date
import csv

class Tarefa:

    def __init__(self, nome, categoria, prioridade, data):
        self.__nome = nome
        self.__categoria = categoria
        self.__prioridade = prioridade
        self.__data = data

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, value):
        self.__categoria = value

    @property
    def prioridade(self):
        return self.__prioridade

    @prioridade.setter
    def prioridade(self, value):
        self.__prioridade = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value


class Sistema:

    def __init__(self):
        self.tarefas = []

    # listar tarefas
    def listarTarefa(self):
        return sorted(self.tarefas, key=lambda t: t.data)

    # adicionar tarefa
    def adicionarTarefa(self, nome, dataTexto, prioridade, classificacao):

        partes = dataTexto.split("/")
        dia = int(partes[0])
        mes = int(partes[1])
        ano = int(partes[2])

        dataEntrega = date(ano, mes, dia)

        nova_tarefa = Tarefa(nome, classificacao, prioridade, dataEntrega)
        self.tarefas.append(nova_tarefa)

        return "Tarefa adicionada!"

    # remover tarefa
    def removerTarefa(self, tarefaRemover):

        for t in self.tarefas:
            if tarefaRemover == t.nome:
                self.tarefas.remove(t)
                return "Tarefa removida."

        return "Tarefa não encontrada."

    # urgência
    def verUrgencia(self):

        ordenadas = sorted(self.tarefas, key=lambda t: t.prioridade)

        resultado = []

        for t in ordenadas:

            if t.prioridade == 1:
                urgencia = "MUITO URGENTE"

            elif t.prioridade == 2:
                urgencia = "URGENTE"

            else:
                continue

            resultado.append({
                "nome": t.nome,
                "data": t.data.strftime("%d/%m/%Y"),
                "urgencia": urgencia
            })

        return resultado

    # classificação
    def classificacaoTarefa(self, solicit):

        resultado = []

        for t in self.tarefas:

            if t.categoria == solicit:

                resultado.append({
                    "nome": t.nome,
                    "categoria": t.categoria,
                    "data": t.data.strftime("%d/%m/%Y")
                })

        return resultado

    # salvar CSV
    def salvarArquivo(self):

        if len(self.tarefas) == 0:
            return "Nenhuma tarefa para salvar"

        with open("tarefas.csv", "w", newline="", encoding="utf-8") as arquivo:

            escritor = csv.writer(arquivo)

            escritor.writerow([
                "Nome",
                "Categoria",
                "Prioridade",
                "Data"
            ])

            for t in self.tarefas:
                escritor.writerow([
                    t.nome,
                    t.categoria,
                    t.prioridade,
                    t.data.strftime("%d/%m/%Y")
                ])

        return "Tarefas salvas em tarefas.csv"