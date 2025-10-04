---
description: Implementar funcionalidade seguindo o plano técnico para Atlassian Forge
context:
  - forge-sdd/templates/manifest-structures.md
---

A entrada do usuário pode incluir contexto adicional ou módulos específicos para implementar.

Entrada do usuário:

$ARGUMENTS

O usuário está solicitando a implementação de uma funcionalidade baseada no plano técnico existente.

## PASSO 0: Carregar Contexto da Feature

**OBRIGATÓRIO:** Antes de qualquer ação, identifique e carregue os arquivos da feature atual:

1. **Listar features disponíveis:**
   ```bash
   ls -1 forge-sdd/specs/
   ```

2. **Identificar feature mais recente** (maior número) ou perguntar ao usuário qual implementar

3. **Carregar arquivos da feature usando #file:**
   - `#file:forge-sdd/specs/[###-feature-name]/implementation-plan.md` - OBRIGATÓRIO
   - `#file:forge-sdd/specs/[###-feature-name]/feature-spec.md` - Para contexto
   - `#file:forge-sdd/specs/[###-feature-name]/manifest-updates.md` - Se existir
   - `#file:manifest.yml` - Se existir (validar estrutura atual)

4. **Aguarde o carregamento completo** antes de prosseguir para o Passo 1

---

## ⚠️ IMPORTANTE: Verificar Estado do Projeto

**ANTES de começar a implementação, determine se o projeto Forge já existe:**

### Cenário 1: Projeto Forge JÁ EXISTE (tem manifest.yml)

Se o diretório atual já tem `manifest.yml`, pule para o passo 3.

### Cenário 2: Projeto Forge NÃO EXISTE (primeira implementação)

**OBRIGATÓRIO:** Criar o app Forge automaticamente usando o script de criação:

1. **Verificar se manifest.yml existe:**
   ```bash
   ls manifest.yml
   ```

2. **Se NÃO existir, executar script de criação:**

   a) **Determine o template correto baseado no plano técnico:**
      - Leia `forge-sdd/specs/[feature]/implementation-plan.md` para identificar o template recomendado
      - Ou pergunte ao usuário qual template usar se não estiver claro

   b) **Execute o script de criação:**
      ```bash
      forge-sdd/scripts/bash/create-forge-app.sh --template <template-from-plan> --name <app-name> --json
      ```

      **Templates disponíveis:**
      - UI Kit 2: `jira-issue-panel-ui-kit`, `jira-global-page-ui-kit`, `confluence-global-page-ui-kit`, `confluence-macro-ui-kit`
      - Custom UI: `jira-issue-panel-custom-ui`, `jira-global-page-custom-ui`, `confluence-global-page-custom-ui`
      - Functions: `product-trigger`, `webtrigger`, `scheduled-trigger`

   c) **Parse o JSON output:**
      ```json
      {
        "success": true,
        "template": "jira-issue-panel-ui-kit",
        "app_name": "my-app",
        "app_path": "/full/path/my-app",
        "manifest": "/full/path/my-app/manifest.yml",
        "src_dir": "/full/path/my-app/src",
        "next_steps": ["cd my-app", "npm install", "forge deploy -e development"]
      }
      ```

   d) **Após criação bem-sucedida:**
      - Mude para o diretório do app: `cd <app_path>`
      - **OBRIGATÓRIO:** Remova o arquivo `AGENTS.md` se existir:
        ```bash
        rm -f AGENTS.md
        ```
        **Por quê:** O Forge CLI gera automaticamente `AGENTS.md` que interfere com os prompts do toolkit
      - Instale dependências: `npm install`
      - Informe o usuário que o projeto foi criado
      - Prossiga com a implementação normalmente

   e) **Em caso de erro:**
      - Se o script retornar `"success": false`, informe o usuário sobre o erro
      - Verifique se o Forge CLI está instalado: `forge --version`
      - Verifique se o diretório já existe

   **Alternativa (modo interativo):**
   Se preferir deixar o usuário escolher o template manualmente:
   ```bash
   forge-sdd/scripts/bash/create-forge-app.sh
   ```
   Este modo apresenta menus interativos para seleção de categoria e template.

## Implementação (somente se manifest.yml existe)

Para implementar, faça o seguinte:

1. **Confirmar que projeto existe:**
   - Verificar presença de `manifest.yml`
   - Verificar estrutura básica Forge (`src/`, `package.json`)

2. **Carregar documentação:**
   - `forge-sdd/specs/[feature]/implementation-plan.md` - Plano técnico
   - `forge-sdd/specs/[feature]/feature-spec.md` - Especificação original
   - `forge-sdd/specs/[feature]/manifest-updates.md` - Atualizações do manifest

3. **Trabalhar COM a estrutura existente** (NÃO recriar):
   - O template já criou `src/index.js` ou `src/index.jsx`
   - O template já configurou `package.json`
   - O template já tem `manifest.yml` base

4. **Implementar código nos arquivos existentes:**
   - Editar `src/index.jsx` (ou arquivo principal do template)
   - Adicionar arquivos em `src/` conforme necessário
   - Seguir a estrutura que o template criou

