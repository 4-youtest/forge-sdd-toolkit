# Estruturas Obrigatórias do manifest.yml - Forge

Este documento define as estruturas **OBRIGATÓRIAS** do `manifest.yml` para cada tipo de módulo e tecnologia no Atlassian Forge.

## ⚠️ REGRA CRÍTICA: Estrutura do Manifest

**NUNCA remova ou omita componentes obrigatórios do manifest.yml!**

Tanto **UI Kit 2** quanto **Custom UI** requerem:
- ✅ `resource` - Referência ao código frontend
- ✅ `resolver` com `function` - Backend para o módulo (SEMPRE necessário!)
- ✅ `function` definition - Implementação do resolver
- ✅ `resources` - Definição do recurso frontend

**O resolver é SEMPRE obrigatório** porque o Forge usa ele para:
1. Determinar o tipo de módulo
2. Conectar frontend com backend
3. Habilitar comunicação entre camadas

---

## 1. UI Kit 2 (com @forge/react)

### Estrutura Obrigatória - Jira Issue Panel

```yaml
modules:
  jira:issuePanel:
    - key: my-panel
      resource: main                    # ✅ OBRIGATÓRIO - referencia resources
      resolver:
        function: panel-resolver        # ✅ OBRIGATÓRIO - referencia function
      render: native                    # ✅ OBRIGATÓRIO para UI Kit 2
      title: My Panel

  function:
    - key: panel-resolver               # ✅ OBRIGATÓRIO - backend resolver
      handler: index.run                # ✅ Handler que exporta o resolver

resources:
  - key: main                           # ✅ OBRIGATÓRIO - código frontend
    path: src/index.jsx                 # Caminho do código UI Kit 2

permissions:
  scopes:
    - read:jira-work
```

### Código Backend Obrigatório (src/index.js ou src/index.jsx)

```javascript
import Resolver from '@forge/resolver';
import ForgeReconciler from '@forge/react';
import { App } from './App';

// ✅ OBRIGATÓRIO - Resolver para backend functions
const resolver = new Resolver();

// Registrar funções do resolver se necessário
resolver.define('getData', async (req) => {
  // Lógica backend
  return { data: 'example' };
});

// ✅ OBRIGATÓRIO - Exportar como handler
export const run = resolver.getDefinitions();

// ✅ UI Kit 2 - Render do frontend
ForgeReconciler.render(<App />);
```

### Estrutura Obrigatória - Confluence Global Page

```yaml
modules:
  confluence:globalPage:
    - key: my-global-page
      resource: main
      resolver:
        function: page-resolver         # ✅ OBRIGATÓRIO mesmo sem backend logic
      render: native
      title: My Global Page

  function:
    - key: page-resolver
      handler: index.run

resources:
  - key: main
    path: src/index.jsx

permissions:
  scopes:
    - read:confluence-content.all
```

---

## 2. Custom UI

### Estrutura Obrigatória - Jira Issue Panel

```yaml
modules:
  jira:issuePanel:
    - key: my-custom-panel
      resource: main                    # ✅ OBRIGATÓRIO - referencia resources
      resolver:
        function: panel-resolver        # ✅ OBRIGATÓRIO - NUNCA REMOVA!
      render: native                    # ✅ OBRIGATÓRIO para Custom UI
      title: My Custom Panel

  function:
    - key: panel-resolver               # ✅ OBRIGATÓRIO - backend resolver
      handler: index.handler            # Handler do resolver

resources:
  - key: main                           # ✅ OBRIGATÓRIO - frontend estático
    path: static/                       # Diretório com index.html

permissions:
  scopes:
    - read:jira-work
```

### Estrutura de Arquivos Custom UI

```
my-app/
├── src/
│   ├── index.js           # ✅ OBRIGATÓRIO - Backend com resolver
│   ├── resolvers.js       # Funções backend (opcional)
│   └── frontend/          # Source do frontend (antes do build)
│       ├── index.tsx      # React entry
│       └── App.tsx        # React app
├── static/                # ✅ Gerado por build (npm run build)
│   ├── index.html         # ✅ OBRIGATÓRIO - Entry point
│   └── assets/
│       ├── index-[hash].js
│       └── index-[hash].css
├── vite.config.ts         # ✅ OBRIGATÓRIO com base: './'
├── package.json
└── manifest.yml
```

### ⚠️ CRÍTICO: Configuração do Vite para Custom UI

**SEMPRE adicione `base: './'` no vite.config.ts:**

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',              // ✅ OBRIGATÓRIO - Caminhos relativos para Forge CDN
  build: {
    outDir: 'static',      // Output para static/
    emptyOutDir: true,     // Limpar antes de build
  },
});
```

**Por que `base: './'` é obrigatório:**
- Forge CDN requer caminhos relativos (`./assets/`)
- Sem isso, assets retornam 404 (`/assets/` não resolve)
- Vite gera caminhos absolutos por padrão

**Outras ferramentas:**
- **Webpack:** `publicPath: './'`
- **Create React App:** `"homepage": "."` no package.json

### Código Backend Obrigatório (src/index.js)

```javascript
import Resolver from '@forge/resolver';

