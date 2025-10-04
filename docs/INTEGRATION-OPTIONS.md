# Opções de Integração das Regras

## 📊 Comparativo de Abordagens

### ✅ Opção 1: GitHub Copilot Instructions (IMPLEMENTADA)

**Arquivo:** `.github/copilot-instructions.md`

**Como funciona:**
- GitHub Copilot lê automaticamente este arquivo
- Aplica as regras em **todo o projeto**
- Funciona em:
  - Autocomplete de código
  - GitHub Copilot Chat
  - Sugestões inline
  - Geração de código

**Vantagens:**
- ✅ Automático - não precisa referenciar manualmente
- ✅ Sempre ativo durante desenvolvimento
- ✅ Funciona em IDE (VS Code, JetBrains, etc.)
- ✅ Contexto consistente em todo o projeto
- ✅ Integra com slash commands do Copilot

**Desvantagens:**
- ⚠️ Requer GitHub Copilot ativo
- ⚠️ Limitado ao contexto do Copilot (não afeta outros agentes IA)

**Quando usar:**
- Desenvolvimento diário com GitHub Copilot
- Equipe já usa Copilot
- Quer aplicação automática das regras

---

### 📋 Opção 2: Referência Manual nos Prompts

**Arquivos:**
- `templates/manifest-structures.md` (contém estruturas + templates)
- `.github/copilot-instructions.md` (regras técnicas detalhadas)
- Cada prompt referencia explicitamente

**Como funciona:**
- Cada arquivo `.prompt.md` referencia documentos específicos:
  ```markdown
  Consulte `templates/manifest-structures.md` para estruturas e templates
  ```

**Vantagens:**
- ✅ Funciona com qualquer agente IA
- ✅ Controle explícito sobre quando aplicar
- ✅ Pode ter regras diferentes por fase

**Desvantagens:**
- ❌ Manual - precisa lembrar de referenciar
- ❌ Aumenta tokens/contexto em cada execução
- ❌ Não funciona em autocomplete

**Quando usar:**
- Usa outros agentes IA além do Copilot
- Quer controle fino sobre aplicação das regras
- Prompts executados via CLI/scripts

---

### 🔄 Opção 3: Híbrida (RECOMENDADA) ⭐

**Combinação:**
1. `.github/copilot-instructions.md` - Regras técnicas aplicadas automaticamente
2. `templates/manifest-structures.md` - Estruturas obrigatórias + catálogo de templates
3. Prompts específicos - Regras de cada fase

**Estrutura atual:**
```
forge-sdd-toolkit/
├── .github/
│   └── copilot-instructions.md     # ← Copilot aplica automaticamente
├── templates/
│   └── manifest-structures.md      # ← Referência para estruturas/templates
└── prompts/
    ├── forge-ideate.prompt.md      # ← Regras específicas da fase
    ├── forge-plan.prompt.md
    ├── forge-implement.prompt.md
    └── forge-test.prompt.md
```

**Como funciona:**
- **GitHub Copilot:** Usa `.github/copilot-instructions.md` automaticamente
- **Slash commands:** Prompts `.prompt.md` já têm regras específicas da fase
- **Referência técnica:** `manifest-structures.md` consultado quando necessário

**Vantagens:**
- ✅ Melhor de ambos os mundos
- ✅ Flexibilidade máxima
- ✅ Redundância (backup)

---

## 🎯 Recomendação por Cenário

### Cenário 1: "Uso só GitHub Copilot"
**Use:** `.github/copilot-instructions.md` apenas
**Status:** ✅ Já implementado

### Cenário 2: "Uso outros agentes IA (Claude, ChatGPT, etc.)"
**Use:** Opção Híbrida
**Ação:** Manter ambos os arquivos (já temos)

### Cenário 3: "Quero slash commands no Copilot Chat"
**Use:** Arquivos `.prompt.md` em `prompts/`
**Status:** ✅ Já implementado
**Como usar:**
```
# No GitHub Copilot Chat
/specify criar um painel no jira para exibir métricas
```

---

## 🔧 Configuração Atual do Projeto

**Já implementado:**
- ✅ `.github/copilot-instructions.md` - Regras automáticas do Copilot (técnicas detalhadas)
- ✅ `templates/manifest-structures.md` - Estruturas obrigatórias + catálogo de templates
- ✅ `prompts/*.prompt.md` - Regras específicas por fase

**Funciona com:**
- ✅ GitHub Copilot (autocomplete e chat)
- ✅ Slash commands personalizados (via `.prompt.md`)
- ✅ Referência técnica (via `manifest-structures.md`)

---

## 📝 Como Usar os Slash Commands

### 1. Configurar no VS Code

**Extensão necessária:** GitHub Copilot Chat

**Localização dos prompts:**
O Copilot busca arquivos `.prompt.md` em:
- `.github/`
- `prompts/`
- Raiz do projeto

### 2. Usar os comandos

No **GitHub Copilot Chat** (panel lateral):

```bash
# Criar especificação de feature
/forge-ideate criar um painel lateral para exibir histórico de mudanças

# Criar plano técnico
/forge-plan

# Implementar código
/forge-implement

# Testar implementação
/forge-test
```

### 3. Renomear para funcionar como slash commands

**Atualmente os arquivos são:**
- `prompts/forge-ideate.prompt.md`
- `prompts/forge-plan.prompt.md`
- `prompts/forge-implement.prompt.md`
- `prompts/forge-test.prompt.md`

**Para usar como `/forge-ideate`, mover para:**
- `.github/forge-ideate.prompt.md`
- `.github/forge-plan.prompt.md`
- `.github/forge-implement.prompt.md`
- `.github/forge-test.prompt.md`

---

## ⚡ Próximos Passos

### Opção A: Manter estrutura atual
**Prós:** Organização clara, separação de concerns
**Contras:** Slash commands não funcionam automaticamente

### Opção B: Mover prompts para `.github/`
**Prós:** Slash commands funcionam automaticamente
**Contras:** Menos organização (tudo em `.github/`)

### Opção C: Criar links simbólicos
```bash
ln -s ../prompts/forge-ideate.prompt.md .github/forge-ideate.prompt.md
```
**Prós:** Mantém organização E funciona como slash command
**Contras:** Complexidade adicional

---

## 🎓 Resumo

**Pergunta:** "Como as regras serão aplicadas?"

**Resposta:**
1. **Via GitHub Copilot:** `.github/copilot-instructions.md` é aplicado **automaticamente** (regras técnicas detalhadas)
2. **Via prompts:** Cada `.prompt.md` tem suas próprias regras (já distribuídas por fase)
3. **Via referência:** `templates/manifest-structures.md` consultado para estruturas e templates

**Pergunta:** "Onde estão as regras?"

**Resposta:** 
- ✅ **Regras técnicas:** `.github/copilot-instructions.md` (aplicadas automaticamente)
- ✅ **Estruturas:** `templates/manifest-structures.md` (consultado quando necessário)
- ✅ **Regras de fase:** Cada `prompts/*.prompt.md` (específico por etapa)


**Status:** 🎉 **Implementado e funcionando!**
