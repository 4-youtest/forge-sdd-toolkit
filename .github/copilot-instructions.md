# GitHub Copilot Instructions - Forge SDD Toolkit

Você está trabalhando em um projeto de **Atlassian Forge**. Siga estas regras ao gerar código, sugestões e respostas.

## 🎯 Contexto do Projeto

Este é um toolkit para desenvolvimento orientado por especificações (SDD) em Atlassian Forge, com fases de:
1. **IDEATE** - Criar especificações de funcionalidades
2. **PLAN** - Planejar implementação técnica
3. **IMPLEMENT** - Implementar código
4. **TEST** - Testar e validar

## ⚠️ REGRA CRÍTICA: Criação de Projetos Forge

**NUNCA crie estrutura de projeto Forge manualmente!**

- ❌ **NÃO** crie diretórios `src/`, `manifest.yml`, `package.json` manualmente
- ✅ **SEMPRE** use script de automação ou `forge create` com template apropriado
- ✅ **SEMPRE** verifique se `manifest.yml` existe antes de implementar
- ✅ **SEMPRE** remova `AGENTS.md` após criar app (interfere com toolkit)

**Workflow correto:**

1. **Verificar se projeto existe:**
   ```bash
   ls manifest.yml
   ```

2. **Se NÃO existir, usar script de automação:**
   ```bash
   # Modo não-interativo (para AI)
   scripts/bash/create-forge-app.sh --template <template> --name <app-name> --json

   # Modo interativo (para usuário)
   scripts/bash/create-forge-app.sh
   ```

   **Templates disponíveis:**
   - UI Kit 2: `jira-issue-panel-ui-kit`, `confluence-global-page-ui-kit`, `confluence-macro-ui-kit`
   - Custom UI: `jira-issue-panel-custom-ui`, `confluence-global-page-custom-ui`
   - Functions: `product-trigger`, `webtrigger`, `scheduled-trigger`

   **Após criação, o script retorna JSON:**
   ```json
   {
     "success": true,
     "app_path": "/full/path/my-app",
     "manifest": "/full/path/my-app/manifest.yml",
     "next_steps": ["cd my-app", "npm install", "forge deploy -e development"]
   }
   ```

   **IMPORTANTE:** Remover `AGENTS.md` após criação:
   ```bash
   rm -f AGENTS.md
   ```
   O script `create-forge-app.sh` já faz isso automaticamente, mas se usar `forge create` diretamente, remova manualmente.

3. **Se existir, trabalhar COM a estrutura criada pelo template:**
   - Editar arquivos existentes em `src/`
   - Atualizar `manifest.yml` existente
   - Não recriar estrutura

## ⚡ Limitações da Plataforma Forge (SEMPRE considerar)

- ⏱️ **Timeout:** Functions têm limite de **25 segundos** de execução
- 💾 **Storage:** Limite de **100MB total** por app (Forge Storage)
- 🌐 **Egress:** APIs externas **devem ser declaradas** no manifest.yml
- 📦 **Runtime:** Node.js 19.x (verificar compatibilidade de bibliotecas)
- 🔒 **CSP:** Custom UI tem Content Security Policy restritiva (**sem inline scripts/styles**)

## 🏗️ Escolha de Tecnologia

### UI Kit vs Custom UI

⚠️ **REGRA CRÍTICA: SEMPRE perguntar ao usuário explicitamente!**

**NUNCA assuma a escolha. SEMPRE faça a pergunta:**

```
Esta funcionalidade requer interface de usuário. Escolha uma opção:

1. **UI Kit 2** (Recomendado)
   - ✅ UI consistente com Atlassian
   - ✅ Desenvolvimento mais rápido
   - ⚠️  Menos customização

2. **Custom UI**
   - ✅ Controle total sobre design
   - ✅ Qualquer biblioteca React
   - ⚠️  Mais complexo

Digite 1 ou 2:
```

**AGUARDE a resposta antes de prosseguir!**

### JavaScript vs TypeScript

⚠️ **REGRA CRÍTICA: SEMPRE perguntar ao usuário explicitamente!**

**NUNCA assuma a escolha. SEMPRE faça a pergunta:**

```
Você prefere JavaScript ou TypeScript?

1. **JavaScript** - Simples, prototipagem rápida
2. **TypeScript** - Type safety, projetos complexos

Digite 1 ou 2:
```

**AGUARDE a resposta antes de prosseguir!**

## 💻 Regras de Código

### Comentários (OBRIGATÓRIO)

**SEMPRE use comentários verbosos** suficientes para desenvolvedores intermediários com experiência limitada em Forge:

```javascript
// ✅ BOM - Explica o "por quê"
// Busca dados da issue usando asUser() para manter contexto
// de permissões do usuário atual. Isso é mais seguro que asApp()
// pois a API já implementa verificação de autorização automática.
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}`
);

// ❌ RUIM - Apenas descreve o "o quê"
// Busca issue
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}`
);
```

### Imports & Bibliotecas

#### ⚠️ CRITICAL: UI Kit Versions

**Forge UI Kit 2** (`@forge/react`) é a ÚNICA versão suportada.

**Templates corretos para criar apps:**
```bash
# ✅ CORRETO - Templates UI Kit 2
forge create -t jira-issue-panel-ui-kit my-app
forge create -t confluence-global-page-ui-kit my-app
forge create -t jira-global-page-ui-kit my-app
```

#### Para UI Kit 2 (@forge/react) - USE SEMPRE:

```javascript
// ✅ CORRETO - UI Kit 2 com @forge/react
import ForgeReconciler from '@forge/react';
import { Box, Text, Button, useProductContext } from '@forge/react';

// ✅ Exemplo completo UI Kit 2
const App = () => {
  return (
    <Box padding="space.200">
      <Text>Hello World</Text>
      <Button text="Click me" />
    </Box>
  );
};

ForgeReconciler.render(<App />);

// ❌ ERRADO - NÃO usar React padrão em UI Kit
import React from 'react';
```

⚠️ **UI Kit 2 SOMENTE suporta componentes de `@forge/react`** - importar de outras fontes quebrará o app com erro JSX!

#### Para Custom UI:

```javascript
// ✅ CORRETO - pode usar React e bibliotecas
import React, { useState } from 'react';
import { Button } from '@atlaskit/button';
import { invoke } from '@forge/bridge';

// ❌ EVITAR - inline styles (viola CSP)
<div style={{ color: 'red' }}>Content</div>

// ✅ USAR - CSS Modules
import styles from './styles.module.css';
<div className={styles.container}>Content</div>
```

### Build Tools (Custom UI)

⚠️ **CRÍTICO: Configuração de caminhos para Forge CDN**

**Vite (recomendado) - SEMPRE use `base: './'`:**

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',              // ✅ OBRIGATÓRIO - Caminhos relativos
  build: {
    outDir: 'static',      // Output para static/
  },
});
```

**Sem `base: './'` → Assets retornam 404 no Forge CDN!**

**Outras ferramentas:**
- **Webpack:** `publicPath: './'`
- **CRA:** `"homepage": "."` no package.json

### Segurança

#### asUser() vs asApp()

**SEMPRE prefira `asUser()`:**
- Autorização automática baseada em permissões do usuário
- Mais seguro por padrão

```javascript
// ✅ Preferido - respeita permissões do usuário
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}`
);
```

**Use `asApp()` APENAS quando necessário:**
- E **SEMPRE implemente verificações de autorização explícitas**

```javascript
// ⚠️ Verificar permissões antes de usar asApp()
const hasPermission = await checkUserPermission(accountId, 'ADMIN');
if (!hasPermission) {
  throw new Error('Unauthorized');
}
const response = await api.asApp().requestJira(route`/rest/api/3/project`);
```

#### Minimização de Escopos

**Solicite APENAS escopos estritamente necessários:**

```yaml
# ✅ Escopos mínimos
permissions:
  scopes:
    - read:jira-work  # Ler issues (necessário para painel)

# ❌ Evitar escopos desnecessários
permissions:
  scopes:
    - read:jira-work
    - write:jira-work  # ❌ Não precisa se só lê dados
    - admin:jira-work  # ❌ Nunca sem justificativa clara
```

### Tratamento de Erros (OBRIGATÓRIO)

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

  return await response.json();

} catch (error) {
  // Log detalhado para debugging
  console.error('Error fetching issue:', {
    issueKey,
    error: error.message,
    stack: error.stack
  });

  // Erro amigável para usuário
  throw new Error('Não foi possível carregar os dados da issue.');
}
```

### Logging

**Use console.log estrategicamente para debugging:**

```javascript
// ✅ Logs úteis
console.log('Processing issue:', { issueKey, action: 'update' });
console.log('Validation passed, proceeding with update');
console.error('Update failed:', {
  issueKey,
  error: error.message,
  timestamp: new Date().toISOString()
});
```

⚠️ **Logs são visíveis via `forge logs`** - nunca exponha dados sensíveis

## 🗄️ Armazenamento de Dados

### Entity Properties (PREFERIDO quando possível)

Para dados vinculados a entidades (issues, páginas, projetos):

```javascript
// Salvar em Issue Property
await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}/properties/custom-data`,
  {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ myData: 'value' })
  }
);

// Ler Issue Property
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}/properties/custom-data`
);
const data = await response.json();
```

⚠️ **NÃO há API dedicada do Forge** - use REST APIs do produto

### Forge Storage

Para dados não vinculados a entidades:

```javascript
// Backend resolver (NÃO disponível no frontend)
import { storage } from '@forge/api';