// ✅ OBRIGATÓRIO - Criar resolver
const resolver = new Resolver();

// Registrar funções backend que o frontend pode chamar
resolver.define('fetchIssueData', async (req) => {
  const { issueKey } = req.payload;
  // Lógica backend
  return { data: 'example' };
});

// ✅ OBRIGATÓRIO - Exportar como handler
export const handler = resolver.getDefinitions();
```

### Frontend Custom UI (static/index.jsx)

```javascript
import React from 'react';
import { createRoot } from 'react-dom/client';
import { invoke } from '@forge/bridge';

const App = () => {
  const fetchData = async () => {
    // Chamar função do resolver backend
    const result = await invoke('fetchIssueData', { issueKey: 'KEY-1' });
    console.log(result);
  };

  return <button onClick={fetchData}>Fetch Data</button>;
};

createRoot(document.getElementById('root')).render(<App />);
```

---

## 3. Functions/Triggers (Sem UI)

### Estrutura - Product Trigger

```yaml
modules:
  function:
    - key: issue-created-handler
      handler: index.handler

  trigger:
    - key: issue-created-trigger
      function: issue-created-handler
      events:
        - avi:jira:created:issue

permissions:
  scopes:
    - read:jira-work
    - write:jira-work
```

**NÃO requer:**
- ❌ `resource` (sem UI)
- ❌ `resources` section
- ❌ `resolver` (apenas function)

### Estrutura - Web Trigger

```yaml
modules:
  function:
    - key: webhook-handler
      handler: index.handler

  webtrigger:
    - key: my-webhook
      function: webhook-handler

permissions:
  scopes:
    - read:jira-work
```

---

## 4. Checklist de Validação do Manifest

### Para UI Kit 2:

- [ ] Módulo tem `resource` referenciando `resources` section
- [ ] Módulo tem `resolver.function` referenciando `function` section
- [ ] Módulo tem `render: native`
- [ ] `function` section define o resolver handler
- [ ] `resources` section define path do código frontend
- [ ] Backend exporta `resolver.getDefinitions()` como handler
- [ ] Frontend usa `ForgeReconciler.render()` do `@forge/react`

### Para Custom UI:

- [ ] Módulo tem `resource` referenciando `resources` section
- [ ] Módulo tem `resolver.function` referenciando `function` section (**CRÍTICO!**)
- [ ] Módulo tem `render: native`
- [ ] `function` section define o resolver handler
- [ ] `resources` section aponta para diretório `static/`
- [ ] `static/index.html` existe como entry point
- [ ] Backend exporta `resolver.getDefinitions()` como handler
- [ ] Frontend usa `invoke()` do `@forge/bridge` para chamar resolver

### Para Functions/Triggers:

- [ ] `function` section define handler
- [ ] `trigger` ou `webtrigger` referencia a function
- [ ] NÃO tem `resource`, `resources`, ou `resolver` (não precisa)
- [ ] Handler exportado corresponde ao definido no manifest

---

## 5. Erros Comuns e Soluções

### ❌ Erro: "Resolver function not found" durante lint

**Causa:** Removeu `resolver.function` do módulo

**Solução:**
```yaml
# ❌ ERRADO - falta resolver
modules:
  jira:issuePanel:
    - key: my-panel
      resource: main
      render: native
      title: My Panel

# ✅ CORRETO - com resolver
modules:
  jira:issuePanel:
    - key: my-panel
      resource: main
      resolver:
        function: panel-resolver  # OBRIGATÓRIO!
      render: native
      title: My Panel
```

### ❌ Erro: "Resource not defined"

**Causa:** Faltando section `resources` ou key incorreta

**Solução:**
```yaml
# Garantir que key do resource corresponde
modules:
  jira:issuePanel:
    - key: my-panel
      resource: main  # ← Deve corresponder a key em resources

resources:
  - key: main       # ← Mesma key
    path: src/index.jsx
```

### ❌ Erro: Custom UI não carrega

**Causa:** Path do resource não aponta para diretório com `index.html`

**Solução:**
```yaml
# ❌ ERRADO - aponta para arquivo
resources:
  - key: main
    path: static/index.html  # Errado!

# ✅ CORRETO - aponta para diretório
resources:
  - key: main
    path: static/  # Diretório que CONTÉM index.html
```

---

## 6. Regras de Ouro

1. **NUNCA remova o resolver** de módulos UI (UI Kit 2 ou Custom UI)
2. **SEMPRE valide com `forge lint`** após qualquer mudança no manifest
3. **resource + resolver + function** são um **trio obrigatório** para módulos UI
4. **render: native** é obrigatório para UI Kit 2 e Custom UI
5. **Backend SEMPRE exporta** `resolver.getDefinitions()` como handler
6. **Custom UI resources path** SEMPRE aponta para diretório (não arquivo)

---

**Resumo:** O Forge usa o `resolver` para identificar e conectar módulos UI, mesmo que não haja lógica backend customizada. **NUNCA remova componentes obrigatórios do manifest!**
