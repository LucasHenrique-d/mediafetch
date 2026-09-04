MediaFetch

<p align="center">
  <img src="assets/icon.ico" width="120" alt="MediaFetch">
</p>

<h1 align="center">MediaFetch</h1>

<p align="center">
  Aplicativo desktop para download e gerenciamento de mídias.
</p>

<p align="center">
  Desenvolvido em Python + PySide6 para Windows.
</p>

<p align="center">
  <strong>Versão 2.2.0</strong>
</p>

<p align="center">
  <a href="https://github.com/LucasHenrique-d/mediafetch/releases">Releases</a>
  •
  <a href="https://github.com/LucasHenrique-d/mediafetch/issues">Issues</a>
</p>

📌 Sobre o projeto

MediaFetch é uma aplicação desktop desenvolvida em Python para facilitar o download e o gerenciamento de mídias a partir de URLs compatíveis.

O projeto possui uma interface gráfica desenvolvida com PySide6, armazenamento local de configurações, histórico de downloads e um processo completo de empacotamento para distribuição como executável Windows.

O projeto começou como uma aplicação focada em downloads de mídias do Instagram e posteriormente evoluiu para uma identidade mais abrangente, dando origem ao MediaFetch.

✨ Recursos

🎬 Download de mídias através de URLs compatíveis

🔎 Análise da mídia antes do download

🖼️ Visualização de informações e thumbnail

📥 Download com acompanhamento de progresso

📁 Seleção do diretório de download

🕘 Histórico dos downloads

💾 Persistência das configurações locais

🎨 Interface gráfica em modo escuro

🖥️ Aplicação desktop para Windows

📦 Geração de executável através do PyInstaller

🛠️ Instalador Windows através do Inno Setup

📝 Sistema de logs para diagnóstico de erros

🖥️ Interface

O MediaFetch utiliza uma interface gráfica construída com PySide6, com foco em simplicidade, organização e facilidade de utilização.

A identidade visual utiliza uma interface escura com uma paleta baseada em tons de roxo.

Screenshots da aplicação serão adicionados futuramente.

## ⚙️ Tecnologias utilizadas

| Tecnologia    | Finalidade                             |
| ------------- | -------------------------------------- |
| Python        | Linguagem principal                    |
| PySide6       | Interface gráfica                      |
| yt-dlp        | Processamento e download de mídias     |
| Requests      | Requisições HTTP                       |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| PyInstaller   | Geração do executável                  |
| Inno Setup    | Criação do instalador Windows          |

📂 Estrutura do projeto

```
MediaFetch/
│
├── assets/
│ ├── icon.ico
│ └── icon.png
│
├── src/
│ ├── gui/
│ │ └── main_window.py
│ │
│ ├── history.py
│ ├── logger.py
│ ├── resources.py
│ ├── settings.py
│ ├── version.py
│ └── main.py
│
├── .gitignore
├── build.spec
├── build_release.bat
├── installer.iss
├── launcher.py
├── release.bat
├── requirements.txt
└── README.md
```

🚀 Instalação para desenvolvimento
Pré-requisitos

Para executar o projeto a partir do código-fonte, você precisará de:

Windows
Python 3.11 ou superior
Git

Recomenda-se utilizar um ambiente virtual Python.

1. Clonar o repositório

```
git clone https://github.com/LucasHenrique-d/mediafetch.git
```

Entre no diretório:

```
cd mediafetch
```

2. Criar o ambiente virtual

```
python -m venv .venv
```

3. Ativar o ambiente virtual

PowerShell

```
.\.venv\Scripts\Activate.ps1
```

CMD

```
.venv\Scripts\activate.bat
```

4. Instalar as dependências

```
python -m pip install -r requirements.txt
```

5. Executar o MediaFetch

A partir da raiz do projeto:

```
python launcher.py
```

A aplicação será iniciada em uma janela desktop.

📦 Gerando o executável

O projeto possui um processo automatizado para gerar o executável Windows utilizando PyInstaller.

Execute:

```
build_release.bat
```

O script irá:

Verificar o ambiente virtual;
Utilizar o Python do ambiente virtual;
Instalar as dependências;
Verificar o PyInstaller;
Limpar builds anteriores;
Executar o processo de empacotamento;
Gerar o executável MediaFetch.exe.

O resultado será:

```
dist/
└── MediaFetch.exe
```

🏗️ Gerando o instalador

O projeto utiliza Inno Setup para gerar o instalador oficial do Windows.

Depois de garantir que o executável foi gerado corretamente, execute:

```
release.bat
```

O processo irá:

Executar o build de produção;
Gerar MediaFetch.exe;
Localizar o Inno Setup;
Processar o arquivo installer.iss;
Criar o instalador Windows.

