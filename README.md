# Forge SDD Toolkit 🚀

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Forge](https://img.shields.io/badge/Atlassian-Forge-0052CC?logo=atlassian)
![AI](https://img.shields.io/badge/AI-GitHub%20Copilot-purple?logo=github)

> **Desenvolva apps Atlassian Forge com IA, seguindo especificações estruturadas.**

Toolkit que integra **GitHub Copilot** ao desenvolvimento de apps Forge, aplicando automaticamente boas práticas, limitações da plataforma e padrões de segurança através de uma metodologia orientada por especificações.

---

## ✨ O que é?

Um conjunto de ferramentas que adiciona ao **GitHub Copilot** conhecimento especializado sobre Atlassian Forge:

- 🎯 **Slash commands personalizados** - `/forge-ideate`, `/forge-plan`, `/forge-implement`, `/forge-test`
- 🤖 **IA com contexto** - Copilot conhece limitações do Forge (timeout 25s, storage 100MB, CSP)
- 🔒 **Segurança automática** - Previne anti-patterns (inline styles, escopos desnecessários)
- 📝 **Workflow estruturado** - Especificação → Planejamento → Implementação → Testes
- ⚡ **Geração de código correta** - Sempre usa `@forge/react` (UI Kit 2), nunca React padrão

---

## �� Para quem é?

### ✅ Ideal se você:
- Usa **GitHub Copilot** e quer aumentar qualidade do código Forge
- Quer **documentação como fonte da verdade** (não código desatualizado)
- Precisa de **rastreabilidade** de decisões técnicas
- Quer que IA gere código **seguindo boas práticas** automaticamente

### ⚠️ Talvez não seja ideal se:
- Não usa GitHub Copilot (toolkit depende dele)
- Prefere codificar direto sem planejamento
- Projeto muito pequeno (overhead pode não compensar)

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- [uv](https://docs.astral.sh/uv/) ou pip
- [GitHub Copilot](https://github.com/features/copilot) ativo

### Via uv (recomendado)

```bash
uv tool install forge-sdd-toolkit --from git+https://github.com/4-youtest/forge-sdd-toolkit.git
```

### Via pip

```bash
pip install git+https://github.com/4-youtest/forge-sdd-toolkit.git
```

---

## 📦 Configurar em um Projeto

```bash
# No diretório do seu projeto Forge (ou diretório vazio)
forge-sdd init --here
```

**Isso cria:**

```
seu-projeto/
├── .github/
│   ├── copilot-instructions.md    # Regras do Forge para o Copilot
│   └── prompts/                   # Slash commands personalizados
│       ├── forge-ideate.prompt.md
│       ├── forge-plan.prompt.md
│       ├── forge-implement.prompt.md
│       └── forge-test.prompt.md
└── forge-sdd/
    ├── scripts/                   # Automações bash
    ├── specs/                     # Suas especificações
    └── templates/                 # Templates de docs
```

---

## 🎮 Como Usar

### 1️⃣ Criar Especificação (IDEATE)

**No GitHub Copilot Chat:**

```
/forge-ideate criar um painel Jira que exibe histórico de mudanças da issue
```

**Copilot vai:**
- Perguntar detalhes (UI Kit ou Custom UI? JavaScript ou TypeScript?)
- Criar especificação em `forge-sdd/specs/001-historico-mudancas/`
- Documentar requisitos, UX e considerações técnicas

---

### 2️⃣ Planejar Implementação (PLAN)

```
/forge-plan
```

**Copilot vai:**
- Ler a especificação criada
- Gerar plano técnico detalhado (arquivos, APIs, estrutura do manifest)
- Considerar limitações do Forge automaticamente

---

### 3️⃣ Implementar Código (IMPLEMENT)

```
/forge-implement
```

**Copilot vai:**
- Criar/editar arquivos seguindo o plano
- Usar `@forge/react` (nunca React padrão)
- Adicionar comentários verbosos
- Aplicar segurança (`asUser()` por padrão)
- Validar manifest.yml

---

### 4️⃣ Testar (TEST)

```
/forge-test
```

**Copilot vai:**
- Sugerir cenários de teste
- Validar com `forge lint`
- Instruir deploy e verificação

---

## 🎨 Exemplo de Workflow

```bash
# 1. Instalar toolkit
uv tool install forge-sdd-toolkit --from git+https://github.com/4-youtest/forge-sdd-toolkit.git

# 2. Criar app Forge
forge create --template jira-issue-panel-ui-kit meu-app
cd meu-app

# 3. Instalar toolkit no projeto
forge-sdd init --here

# 4. Usar Copilot Chat
/forge-ideate painel que calcula story points da sprint
/forge-plan
/forge-implement
/forge-test
```

---

## 🧠 O que o Copilot aprende?

### Regras Aplicadas Automaticamente

| Categoria | O que o Copilot faz |
|-----------|---------------------|
| **UI Kit** | Usa `@forge/react`, nunca `import React` |
| **Custom UI** | Configura `base: './'` no Vite (evita 404 no CDN) |
| **Segurança** | Prefere `asUser()` sobre `asApp()`, minimiza escopos |
| **Performance** | Lembra limite de 25s, sugere otimizações |
| **Storage** | Considera limite 100MB, sugere limpeza de dados antigos |
| **Manifest** | Nunca remove `resolver` de módulos UI |
| **Comentários** | Adiciona explicações verbosas ("por quê", não só "o quê") |

---

## 🔄 Atualizar

```bash
# Via uv
uv tool upgrade forge-sdd-toolkit

# Via pip
pip install --upgrade git+https://github.com/4-youtest/forge-sdd-toolkit.git
```

---

## 🗑️ Desinstalar

### Remover CLI

```bash
# Via uv
uv tool uninstall forge-sdd-toolkit

# Via pip
pip uninstall forge-sdd-toolkit
```

### Remover de um projeto

Apenas delete as pastas:
```bash
rm -rf .github/copilot-instructions.md .github/prompts/ forge-sdd/
```

---

## 📚 Documentação

- [📖 Guia de Instalação](docs/INSTALL.md) - Detalhes sobre instalação e configuração
- [🔌 Opções de Integração](docs/INTEGRATION-OPTIONS.md) - Diferentes formas de usar o toolkit
- [🧪 Como Testar](docs/INSTALL-TEST.md) - Validar instalação em projetos de teste
- [🐛 Troubleshooting](docs/TROUBLESHOOTING.md) - Problemas comuns e soluções

---

## 🤝 Contribuir

Contribuições são bem-vindas! Este projeto é open source sob licença MIT.

```bash
# Clone o repositório
git clone https://github.com/4-youtest/forge-sdd-toolkit.git
cd forge-sdd-toolkit

# Faça suas alterações
# Abra um Pull Request
```

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## 🙋 Suporte

- **Issues:** [GitHub Issues](https://github.com/4-youtest/forge-sdd-toolkit/issues)
- **Discussões:** [GitHub Discussions](https://github.com/4-youtest/forge-sdd-toolkit/discussions)

---

<div align="center">

**Feito com ❤️ para desenvolvedores Atlassian Forge**

[⭐ Star no GitHub](https://github.com/4-youtest/forge-sdd-toolkit) | [📖 Documentação](docs/) | [🐛 Reportar Bug](https://github.com/4-youtest/forge-sdd-toolkit/issues)

</div>
