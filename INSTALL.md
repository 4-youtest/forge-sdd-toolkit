# Instalação do Forge SDD CLI

Guia de instalação e uso do CLI do Forge SDD Toolkit.

## 📦 Pré-requisitos

### Obrigatórios

- **Python 3.8+**
- **uv** (Python package installer)
  ```bash
  # macOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Windows
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Recomendados (para desenvolvimento Forge)

- **Git**
- **Node.js** (v18+) e **npm**
- **Forge CLI**
  ```bash
  npm install -g @forge/cli
  ```
- **GitHub Copilot** (extensão VS Code)

## 🚀 Instalação

### Opção 1: Uso Direto (sem instalação)

Execute diretamente via `uv run`:

```bash
# Navegar até um projeto Forge
cd meu-projeto-forge

# Navegar até o diretório do toolkit
cd /caminho/para/forge-sdd-toolkit

# Inicializar o toolkit no projeto
uv run forge-sdd-cli.py init --here

# Ou especificar caminho completo
cd meu-projeto-forge
uv run /caminho/para/forge-sdd-toolkit/forge-sdd-cli.py init --here

# Verificar ferramentas instaladas
uv run /caminho/para/forge-sdd-toolkit/forge-sdd-cli.py check
```

### Opção 2: Instalação Global (recomendado)

Instale o CLI globalmente via `uv`:

```bash
# Instalar
uv tool install /caminho/para/forge-sdd-cli.py

# Usar em qualquer lugar
cd meu-projeto-forge
forge-sdd init --here
forge-sdd check
```

**Nota:** O comando instalado será `forge-sdd` (não `forge-sdd-cli`).

### Opção 3: Alias no Shell

Adicione um alias no seu `~/.bashrc` ou `~/.zshrc`:

```bash
# Para uv run (mais simples)
alias forge-sdd='uv run /caminho/completo/para/forge-sdd-toolkit/forge-sdd-cli.py'
```

Depois:

```bash
source ~/.bashrc  # ou ~/.zshrc
cd meu-projeto-forge
forge-sdd init --here
```

## 📖 Comandos Disponíveis

### `forge-sdd init --here`

Inicializa o toolkit no diretório atual (deve ser um projeto Forge).

**Flags:**
- `--here` - Inicializar no diretório atual
- `--no-git` - Não inicializar repositório git
- `--force` - Forçar inicialização mesmo se não for projeto Forge

**Exemplos:**

```bash
# Em um projeto Forge existente
cd meu-app-forge
forge-sdd init --here

# Sem inicializar git
forge-sdd init --here --no-git

# Forçar em diretório não-Forge
forge-sdd init --here --force
```

**O que faz:**
1. ✅ Verifica se é projeto Forge (`manifest.yml`)
2. ✅ Copia estrutura do toolkit:
   - `.github/copilot-instructions.md`
   - `.github/prompts/` (slash commands)
   - `scripts/`, `templates/`, `prompts/` (backup)
3. ✅ Cria diretório `forge-specs/`
4. ✅ Cria guia de uso `README-FORGE-SDD.md`
5. ✅ Torna scripts bash executáveis
6. ✅ Inicializa git (se necessário)

**Estrutura criada:**
```
seu-projeto-forge/
├── .github/
│   ├── copilot-instructions.md
│   └── prompts/              # ← Slash commands aqui!
│       ├── forge-ideate.prompt.md
│       ├── forge-plan.prompt.md
│       ├── forge-implement.prompt.md
│       └── forge-test.prompt.md
├── forge-specs/
├── scripts/bash/
├── templates/
└── prompts/                  # Backup
```

### `forge-sdd check`

Verifica se todas as ferramentas necessárias estão instaladas.

**Exemplo:**

```bash
forge-sdd check
```

**Verifica:**
- ✅ Git
- ✅ Node.js
- ✅ npm
- ✅ Forge CLI

### `forge-sdd version`

Mostra a versão do toolkit.

```bash
forge-sdd version
```

### `forge-sdd help-commands`

Lista todos os slash commands disponíveis para GitHub Copilot.

```bash
forge-sdd help-commands
```

## 🎯 Workflow Completo

### 1. Criar novo app Forge

```bash
# Criar app Forge a partir de template
forge create -t jira-issue-panel-ui-kit meu-app

cd meu-app
```

### 2. Inicializar Forge SDD Toolkit

```bash
# Inicializar toolkit
forge-sdd init --here

# Ou via uvx (sem instalação)
uvx /caminho/para/forge-sdd-cli.py init --here
```

### 3. Verificar ambiente

```bash
forge-sdd check
```

### 4. Usar GitHub Copilot

Abra o projeto no VS Code e use os slash commands:

```
/forge-ideate criar um painel para exibir métricas de sprint
/forge-plan
/forge-implement
/forge-test
```

## 🛠️ Troubleshooting

### Erro: "Not a Forge project"

**Causa:** O diretório atual não tem `manifest.yml`.

**Solução:**
```bash
# Criar app Forge primeiro
forge create -t <template> <app-name>
cd <app-name>
forge-sdd init --here

# Ou forçar inicialização
forge-sdd init --here --force
```

### Erro: "uv: command not found"

**Causa:** `uv` não está instalado.

**Solução:**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Erro: Scripts não executáveis

**Causa:** Permissões incorretas em `scripts/bash/*.sh`.

**Solução:**
```bash
chmod +x scripts/bash/*.sh
```

### Slash commands não aparecem no Copilot

**Causa:** Copilot pode levar alguns segundos para indexar.

**Solução:**
1. Feche e reabra o VS Code
2. Aguarde alguns segundos
3. Digite `/forge` no Copilot Chat para ver sugestões
4. Verifique se arquivos `.prompt.md` estão em `.github/`

## 📚 Próximos Passos

Após instalar o toolkit:

1. 📖 Leia `README-FORGE-SDD.md` no projeto
2. 🎯 Leia `templates/forge-rules.md` para regras completas
3. 💬 Abra GitHub Copilot Chat e digite `/forge-ideate`
4. 🚀 Comece a desenvolver com SDD!

## 🔗 Links Úteis

- **Forge Docs:** https://developer.atlassian.com/platform/forge/
- **GitHub Copilot:** https://github.com/features/copilot
- **uv Docs:** https://github.com/astral-sh/uv

## 🤝 Suporte

Se encontrar problemas:

1. Execute `forge-sdd check` para verificar ambiente
2. Verifique se está em um projeto Forge válido
3. Consulte `README-FORGE-SDD.md` no projeto
4. Revise logs de erro detalhados

---

**Forge SDD Toolkit v1.0.0** 🚀