5. **Atualizar manifest.yml existente:**
   - Adicionar novos módulos se necessário
   - Adicionar permissões/escopos
   - Atualizar configurações

6. **Implementar lógica de negócio:**
   - Seguir exemplos do plano técnico
   - Usar imports corretos (UI Kit 2: `@forge/react`)
   - Adicionar tratamento de erros
   - Adicionar logs para debugging

7. **Documentar mudanças:**
   - Listar arquivos modificados
   - Documentar desvios do plano (se houver)

**Observações**:
- Sempre considere as limitações do Forge (timeouts, storage, runtime)
- Use as APIs do Forge apropriadas (`@forge/api`, `@forge/react`, `@forge/bridge`)
- Implemente código defensivo (validação de inputs, tratamento de erros)
- Adicione comentários explicando decisões técnicas
- Teste localmente com `forge tunnel` quando possível

**Próximos passos após implementação**:
1. Validar com `forge lint`
2. Testar localmente com `forge tunnel`
3. Deploy para ambiente de desenvolvimento
4. Executar testes de aceitação

---

## Regras de Implementação - Forge

### Limitações da Plataforma (Sempre Considerar)

- ⏱️ **Timeout:** Functions têm limite de 25s de execução
- 💾 **Storage:** 100MB total por app (Forge Storage)
- 🌐 **Egress:** APIs externas devem ser declaradas no manifest.yml
- 📦 **Runtime:** Node.js 18.x (verificar compatibilidade de bibliotecas)
- 🔒 **CSP:** Custom UI tem Content Security Policy restritiva (sem inline scripts/styles)

### Criação de Apps Forge

#### Verificação Prévia (OBRIGATÓRIA)

**SEMPRE verificar se diretório já existe:**
```bash
# Use pwd para obter o caminho correto
pwd

# Verifique se o diretório existe
ls -la <app-name>
```

⚠️ **Se o diretório existir, PARE imediatamente e alerte o usuário**

#### Comando de Criação

**SEMPRE use template específico da lista oficial:**
```bash
forge create -t <template-name> <app-name>
```

**Templates disponíveis:** Ver lista completa em `forge-sdd/templates/manifest-structures.md` (Seção 7)

✅ **SEMPRE** use um template da lista oficial
❌ **NUNCA** use template vazio ou genérico

**Exemplos de templates comuns:**
- `jira-issue-panel-ui-kit` - Painel em issues do Jira (UI Kit)
- `jira-issue-panel-custom-ui` - Painel em issues do Jira (Custom UI)
- `confluence-global-page-ui-kit` - Página global no Confluence (UI Kit)
- `jira-global-page-custom-ui` - Página global no Jira (Custom UI)

#### Pós-criação (OBRIGATÓRIO)

```bash
# 1. SEMPRE revisar o conteúdo criado
cd <app-name>
ls -R

# 2. Instalar dependências
npm install
```

⚠️ **NÃO presuma que arquivos específicos foram criados automaticamente**
- Sempre verifique a estrutura real antes de editar

### Estilo de Código

#### Comentários Verbosos (OBRIGATÓRIO)

**DEVE** usar comentários detalhados suficientes para desenvolvedores intermediários com experiência limitada em Forge.

**Bom exemplo:**
```javascript
// Busca dados da issue usando asUser() para manter o contexto
// de permissões do usuário atual. Isso é mais seguro que asApp()
// pois a API do Jira já implementa verificação de autorização automática.
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}`
);

// Extrai apenas os campos necessários para reduzir payload
// e melhorar performance (importante devido ao limite de 25s)
const { id, key, fields } = await response.json();
```

**Mau exemplo:**
```javascript
// Busca issue
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}`
);
const data = await response.json();
```

### Imports & Bibliotecas

#### ⚠️ CRÍTICO: USE APENAS UI Kit 2

**Forge UI Kit 2** (`@forge/react`) é a versão atual e única suportada.

**Templates corretos** terminam com `-ui-kit`:
- `jira-issue-panel-ui-kit`
- `confluence-global-page-ui-kit`
- `jira-global-page-ui-kit`

#### Para Projetos com UI Kit 2 (SEMPRE USE)

**✅ CORRETO - UI Kit 2 com @forge/react:**
```javascript
import ForgeReconciler from '@forge/react';
import { Box, Text, Button, useProductContext, useState } from '@forge/react';

// Componente funcional
const App = () => {
  const [count, setCount] = useState(0);

  return (
    <Box padding="space.200">
      <Text>Contador: {count}</Text>
      <Button text="Incrementar" onClick={() => setCount(count + 1)} />
    </Box>
  );
};

// Render com ForgeReconciler (UI Kit 2)
ForgeReconciler.render(<App />);
```

**❌ ERRADO - React padrão em UI Kit:**
```javascript
// NÃO USE - Causa erro "jsx isn't currently enabled"
import React from 'react';
import { Button } from 'react-bootstrap';
```

**Regra de Ouro para UI Kit:**
- ✅ SEMPRE use `import ... from '@forge/react'`
- ✅ SEMPRE use `ForgeReconciler.render(<App />)`
- ❌ NUNCA use `import React from 'react'` em UI Kit