O resultado esperado será:

```
installer/
└── MediaFetch-Setup-2.2.0.exe
```

🖥️ Versão para usuários finais

Usuários que não desejam executar o projeto a partir do código-fonte podem utilizar o instalador Windows disponível na seção Releases do GitHub.

Download

As versões publicadas podem ser encontradas em:

https://github.com/LucasHenrique-d/mediafetch/releases

Após a instalação, o aplicativo poderá ser iniciado pelo:

Menu Iniciar;
Atalho da área de trabalho.

💾 Dados locais

O MediaFetch utiliza o diretório local de aplicativos do Windows para armazenar dados da aplicação:

```
%LOCALAPPDATA%\MediaFetch
```

Arquivos utilizados atualmente:

```
settings.json
history.json
app.log
```

settings.json

Armazena as configurações persistentes da aplicação.

history.json

Armazena o histórico dos downloads realizados.

app.log

Armazena informações de execução e erros para auxiliar no diagnóstico.

📝 Sistema de logs

O MediaFetch possui um sistema de logging integrado.

O arquivo de log está localizado em:

%LOCALAPPDATA%\MediaFetch\app.log

O log pode ser utilizado para auxiliar na identificação de problemas durante a execução da aplicação.

🔖 Versão atual

MediaFetch 2.2.0

Status

🟢 Release funcional

A versão atual foi validada através dos seguintes cenários:

Execução através do Python;

Execução através do executável;

Geração do executável com PyInstaller;

Geração do instalador;

Instalação do aplicativo;

Execução após instalação;

Download de mídias;

Histórico de downloads;

Persistência das configurações;

Desinstalação do aplicativo.

🛣️ Roadmap

O MediaFetch continuará evoluindo com novas funcionalidades, melhorias de usabilidade e aprimoramentos técnicos.

Interface e experiência

Melhorias adicionais na interface

Novos elementos visuais

Melhor feedback durante operações

Sistema de notificações

Downloads

Seleção avançada de qualidade

Seleção de formato de mídia

Fila de downloads

Gerenciamento avançado de downloads

Melhor gerenciamento de erros

Histórico

Busca no histórico

Filtros

Organização avançada

Gerenciamento de itens

Plataforma

Atualização automática da aplicação

Suporte ampliado a diferentes fontes de mídia

Melhorias de desempenho

Novos recursos de gerenciamento de mídia

⚠️ Aviso de uso

O MediaFetch é uma ferramenta para download e gerenciamento de mídias.

O usuário é responsável por garantir que possui autorização para baixar, armazenar ou utilizar qualquer conteúdo obtido através da aplicação.

Respeite os direitos autorais, os termos de serviço das plataformas utilizadas e a legislação aplicável.

Os desenvolvedores do MediaFetch não se responsabilizam pelo uso indevido da aplicação.

🤝 Contribuição

Contribuições são bem-vindas.

Para contribuir com o projeto:

1. Faça um fork

Crie uma cópia do projeto na sua conta do GitHub.

2. Clone o seu fork

```
git clone https://github.com/SEU-USUARIO/mediafetch.git
```

3. Crie uma branch

```
git checkout -b feature/minha-feature
```

4. Faça suas alterações

Implemente a funcionalidade ou correção desejada.

5. Faça o commit

```
git add .

git commit -m "feat: adiciona minha feature"
```

6. Envie a branch

```
git push origin feature/minha-feature
```

7. Abra um Pull Request

Descreva as alterações realizadas e aguarde a revisão.

🐛 Reportando problemas

Encontrou um problema?

Antes de abrir uma Issue, verifique se está utilizando a versão mais recente do MediaFetch.

Ao reportar um problema, forneça, sempre que possível:

Versão do MediaFetch;

Versão do Windows;

Descrição do problema;

Passos necessários para reproduzir o problema;

Mensagem de erro;

Informações relevantes presentes no arquivo app.log.

O arquivo de log pode ser encontrado em:

%LOCALAPPDATA%\MediaFetch\app.log

🔐 Segurança

Não envie informações sensíveis em Issues ou Pull Requests.

Caso o arquivo de log contenha informações potencialmente sensíveis, revise seu conteúdo antes de compartilhá-lo publicamente.

📄 Licença

Este projeto ainda não possui uma licença de código aberto definida.

Até que uma licença seja adicionada, todos os direitos sobre o código permanecem reservados ao autor.

👨‍💻 Autor

Luczeraaa

Projeto desenvolvido utilizando:

Python

PySide6

yt-dlp

Requests

PyInstaller

Inno Setup

<p align="center">
  <strong>MediaFetch</strong>
</p>

<p align="center">
  Download. Organize. Gerencie.
</p>
