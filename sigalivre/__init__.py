#!/usr/bin/env python
# coding: utf-8

# -----------------------------------------------------------------------------
# Copyright 2014 Andrés Mantecon Ribeiro Martano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------


import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class SigaLivre(object):

    def __init__(self, firefox, pasta=None):
        """'firefox' é o caminho para o binário do Firefox a ser usado.
        'pasta' é o caminho para a pasta onde salvar os downloads."""
        self.firefox = firefox
        self.pasta = pasta
        self.navegador = None
        # Nome do arquivo baixado do sistema
        self.arquivo = "Novo documento do Web Intelligence.csv"

    def criar_navegador(self):
        """Retorna um navegador firefox configurado para salvar arquivos
        baixados em 'pasta'."""
        print("Configurando e iniciando navegador")
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self.pasta)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "text/csv,application/vnd.ms-excel")
        # O binário do navegador deve estar na pasta firefox
        binary = FirefoxBinary(self.firefox)
        self.navegador = webdriver.Firefox(
            firefox_binary=binary, firefox_profile=fp
        )
        self.navegador.implicitly_wait(20)
        # driver = webdriver.PhantomJS(service_args=['--local-storage-path=/tmp/aaaa'])
        # driver = webdriver.PhantomJS(executable_path='phantomjs-download-support/bin/phantomjs')
        # driver = webdriver.Chrome()

    def abrir_base(self, base):
        """Navega no site do Senado até o 'lindo' sistema de consulta de dados.
        O nome passado é usado para escolher a base que será analisada"""
        print("Navegando...")
        print("    Site do Senado")
        a ='http://www8a.senado.gov.br/dwweb/autoLogon.html'
        self.navegador.get(a)
        # time.sleep(5)
        a = "http://www8a.senado.gov.br/AnalyticalReporting/WebiCreate.do?cafWebSesInit=true&appKind=InfoView&service=/InfoViewApp/common/appService.do&loc=pt&pvl=pt_BR&ctx=standalone&actId=223&containerId=3494812&pref=maxOpageU%3D100%3BmaxOpageUt%3D200%3BmaxOpageC%3D10%3Btz%3DAmerica%2FSao_Paulo%3BmUnit%3Dinch%3BshowFilters%3Dtrue%3BsmtpFrom%3Dtrue%3BpromptForUnsavedData%3Dtrue%3B"
        self.navegador.get(a)
        print("    Escolhendo base e abrindo o 'lindo' sistema de consulta de dados")
        self.navegador.find_element_by_partial_link_text(base).click()

    def escolher_dados(self, dados):
        """Adiciona os dados passados para serem consultados e executa a
        consulta"""
        # time.sleep(5)
        self.navegador.switch_to.frame("webiViewFrame")
        self.navegador.switch_to.frame("querypanel")
        print("    Escolhendo dados a serem exportados")
        for p in dados:
            self.navegador.find_element_by_id("objectSearchZoneTxt").clear()
            self.navegador.find_element_by_id("objectSearchZoneTxt").send_keys(p)
            self.navegador.find_element_by_id("IconImg_iconMenu_icon_objectSearchZoneIcn").click()
            self.navegador.find_element_by_id("theBttnIconaddObjButton").click()
        self.navegador.switch_to.default_content()
        self.navegador.switch_to.frame("webiViewFrame")
        # self.navegador.switch_to.parent_frame()
        print("    Rodando consulta")
        self.navegador.find_element_by_id("IconImg_Txt_runquery").click()
        time.sleep(20)

    def baixar_csv(self, pasta):
        """Inicia o download do CSV e aguarda ele terminar"""
        self.navegador.find_element_by_id("IconImg_Txt_iconMenu_icon_docMenu").click()
        time.sleep(2)
        self.navegador.find_element_by_id("iconMenu_menu_docMenu_span_text_saveDocComputerAs").click()
        time.sleep(2)
        self.navegador.find_element_by_id("saveDocComputerMenu_text_saveCSV").click()
        time.sleep(10)
        # Enquanto ainda existir um arquivo temporário do firefox, esperar
        print("Baixando...")
        while self.arquivo + ".part" in os.listdir(pasta):
            time.sleep(1)
        print("Pronto!")

    def obter_dados(self, base, dados, pasta=None):
        """Obtem dados de base salvando em pasta. Retorna o caminho para o
        arquivo baixado."""
        # Tenta pegar 'pasta' dos parâmetros ou do objeto
        if not pasta:
            pasta = self.pasta
            if not pasta:
                raise "ERRO: Pasta de download não especificada!"
        # Cria a pasta onde baixar
        try:
            os.makedirs(pasta)
        except OSError as erro:
            # Ignora se a pasta já existe
            if erro.errno != 17:
                raise
        # Remove possível arquivo baixado anteriormente
        caminho_arquivo = os.path.join(pasta, self.arquivo)
        try:
            os.remove(caminho_arquivo)
        except OSError as erro:
            # Ignora se arquivo não existe
            if erro.errno != 2:
                raise
        self.criar_navegador()
        self.abrir_base(base)
        self.escolher_dados(dados)
        self.baixar_csv(pasta)
        self.navegador.quit()
        return caminho_arquivo
