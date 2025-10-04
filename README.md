# Forge SDD Toolkit 🚀

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Forge](https://img.shields.io/badge/Atlassian-Forge-0052CC?logo=atlassian)
![Platform](https://img.shields.io/badge/platform-Jira%20%7C%20Confluence-blue)
![AI](https://img.shields.io/badge/AI-GitHub%20Copilot-purple?logo=github)

> **Specification-Driven Development toolkit for Atlassian Forge apps, powered by AI.**

Desenvolva apps Atlassian Forge de forma estruturada e orientada por especificações, com suporte integrado ao GitHub Copilot para automação inteligente de todo o ciclo de desenvolvimento.

---

## 📖 O que é Specification-Driven Development (SDD)?

**SDD** é uma metodologia de desenvolvimento onde você:

1. **Primeiro especifica** o que quer construir (funcionalidades, requisitos, UX)
2. **Depois planeja** a implementação técnica
3. **Então implementa** seguindo o plano
4. **Finalmente valida** com testes automatizados

**Benefícios:**
- 📝 Documentação como fonte da verdade
- 🤖 IA entende melhor o contexto
- 🎯 Menos retrabalho
- ✅ Implementação mais consistente
- 📊 Rastreabilidade de decisões

---

## ✨ Features

- 🤖 **Integração com GitHub Copilot** - Autocomplete e chat contextualizado
- 📋 **4 Fases Estruturadas** - IDEATE → PLAN → IMPLEMENT → TEST
- 🎨 **Slash Commands Personalizados** - `/forge-ideate`, `/forge-plan`, etc.
- ⚡ **Regras Específicas do Forge** - Limitações, segurança e boas práticas
- 📦 **CLI de Instalação** - Setup automatizado em projetos existentes
- 🗂️ **Organização Automática** - Cada feature em sua própria pasta
- 🔒 **Validações de Segurança** - Prevenção automática de anti-patterns

---

## 🚀 Início Rápido

### 1. Instalar no Projeto

**Pré-requisitos:**
- Python 3.8+
- [uv](https://astral.sh/uv/) instalado
- Projeto Forge existente

```bash
# No diretório do seu projeto Forge
uv run /caminho/para/forge-sdd-toolkit/forge-sdd-cli.py init --here

# Ou instalar CLI globalmente
uv tool install /caminho/para/forge-sdd-toolkit/forge-sdd-cli.py
forge-sdd init --here
```

### 2. Usar os Comandos

**No GitHub Copilot Chat:**

```bash
# Criar especificação
/forge-ideate criar um painel para exibir histórico de mudanças

# Criar plano técnico
/forge-plan

# Implementar código
/forge-implement

# Testar implementação
/forge-test
```

**Ou via scripts bash:**

```bash
./scripts/bash/create-new-feature.sh "nome da funcionalidade"
./scripts/bash/create-implementation-plan.sh
```

### 3. Desenvolver

O GitHub Copilot irá automaticamente:
- Aplicar regras do Forge ao gerar código
- Sugerir componentes corretos (`@forge/react`)
- Validar segurança (`asUser()` vs `asApp()`)
- Adicionar comentários verbosos
- Respeitar limitações da plataforma (timeout 25s, storage 100MB)

---

## 📂 Estrutura do Projeto

```
forge-sdd-toolkit/
├── .github/
│   ├── copilot-instructions.md      # ← Copilot aplica automaticamente
│   └── prompts/                     # ← Slash commands
│       ├── forge-ideate.prompt.md
│       ├── forge-plan.prompt.md
│       ├── forge-implement.prompt.md
│       └── forge-test.prompt.md
│
├── scripts/bash/                     # Automação CLI
├── templates/                        # Templates de documentos
├── forge-sdd-cli.py                 # CLI de instalação
└── forge-specs/                      # Especificações (gerado)
    └── [###-feature-name]/
        ├── feature-spec.md
        ├── implementation-plan.md
        └── test-results.md
```

---

## 🎯 Workflow Completo

### Exemplo: Criar Painel de Issue

```bash
# 1. IDEATE - Criar especificação
/forge-ideate criar um painel lateral que exibe histórico de mudanças de uma issue

# Output: forge-specs/001-painel-historico/feature-spec.md

# 2. PLAN - Planejar implementação
/forge-plan

# Output: forge-specs/001-painel-historico/implementation-plan.md

# 3. IMPLEMENT - Implementar código
/forge-implement

# Copilot cria:
# - src/issue-panel/index.jsx
# - Atualiza manifest.yml
# - Adiciona comentários verbosos

# 4. TEST - Testar localmente
forge tunnel

# Abrir Jira → Issue → Panel aparece

# 5. VALIDATE - Validar e deployar
/forge-test
forge deploy -e development
```

---

## 📚 Documentação

### Limitações da Plataforma Forge

| Limitação | Valor | Impacto |
|-----------|-------|---------|
| ⏱️ **Timeout** | 25s | Functions devem ser rápidas |
| 💾 **Storage** | 100MB | Implementar limpeza de dados |
| 🌐 **Egress** | Declarado | APIs externas no manifest |
| 📦 **Runtime** | Node.js 18.x | Verificar compatibilidade |
| 🔒 **CSP** | Restritivo | Sem inline scripts/styles |

### Regras de Segurança

✅ **Prefira `asUser()`** - Respeita permissões do usuário
```javascript
// ✅ BOM - autorização automática
const response = await api.asUser().requestJira(route`/rest/api/3/issue/${key}`);
```

⚠️ **Use `asApp()` com validação**
```javascript
// ⚠️ Verificar permissões antes
const hasPermission = await checkUserPermission(accountId, 'ADMIN');
if (!hasPermission) throw new Error('Unauthorized');
const response = await api.asApp().requestJira(route`/rest/api/3/project`);
```

### Mais Documentação

- 📖 [Regras Completas](templates/forge-rules.md) - Todas as regras do Forge
- 🔧 [Opções de Integração](INTEGRATION-OPTIONS.md) - Como integrar o toolkit
- 💻 [Guia de Instalação](INSTALL.md) - Instalação detalhada
- 🆘 [Troubleshooting](TROUBLESHOOTING.md) - **Erros comuns e soluções** ⭐
- 🌐 [Atlassian Forge Docs](https://developer.atlassian.com/platform/forge/) - Documentação oficial

---

## 🔧 Comandos Úteis

### Forge CLI

```bash
# Validar
forge lint

# Testar localmente
forge tunnel

# Deploy
forge deploy -e development

# Logs
forge logs -e development

# Testar function
forge function invoke my-function --payload '{"key":"value"}'
```

### Toolkit CLI

```bash
# Instalar em projeto
forge-sdd init --here

# Verificar instalação
forge-sdd check

# Criar feature
./scripts/bash/create-new-feature.sh "nome"
```

---

## 🙏 Acknowledgments

This project was inspired by GitHub's [Spec Toolkit](https://github.com/github/spec-toolkit) approach to specification-driven development. 

**What we borrowed (conceptually):**
- 📝 Four-phase workflow structure (Ideate, Plan, Implement, Test)
- 🤖 AI-assisted prompt engineering approach
- 📂 Organized specification storage methodology

**What's original:**
- ⚡ **Forge-specific implementation rules** - Platform constraints, timeouts, storage limits
- 🏗️ **UI Kit vs Custom UI decision frameworks** - Technology selection guidance
- 🔒 **Atlassian security best practices** - `asUser()` vs `asApp()`, scope minimization
- 🗄️ **Storage patterns** - Entity Properties + Forge Storage strategies
- 📦 **Manifest.yml configuration** - Forge module declarations and validations
- 🤖 **GitHub Copilot integration** - Automatic rule application via `.github/copilot-instructions.md`

While the **methodology** draws inspiration from Spec Toolkit, the **implementation** is entirely focused on the Atlassian Forge ecosystem with platform-specific patterns and constraints.

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/seu-usuario/forge-sdd-toolkit/issues) if you want to contribute.

---

## 📄 License

This project is [MIT](LICENSE) licensed.

---

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ for the Atlassian Forge community**

[![Forge](https://img.shields.io/badge/Built%20for-Atlassian%20Forge-0052CC?style=for-the-badge&logo=atlassian)](https://developer.atlassian.com/platform/forge/)
[![AI Powered](https://img.shields.io/badge/Powered%20by-GitHub%20Copilot-purple?style=for-the-badge&logo=github)](https://github.com/features/copilot)
