# SigaLivre


Extrator de dados do SigaBrasil.

## Como assim?

O SigaLivre basicamente é uma receita para Selenium, que é uma biblioteca para interagir com navegadores. Ele abre o navegador e vai clicando.
Passando parâmetros para o SigaLivre ele pode escolher bases e colunas para baixar.
Ele basicamente faz o que você faria clicando na interface do Siga, e no fim clica para baixar os dados em CSV.


## Como usar?

Boa pergunta...

Os comandos abaixo assumem que você sabe usar um terminal GNU/Linux.

### Instalação

Bom, primeiro você vai precisa de Python, algumas dependências dele e de um Firefox.
Acho que ele roda em Python 2 ou 3, mas não tenho certeza...

Em uma distro baseada em Debian seria algo como isso:

    apt-get install python python-virtualenv firefox

Dai você vai para a pasta onde quer colocar o SigaLivre, baixe-o ou via ZIP ou via Git:

    git clone https://github.com/andresmrm/sigalivre.git

Entre na pasta do SigaLivre:

    cd sigalivre

Crie um ambiente virtual Python e instale as dependências:

    virtualenv env
    source env/bin/activate
    pip install selenium
    pip install requests

### Rodar

O SigaLivre basicamente vai entrar na página de "Novo Documento de Web Intelligence" do SigaBrasil e escolher uma base. Na nova página que se abre ele escolhe um conjunto de colunas, gera o relatório e, na página seguinte o exporta em CSV.

A página do documento de "Web Intelligence" é essa:

http://www8a.senado.gov.br/AnalyticalReporting/WebiCreate.do?cafWebSesInit=true&appKind=InfoView&service=/InfoViewApp/common/appService.do&loc=pt&pvl=pt_BR&ctx=standalone&actId=223&containerId=11047961&pref=maxOpageU%3D100%3BmaxOpageUt%3D200%3BmaxOpageC%3D10%3Btz%3DAmerica%2FSao_Paulo%3BmUnit%3Dinch%3BshowFilters%3Dtrue%3BsmtpFrom%3Dtrue%3BpromptForUnsavedData%3Dtrue%3B

Porém, aparentemente você só consegue abri-la se primeiro acessar essa página:

http://www8a.senado.gov.br/dwweb/autoLogon.html

(É, eu adoro esse site...)

Por quê você quer saber qual é a página do documento de "Web Intelligence"? Porque são os nomes das bases listadas lá que você vai precisar passar para o SigaLivre para ele saber qual base abrir.

E depois de escolher a base, na página seguinte, são os nomes das colunas que estão ai que você também vai precisar passar para o SigaLivre.
Nessa segunda página ele vai digitar os nomes das colunas no campos de busca, e (acho) pegar o primeiro que for selecionado.

Ok, como uso o SigaLivre?! Com um código em Python semelhante a esse:

    import sigalivre
    firefox = "/usr/bin/firefox"
    pasta = "/tmp"
    siga = sigalivre.SigaLivre(firefox, pasta)
    base = 'LOA2015 - Despesa Execu'
    dados = ("Ano", u"Mês (Número)", u"Órgão (Cod)", u"Órgão", u"UO (Cod)", "UO", u"Função (Cod)", u"Função", u"Subfunção", u"GND (Cod)", "GND", "Autorizado", "Pago", "RP Pago")
    siga.obter_dados(base, dados)

Ele vai abrir a base que começa com o nome `base`, escolher as colunas `dados` e baixar o CSV na pasta `pasta` usando o binário do Firefox que está em `firefox`.

## E se eu quiser ficar sem a cabeça?

Se você tentar rodar o SigaLivre do jeito que expliquei acima em um servidor, provavelmente vai dar pau, pois servidores não costumam ter "cabeça" (ambiente gráfico).

Como fazer? Bom, você pode usar o Xvfb. Ele cria um X "fantasma". Dai basta colocar o Firefox para rodar dentro desse X fantasma. (macabro, não?)

O pacote do Xvfb muda de nome com distro, no Archlinux é `xorg-server-xvfb`, no Debian é `xvfb` mesmo. Instale-o depois rode o seu extrator de dados do Siga com algo assim:

    echo "Abrindo monitor fantasma"
    Xvfb :10 -ac &
    export DISPLAY=:10
    echo "Ativando virtualenv"
    source env/bin/activate
    echo "Rodando script"
    python meu_script_de_extracao.py
    echo "Desativando virtualenv"
    deactivate
    echo "Matando monitor fantasma"
    pkill Xvfb
    echo "As vezes temos raposas zumbis... Quem sabe assim não mais"
    killall firefox
