import pandas as pd
from django.core.management.base import BaseCommand
from centroProva.models import CentroProva
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging
import os

# Configuração do logging (modificação para salvar na pasta 'logs')
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_centroProva-log.txt')

logging.basicConfig(
    filename=log_file,  # Nome do arquivo de log dentro da pasta 'logs'
    level=logging.INFO,  # Define o nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa tipos de contato de uma planilha Excel'

    def handle(self, *args, **kwargs):
        # Oculta a janela principal do Tkinter
        Tk().withdraw()
        
        # Solicita ao usuário selecionar a planilha do Excel
        arquivo = askopenfilename(title='Selecione a planilha Excel', filetypes=[('Excel files', '*.xlsx;*.xls')])
        
        if not arquivo:
            self.stdout.write(self.style.ERROR('Nenhum arquivo selecionado.'))
            logging.warning('Nenhum arquivo selecionado.')
            return

        try:
            # Lê o arquivo Excel
            df = pd.read_excel(arquivo)
            logging.info('Arquivo Excel lido com sucesso.')

            # Verificar se a coluna 'id' ou outra chave primária existe
            if 'id' not in df.columns:
                raise ValueError("A coluna 'id' não foi encontrada no arquivo Excel.")

            for index, row in df.iterrows():
                try:
                    # Verificar se o ID está presente e é válido
                    if pd.isna(row['id']) or not isinstance(row['id'], (int, float)):
                        raise ValueError(f"ID inválido na linha {index + 1}")

                    # Preencher os campos do modelo TpContato
                    centro_prova = CentroProva(
                        id=int(row['id']),  # Convertendo ID para inteiro
                        nome=str(row['nome']).strip() if pd.notna(row['nome']) else None,
                        inativo = bool(row['inativo']) if pd.notna(row['inativo']) else False
                    )
                    centro_prova.save()
                    logging.info(f'Centro de Provas {centro_prova.nome} importado com sucesso.')
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar Centro de Provas na linha {index + 1}: {e}"))
                    logging.error(f'Erro ao importar Centro de Provas na linha {index + 1}: {e}')

            self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))
            logging.info('Importação concluída com sucesso!')
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')
