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

from __future__ import unicode_literals  # unicode by default

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
        self.arquivo = "null.csv"

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

    def abrir_base(self, nome_base):
        """Navega no site do Senado até o 'lindo' sistema de consulta de dados.
        O nome passado é usado para escolher a base que será analisada"""
        print("Navegando...")
        print("    Site do Senado")
        a = 'http://www12.senado.gov.br/orcamento/sigabrasil'
        self.navegador.get(a)
        print("    Escolhendo base e abrindo o 'lindo' sistema de consulta de dados")
        a = 'http://www8d.senado.gov.br/dwweb/autoLogon.html'
        self.navegador.get(a)
        time.sleep(10)
        self.navegador.switch_to.frame('servletBridgeIframe')
        # import IPython; IPython.embed()
        self.navegador.find_element_by_partial_link_text(
            'Página inicial').click()

        # Nessa parte estamos tentando apertar o icone colorido que
        # vai para a tela onde é possível criar um novo documento
        self.navegador.switch_to.frame('iframeHome-76525')
        # O ID mudou, por isso a linha abaixo não funcionou mais...
        # self.navegador.find_element_by_id('id_51').click()
        # Tentando ver pela imagem:
        els = self.navegador.find_elements_by_class_name('CarouselItemImage')
        for el in els:
            if 'WebI_48x48.png' in el.get_attribute('src'):
                el.click()
                break

        self.navegador.switch_to.parent_frame()
        self.navegador.switch_to.frame(6)
        self.navegador.switch_to.frame('webiViewFrame')
        self.navegador.find_element_by_id('IconImg__dhtmlLib_188').click()
        self.navegador.find_element_by_id('basicNaviTab_1_dsTypeBar').click()
        self.navegador.find_element_by_id('OK_BTN_DataSourceTypeDlg').click()
        bases = self.navegador.find_elements_by_class_name('mclM')
        for base in bases:
            if(base.text.find(nome_base) != -1):
                base.click()
                self.navegador.find_element_by_id('OK_BTN_addQueryDlg').click()
                break
        # self.navegador.find_element_by_partial_link_text(base).click()

    def escolher_dados(self, dados):
        """Adiciona os dados passados para serem consultados e executa a
        consulta"""
        # self.navegador.switch_to.frame("webiViewFrame")
        # self.navegador.switch_to.frame("querypanel")

        # id_input = 'outlineTree_0_searchWidget_text'
        print("    Escolhendo dados a serem exportados")
        self.navegador.find_element_by_id(
            "IconImg_outlineTree_0_expandAllIcon").click()
        botoes = self.navegador.find_elements_by_class_name('treeNormal')
        for p in dados:
            # self.navegador.find_element_by_id(id_input).clear()
            # self.navegador.find_element_by_id(id_input).send_keys(p)
            # self.navegador.find_element_by_id("IconImg_iconMenu_icon_objectSearchZoneIcn").click()
            for botao in botoes:
                if botao.text.strip() == p:
                    botao.click()
                    self.navegador.find_element_by_id(
                        "RealBtn_addObjqpZone_0").click()
                    break

        # self.navegador.switch_to.default_content()
        # self.navegador.switch_to.frame("webiViewFrame")
        # self.navegador.switch_to.parent_frame()
        print("    Rodando consulta")
        self.navegador.find_element_by_id("IconImg_Txt_runQuery").click()
        time.sleep(20)

    def baixar_csv(self, pasta):
        """Inicia o download do CSV e aguarda ele terminar"""
        # self.navegador.implicitly_wait(0)
        # import IPython; IPython.embed()

        # Costuma demorar muito para abrir o relatório...
        self.navegador.implicitly_wait(200)

        # Abrir menu de opções de dowloand
        # botoes = self.navegador.find_elements_by_css_selector(
        #     'div[id^="IconImg_iconMenu_icon__dhtmlLib_"]')
        # estilo_botao_baixar_csv = "background-image:url('images/main/galleries/icon16x16gallery1b.png');background-position:0px -672px"
        # for botao in botoes:
        #     estilo = botao.get_attribute('style')
        #     # Sim, vamos procurar o botão certo pelo estilo dele. Tenso...
        #     if estilo.find(estilo_botao_baixar_csv) != -1:
        #         botao.click()
        #         break


        # Escolher CSV
        # botoes = self.navegador.find_elements_by_css_selector(
        #     'div[id^="iconMenu_menu__dhtmlLib_"]')
        # for botao in botoes:
        #     if botao.text.find('Exportar dados para CSV...') != -1:
        #         botao.click()
        #         break

        self.navegador.find_element_by_id(
            "IconImg_iconMenu_icon__dhtmlLib_545").click()
        self.navegador.implicitly_wait(20)
        time.sleep(2)
        self.navegador.find_element_by_id(
            "iconMenu_menu__dhtmlLib_545_span_text__menuAutoId_54").click()
        time.sleep(2)
        self.navegador.find_element_by_id("BtnCImg_csvopOKButton").click()
        time.sleep(20)
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
