# Como Instalar e Testar o Forge SDD Toolkit

## 📦 Instalação

### Opção 1: Via uv (Recomendado)

```bash
# Instalar diretamente do GitHub
uv tool install forge-sdd-toolkit --from git+https://github.com/4-youtest/forge-sdd-toolkit.git

# Verificar instalação
forge-sdd --help
```

### Opção 2: Via pip

```bash
# Instalar diretamente do GitHub
pip install git+https://github.com/4-youtest/forge-sdd-toolkit.git

# Verificar instalação
forge-sdd --help
```

### Opção 3: Clone Local (Desenvolvimento)

```bash
# Clone em diretório separado
cd ~/projects  # ou qualquer lugar fora do projeto Forge
git clone https://github.com/4-youtest/forge-sdd-toolkit.git
cd forge-sdd-toolkit

# Instalar em modo editable
pip install -e .  # ou: uv tool install --editable .

# Verificar instalação
forge-sdd --help
```

---

## 🧪 Testar em um Projeto

### 1. Criar projeto de teste

```bash
# Em um diretório separado
mkdir ~/test-forge-project
cd ~/test-forge-project
```

### 2. Instalar o toolkit no projeto

```bash
# Opção A: Projeto vazio (apenas toolkit)
forge-sdd init --here

# Opção B: Com app Forge existente
forge create --template jira-issue-panel-ui-kit my-test-app
cd my-test-app
forge-sdd init --here
```

### 3. Verificar estrutura criada

```bash
tree -L 3
```

**Deve mostrar:**
```
.
├── .github/
│   ├── copilot-instructions.md
│   └── prompts/
│       ├── forge-ideate.prompt.md
│       ├── forge-implement.prompt.md
│       ├── forge-plan.prompt.md
│       └── forge-test.prompt.md
└── forge-sdd/
    ├── scripts/
    │   └── bash/
    ├── specs/
    └── templates/
```

### 4. Testar comandos

```bash
# Criar uma feature de teste
./forge-sdd/scripts/bash/create-new-feature.sh "minha primeira feature"

# Verificar se foi criada
ls -la forge-sdd/specs/
```

### 5. Testar GitHub Copilot

No VS Code com GitHub Copilot:

1. Abra o projeto de teste
2. Abra o Copilot Chat
3. Digite: `/forge-ideate criar um painel simples`
4. Verifique se o Copilot carrega as instruções corretas

---

## 🔄 Atualizar o Toolkit

### Via uv
```bash
uv tool upgrade forge-sdd-toolkit
```

### Via pip
```bash
pip install --upgrade git+https://github.com/4-youtest/forge-sdd-toolkit.git
```

---

## 🗑️ Desinstalar

### Via uv
```bash
uv tool uninstall forge-sdd-toolkit
```

### Via pip
```bash
pip uninstall forge-sdd-toolkit
```

---

## ⚠️ Importante

- **NÃO instale o toolkit em modo editable (`pip install -e .`) no próprio repositório** do toolkit
- Isso pode poluir o projeto com arquivos `.egg-info`, `build/`, etc.
- Para desenvolvimento, clone em um diretório separado e instale de lá
- Para uso normal, instale direto do GitHub

---

## 🐛 Troubleshooting

### Erro: "command not found: forge-sdd"

**Causa:** CLI não está no PATH

**Solução (uv):**
```bash
# Verificar onde uv instala tools
uv tool list

# Adicionar ao PATH (geralmente ~/.local/bin)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Solução (pip):**
```bash
# Verificar onde pip instala scripts
python -m site --user-base

# Adicionar ao PATH
echo 'export PATH="$(python -m site --user-base)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Erro: "externally-managed-environment"

**Causa:** macOS/Linux protege Python do sistema

**Solução:** Use `uv` (recomendado) ou crie virtual environment:
```bash
python3 -m venv ~/.venvs/forge-sdd
source ~/.venvs/forge-sdd/bin/activate
pip install git+https://github.com/4-youtest/forge-sdd-toolkit.git
```

### Toolkit não atualiza após git pull

**Causa:** Instalação em cache

**Solução:**
```bash
# Forçar reinstalação
pip install --force-reinstall git+https://github.com/4-youtest/forge-sdd-toolkit.git
```