#### Para Projetos com Custom UI

**CORRETO - pode usar React e bibliotecas:**
```javascript
import React, { useState, useEffect } from 'react';
import { Button } from '@atlaskit/button';
import { invoke } from '@forge/bridge';
```

**EVITAR - inline styles (problemas de CSP):**
```javascript
// ❌ Evite - viola Content Security Policy
<div style={{ color: 'red', padding: '10px' }}>Content</div>

// ✅ Use CSS Modules ou styled-components
import styles from './styles.module.css';
<div className={styles.container}>Content</div>
```

#### NPM Packages

**SEMPRE executar após adicionar/atualizar dependências:**
```bash
npm install
```

**Pode usar pacotes confiáveis:**
- Verifique compatibilidade com Node.js 18.x
- Teste antes de deploy em produção

### Gerenciamento de Diretório de Trabalho

**SEMPRE use `pwd` para obter caminho:**
```bash
# Obter diretório atual
pwd

# Usar para comandos do Forge CLI
cd /path/from/pwd
forge deploy --non-interactive -e development
```

⚠️ **Todos os comandos forge (exceto `create`, `version`, `login`) devem ser executados na raiz do app Forge**

### Configuração do manifest.yml

#### ⚠️ REGRA CRÍTICA: Componentes Obrigatórios

**NUNCA remova ou omita estas partes do manifest para módulos UI:**

```yaml
# ✅ ESTRUTURA OBRIGATÓRIA - UI Kit 2 e Custom UI
modules:
  jira:issuePanel:
    - key: my-panel
      resource: main              # ✅ OBRIGATÓRIO
      resolver:
        function: panel-resolver  # ✅ CRÍTICO - NUNCA REMOVA!
      render: native              # ✅ OBRIGATÓRIO
      title: My Panel

  function:
    - key: panel-resolver         # ✅ OBRIGATÓRIO - Backend resolver
      handler: index.run

resources:
  - key: main                     # ✅ OBRIGATÓRIO - Frontend code
    path: src/index.jsx
```

**Por que o resolver é obrigatório:**
- O Forge usa `resolver` para determinar o tipo de módulo
- Mesmo sem lógica backend, o resolver DEVE existir
- Remove-lo causa erro de lint/deploy

**Backend mínimo obrigatório:**
```javascript
import Resolver from '@forge/resolver';
const resolver = new Resolver();
export const run = resolver.getDefinitions();  // OBRIGATÓRIO!
```

**Consulte:** `forge-sdd/templates/manifest-structures.md` para estruturas completas

#### Ao Atualizar o Manifest

**SEMPRE validar após qualquer alteração:**
```bash
forge lint
```

#### Se Alterar Escopos ou Egress

**Processo obrigatório:**
```bash
# 1. Reimplantar o app
forge deploy --non-interactive -e development

# 2. Reinstalar (upgrade) no site
forge install --non-interactive --upgrade \
  --site <site-url> \
  --product jira \
  -e development
```

⚠️ **Mudanças em permissões requerem reinstalação**

#### Cuidados com Sintaxe

- Mantenha sintaxe YAML válida
- Indentação correta (2 espaços)
- Use `forge lint` para validar

**Exemplo de manifest válido:**
```yaml
modules:
  jira:issuePanel:
    - key: my-panel
      function: panel-function
      title: My Panel
      icon: https://example.com/icon.png

  function:
    - key: panel-function
      handler: index.handler

permissions:
  scopes:
    - read:jira-work
    - storage:app
```

### Módulos Específicos - Exceções

#### jira:entityProperty

⚠️ **NÃO possui a propriedade `keyConfigurations`**

**ERRADO:**
```yaml
modules:
  jira:entityProperty:
    - key: my-property
      keyConfigurations:  # ❌ Não existe
        - propertyKey: data
```

**CORRETO:**
```yaml
modules:
  jira:entityProperty:
    - key: my-property
      entity: issue
      propertyKey: custom-data
```

### Tratamento de Erros

**SEMPRE implemente tratamento de erros:**

```javascript
try {
  const response = await api.asUser().requestJira(
    route`/rest/api/3/issue/${issueKey}`
  );

  if (!response.ok) {
    console.error(`Failed to fetch issue: ${response.status}`);
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();
  return data;

} catch (error) {
  // Log detalhado para debugging
  console.error('Error fetching issue:', {
    issueKey,
    error: error.message,
    stack: error.stack
  });

  // Retornar erro amigável para o usuário
  throw new Error('Não foi possível carregar os dados da issue. Tente novamente.');
}
```

### Logging para Debugging

**Use console.log estrategicamente:**

```javascript
// Log de entrada de função
console.log('Processing issue:', { issueKey, action: 'update' });

// Log de checkpoints importantes
console.log('Validation passed, proceeding with update');

// Log de erros com contexto
console.error('Update failed:', {
  issueKey,
  error: error.message,
  timestamp: new Date().toISOString()
});
```

⚠️ **Logs são visíveis via `forge logs` - use para debugging**