export async function saveData(key, value) {
  await storage.set(key, value);
}

export async function getData(key) {
  return await storage.get(key);
}
```

⚠️ **Limite de 100MB total** - implemente limpeza de dados antigos

## 📝 manifest.yml

### ⚠️ REGRA CRÍTICA: Componentes Obrigatórios

**NUNCA remova ou omita estas partes para módulos UI (UI Kit 2 e Custom UI):**

```yaml
# ✅ ESTRUTURA OBRIGATÓRIA
modules:
  jira:issuePanel:
    - key: my-panel
      resource: main              # ✅ OBRIGATÓRIO
      resolver:
        function: panel-resolver  # ✅ CRÍTICO - NUNCA REMOVA!
      render: native              # ✅ OBRIGATÓRIO
      title: My Panel

  function:
    - key: panel-resolver         # ✅ OBRIGATÓRIO
      handler: index.run

resources:
  - key: main                     # ✅ OBRIGATÓRIO
    path: src/index.jsx
```

**Por que o resolver é SEMPRE obrigatório:**
- Forge usa `resolver` para determinar tipo de módulo
- Mesmo sem lógica backend, o resolver DEVE existir
- Remove-lo causa erro de lint/deploy

**Backend mínimo obrigatório:**
```javascript
import Resolver from '@forge/resolver';
const resolver = new Resolver();
export const run = resolver.getDefinitions();  // OBRIGATÓRIO!
```

**Consulte:** `templates/manifest-structures.md` para todas as estruturas

### SEMPRE validar após alterações:

```bash
forge lint
```

### Se alterar escopos/permissões:

```bash
# 1. Reimplantar
forge deploy --non-interactive -e development

# 2. Reinstalar (upgrade)
forge install --non-interactive --upgrade \
  --site <site-url> \
  --product jira \
  -e development
```

### Exemplo de manifest válido:

```yaml
modules:
  jira:issuePanel:
    - key: my-panel
      function: panel-function
      title: My Panel

  function:
    - key: panel-function
      handler: index.handler

permissions:
  scopes:
    - read:jira-work
    - storage:app
```

### Exceção: jira:entityProperty

⚠️ **NÃO possui propriedade `keyConfigurations`**

```yaml
# ✅ CORRETO
modules:
  jira:entityProperty:
    - key: my-property
      entity: issue
      propertyKey: custom-data
```

## 🧪 Testes e Deploy

### Validação:

```bash
forge lint                    # Validar manifest e código
forge tunnel                  # Testar localmente
forge deploy -e development   # Deploy
forge logs -e development     # Ver logs
```

### Quando reimplantar:

**✅ DEVE reimplantar se:**
- Alterou `manifest.yml`
- Adicionou módulos
- Mudou escopos/permissões

**❌ NÃO precisa se:**
- Mudou apenas código (hot reload no tunnel)

## 🚨 Regras Críticas

1. **SEMPRE** use `@forge/react` para UI Kit (única versão suportada)
2. **NUNCA** importe React padrão em projetos UI Kit
3. **NUNCA** use inline styles em Custom UI (CSP)
4. **NUNCA** use `--no-verify` em deploy
5. **NUNCA** remova `resolver` de módulos UI (obrigatório para UI Kit 2 e Custom UI)
6. **NUNCA** esqueça `base: './'` no vite.config para Custom UI (assets 404 sem isso)
7. **SEMPRE** pergunte explicitamente sobre UI Kit 2 vs Custom UI (não assuma)
8. **SEMPRE** use comentários verbosos
9. **SEMPRE** prefira `asUser()` sobre `asApp()`
10. **SEMPRE** minimize escopos de permissões
11. **SEMPRE** implemente tratamento de erros
12. **SEMPRE** valide com `forge lint` após mudar manifest
13. **SEMPRE** considere limite de 25s em functions
14. **SEMPRE** exporte `resolver.getDefinitions()` como handler em módulos UI

## 📚 Referências

- Estrutura do projeto: `/forge-specs/` contém especificações de features
- Templates: `/templates/` contém templates de especificação e planejamento
- Scripts: `/scripts/bash/` contém automações do toolkit

---

**Ao gerar código ou sugestões, SEMPRE aplique estas regras automaticamente.**
