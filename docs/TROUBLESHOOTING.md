# Troubleshooting - Forge SDD Toolkit

Soluções para erros comuns durante o desenvolvimento com Atlassian Forge.

> **⚠️ Nota:** Este documento menciona UI Kit 1 (`@forge/ui`) **apenas para solução de erros em apps legados**. Para novos projetos, use **sempre UI Kit 2** (`@forge/react`).

---

## 🔴 Erro: "deprecated UI Kit 1 modules"

### Erro Completo
```
Warning: Your app is currently using deprecated UI Kit 1 modules: your-module.
UI Kit 1 has been deprecated on February 28, 2025.
```

### Causa
O app foi criado com ou está usando **UI Kit 1** (`@forge/ui`), que foi depreciado.

### Solução

**Opção 1: Criar novo app com template correto**

```bash
# ❌ NÃO use templates antigos
forge create my-app  # Pode gerar UI Kit 1

# ✅ Use templates UI Kit 2 (com sufixo -ui-kit)
forge create -t jira-issue-panel-ui-kit my-app
forge create -t confluence-global-page-ui-kit my-app
```

**Opção 2: Migrar código existente**

1. Verificar imports no código:

```javascript
// ❌ REMOVER - UI Kit 1
import ForgeUI, { Text, render } from '@forge/ui';

// ✅ ADICIONAR - UI Kit 2
import ForgeReconciler from '@forge/react';
import { Text, Box } from '@forge/react';
```

2. Atualizar render:

```javascript
// ❌ UI Kit 1
render(<Text>Hello</Text>);

// ✅ UI Kit 2
const App = () => <Box><Text>Hello</Text></Box>;
ForgeReconciler.render(<App />);
```

3. Atualizar `manifest.yml`:

```yaml
# Trocar módulos UI Kit 1 por UI Kit 2
modules:
  jira:issuePanel:
    - key: my-panel
      resource: main  # UI Kit 2 usa resources
      resolver:
        function: resolver
      render: native
      title: My Panel

resources:
  - key: main
    path: src/index.jsx  # Código UI Kit 2
```

## 🔴 Erro: "Support for the experimental syntax 'jsx' isn't currently enabled"

### Erro Completo
```
Error: Bundling failed
SyntaxError: Support for the experimental syntax 'jsx' isn't currently enabled

Add @babel/preset-react to the 'presets' section of your Babel config to enable transformation.
```

### Causa
Código JSX sendo usado sem os imports corretos do Forge, ou mistura de UI Kit 1 com sintaxe errada.

### Solução

**1. Verificar imports:**

```javascript
// ❌ ERRADO - Causa erro JSX
import React from 'react';  // Não use em UI Kit!

const App = () => (
  <div>Hello</div>  // Erro: jsx não habilitado
);

// ✅ CORRETO - UI Kit 2
import ForgeReconciler from '@forge/react';
import { Box, Text } from '@forge/react';

const App = () => (
  <Box>
    <Text>Hello</Text>
  </Box>
);

ForgeReconciler.render(<App />);
```

**2. Verificar package.json:**

```json
{
  "dependencies": {
    "@forge/react": "^latest",  // ✅ UI Kit 2
    "@forge/ui": "..."  // ❌ REMOVER se presente
  }
}
```

**3. Reinstalar dependências:**

```bash
rm -rf node_modules package-lock.json
npm install
forge deploy -e development
```

## 🔴 Erro: IA tentando criar estrutura manualmente

### Sintomas
- IA tentando criar `src/`, `manifest.yml`, `package.json` do zero
- Tentando recriar estrutura que o template já criou
- Estrutura de diretórios inconsistente com padrão Forge

### Causa
IA não foi instruída a usar `forge create` ou não verificou se projeto existe.

### Solução

**NUNCA crie projeto Forge manualmente! SEMPRE use `forge create`:**

```bash
# 1. Verificar se projeto existe
ls manifest.yml

# 2. Se NÃO existir, criar com template correto
forge create -t jira-issue-panel-ui-kit my-app
cd my-app

# 3. Agora sim, implementar código
# Editar arquivos que o template criou em src/
# Atualizar manifest.yml existente
```

**Workflow correto:**

```
1. CRIAR APP    → forge create -t <template> <name>
2. IMPLEMENTAR  → Editar src/index.jsx (já existe)
3. DEPLOY       → forge deploy -e development
```

**❌ NÃO faça:**
- Criar `src/index.jsx` do zero (template já criou)
- Criar `manifest.yml` do zero (template já criou)
- Criar `package.json` do zero (template já criou)
- Criar estrutura de diretórios manualmente

**✅ SIM faça:**
- Usar `forge create` com template apropriado
- Editar arquivos que o template criou
- Adicionar novos arquivos em `src/` se necessário
- Atualizar `manifest.yml` existente com novos módulos

**Templates corretos:**
```bash
# UI Kit 2 (recomendado)
forge create -t jira-issue-panel-ui-kit my-app
forge create -t confluence-global-page-ui-kit my-app

# Custom UI
forge create -t jira-issue-panel-custom-ui my-app

# Functions/Triggers
forge create -t product-trigger my-app
```

## 🔴 Problema: IA não pergunta sobre UI Kit vs Custom UI

### Sintomas
- IA escolhe UI Kit 2 automaticamente sem perguntar
- Interface gerada não atende expectativas de customização
- UI "mal feita" ou muito básica (porque foi usado UI Kit 2 quando deveria ser Custom UI)
- Nenhuma pergunta sobre preferência de tecnologia durante `/forge-ideate` ou `/forge-plan`

### Causa
A escolha entre UI Kit 2 e Custom UI não foi explicitamente solicitada ao usuário.

### Impacto
- **UI Kit 2**: Gera interfaces simples e consistentes com Atlassian, mas com limitações de customização
- **Custom UI**: Permite customização total, mas é mais complexo de implementar

### Solução

**Durante `/forge-ideate` (OBRIGATÓRIO):**

A IA DEVE fazer esta pergunta quando detectar que a funcionalidade precisa de UI:

```
Esta funcionalidade requer interface de usuário. Escolha uma opção:

1. **UI Kit 2** (Recomendado)
   - ✅ UI consistente com Atlassian (design system nativo)
   - ✅ Desenvolvimento mais rápido
   - ✅ Menor complexidade
   - ⚠️  Menos flexibilidade para customização avançada

2. **Custom UI**
   - ✅ Controle total sobre design e UX
   - ✅ Pode usar qualquer biblioteca React
   - ✅ Ideal para interfaces complexas/customizadas
   - ⚠️  Mais complexo de implementar
   - ⚠️  Requer conhecimento React avançado

Digite 1 para UI Kit 2 ou 2 para Custom UI:
```

**Durante `/forge-plan` (VALIDAÇÃO):**

A IA DEVE verificar se a escolha foi feita no IDEATE. Se não foi:

```
ERRO: A escolha entre UI Kit 2 e Custom UI não foi especificada no IDEATE.

Por favor, escolha agora:

1. **UI Kit 2** (Recomendado)
   - ✅ UI consistente com Atlassian
   - ✅ Desenvolvimento mais rápido
   - ⚠️  Menos customização

2. **Custom UI**
   - ✅ Controle total sobre design
   - ✅ Qualquer biblioteca React
   - ⚠️  Mais complexo

Qual você prefere? (1 ou 2)
```

**Se a pergunta não foi feita:**

1. **Interrompa o processo atual**
2. **Execute novamente `/forge-ideate`** e responda à pergunta quando for feita
3. **Continue normalmente** com `/forge-plan` e `/forge-implement`

### Prevenção

✅ **SEMPRE** espere a pergunta durante IDEATE
✅ **SEMPRE** responda explicitamente (1 ou 2)
✅ **NUNCA** assuma que a IA escolherá corretamente
✅ **SEMPRE** valide que a escolha está documentada na especificação

### Como Reverter se Escolheu Errado

Se você escolheu UI Kit 2 mas quer Custom UI (ou vice-versa):

**1. Durante IDEATE ou PLAN (antes de implementar):**
```bash
# Simplesmente edite o arquivo de especificação
# forge-specs/[feature]/feature-spec.md
# E atualize a seção de tecnologia
```

**2. Após IMPLEMENT (já criou o app):**
```bash
# Precisa criar novo app com template correto
rm -rf my-app/  # Remover app antigo

# Criar com template Custom UI se era UI Kit 2
forge create -t jira-issue-panel-custom-ui my-app

# Ou criar com template UI Kit 2 se era Custom UI
forge create -t jira-issue-panel-ui-kit my-app

# Executar novamente /forge-implement
```

### Exemplos de Quando Usar Cada Um

**Use UI Kit 2 quando:**
- Quer rapidez no desenvolvimento
- Interface simples (formulários, listagens, botões básicos)
- Quer consistência visual com Jira/Confluence
- Não tem requisitos de design customizado

**Use Custom UI quando:**
- Precisa de design totalmente customizado
- Quer usar bibliotecas React específicas (charts, calendários complexos, etc.)
- Interface complexa com interações avançadas
- Tem designer dedicado com mockups específicos

## 🔴 Erro: "Resolver function not found" ou falha no forge lint

### Sintomas
- `forge lint` falha com erro sobre resolver não encontrado
- Deploy falha com mensagem sobre módulo inválido
- Manifest.yml aparentemente correto mas app não valida

### Erro Típico
```
Error: The resolver function 'panel-resolver' referenced in module 'my-panel' was not found
```

### Causa
O `resolver` foi removido ou omitido do módulo UI no manifest.yml.

**IMPORTANTE:** Tanto UI Kit 2 quanto Custom UI **SEMPRE requerem** o `resolver`, mesmo que não haja lógica backend customizada!

### Por Que o Resolver é Obrigatório

O Forge usa o `resolver` para:
1. **Determinar o tipo de módulo** (UI Kit vs Custom UI vs Function)
2. **Conectar frontend com backend** (mesmo sem lógica customizada)
3. **Habilitar comunicação** entre camadas via `invoke()`

### Solução

**1. Verificar estrutura obrigatória do manifest:**

```yaml
# ✅ CORRETO - Estrutura completa obrigatória
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
      handler: index.run          # ou index.handler para Custom UI

resources:
  - key: main                     # ✅ OBRIGATÓRIO
    path: src/index.jsx           # UI Kit 2
    # ou path: static/            # Custom UI
```

**2. Garantir backend mínimo obrigatório:**

Para UI Kit 2:
```javascript
// src/index.jsx
import Resolver from '@forge/resolver';
import ForgeReconciler from '@forge/react';
import { App } from './App';

// ✅ OBRIGATÓRIO - Criar resolver
const resolver = new Resolver();

// Registrar funções backend (opcional)
resolver.define('getData', async (req) => {
  return { data: 'example' };
});

// ✅ OBRIGATÓRIO - Exportar como handler
export const run = resolver.getDefinitions();

// Render UI Kit 2
ForgeReconciler.render(<App />);
```

Para Custom UI:
```javascript
// src/index.js
import Resolver from '@forge/resolver';

// ✅ OBRIGATÓRIO - Criar resolver
const resolver = new Resolver();

// Registrar funções backend
resolver.define('fetchData', async (req) => {
  return { data: 'example' };
});

// ✅ OBRIGATÓRIO - Exportar como handler
export const handler = resolver.getDefinitions();
```

**3. Validar:**
```bash
forge lint
```

### Checklist de Validação

Para módulos UI (UI Kit 2 ou Custom UI):
- [ ] Módulo tem `resource` (referencia `resources` section)
- [ ] Módulo tem `resolver.function` (referencia `function` section) ← **CRÍTICO!**
- [ ] Módulo tem `render: native`
- [ ] `function` section define o resolver handler
- [ ] `resources` section define path correto
- [ ] Backend importa `Resolver` de `@forge/resolver`
- [ ] Backend exporta `resolver.getDefinitions()` como handler

### Estruturas Completas

Consulte [`templates/manifest-structures.md`](templates/manifest-structures.md) para:
- Estruturas obrigatórias completas por tipo de módulo
- Exemplos de código backend/frontend
- Checklist detalhado de validação

## 🔴 Erro: Assets não carregam em Custom UI (404 em /assets/)

### Sintomas
- Custom UI deploy com sucesso mas interface quebrada
- Console do navegador mostra 404 para `/assets/index-[hash].js`
- CSS e JavaScript não carregam
- Erro típico: `GET https://[forge-cdn]/assets/index-abc123.js 404 (Not Found)`

### Causa
O Vite gera caminhos absolutos (`/assets/`) por padrão, mas o Forge CDN requer caminhos relativos (`./assets/`).

Quando o Forge hospeda Custom UI:
- ❌ `/assets/file.js` → Procura na raiz do CDN (não existe)
- ✅ `./assets/file.js` → Procura relativo ao `index.html` (correto)

### Solução

**Adicionar `base: './'` no `vite.config.ts` ou `vite.config.js`:**

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',  // ✅ CRÍTICO - Usar caminhos relativos para Forge CDN
  build: {
    outDir: 'static',  // Output para static/ (Forge espera isso)
  },
});
```

**Para JavaScript:**
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',  // ✅ CRÍTICO - Caminhos relativos
  build: {
    outDir: 'static',
  },
});
```

**Após adicionar:**
```bash
# Rebuild
npm run build

# Verificar que paths estão relativos
cat static/index.html
# Deve mostrar: <script src="./assets/index-abc123.js">
# NÃO: <script src="/assets/index-abc123.js">

# Deploy novamente
forge deploy -e development
```

### Configuração Completa Recomendada

**vite.config.ts completo para Custom UI:**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',                    // ✅ Caminhos relativos (obrigatório!)
  build: {
    outDir: 'static',            // Output para static/
    emptyOutDir: true,           // Limpar antes de build
  },
  server: {
    port: 3000,                  // Porta dev local
  },
});
```

### Validação

**1. Verificar `index.html` gerado:**
```bash
cat static/index.html | grep -E '(src|href)='
```

Deve mostrar:
```html
<!-- ✅ CORRETO - Caminhos relativos -->
<script type="module" src="./assets/index-abc123.js"></script>
<link rel="stylesheet" href="./assets/index-abc123.css">

<!-- ❌ ERRADO - Caminhos absolutos -->
<script type="module" src="/assets/index-abc123.js"></script>
```

**2. Testar localmente antes de deploy:**
```bash
npm run build
cd static
python3 -m http.server 8000
# Abrir http://localhost:8000 - deve funcionar
```

**3. Deploy e verificar:**
```bash
forge deploy -e development
forge install --site [site-url] --product jira -e development
# Abrir no Jira - assets devem carregar
```

### Estrutura de Arquivos Custom UI Correta

```
my-custom-app/
├── src/
│   ├── index.js           # Backend resolver
│   └── frontend/
│       ├── index.tsx      # React app entry
│       └── App.tsx
├── static/               # ✅ Gerado por Vite
│   ├── index.html        # Entry point (paths relativos!)
│   └── assets/
│       ├── index-[hash].js
│       └── index-[hash].css
├── vite.config.ts        # ✅ Com base: './'
├── package.json
└── manifest.yml
```

### Prevenção

✅ **SEMPRE** adicione `base: './'` em `vite.config.ts` para Custom UI
✅ **SEMPRE** verifique `index.html` antes de deploy
✅ **SEMPRE** teste build local antes de `forge deploy`
✅ **NUNCA** use caminhos absolutos em Custom UI

### Se Não Usar Vite (Webpack, etc.)

**Webpack:**
```javascript
// webpack.config.js
module.exports = {
  output: {
    publicPath: './',  // Caminhos relativos
  },
};
```

**Create React App (CRA):**
```json
// package.json
{
  "homepage": "."
}
```

## 🔴 Erro: "Module build failed from babel-loader"

### Causa
Configuração Babel incompatível ou código JSX sem setup adequado.

### Solução

**Para UI Kit 2:**

Certifique-se de usar APENAS imports de `@forge/react`:

```javascript
// ✅ SEMPRE assim
import ForgeReconciler from '@forge/react';
import { Box, Text, Button, useState, useEffect } from '@forge/react';

// Tudo vem de @forge/react!
```

**Para Custom UI:**

Custom UI pode usar React padrão, mas precisa estar configurado corretamente:

```javascript
// Custom UI frontend (static/)
import React from 'react';
import { createRoot } from 'react-dom/client';

// Usar normalmente
```

## 🔴 Erro: "Cannot find module '@forge/ui'"

### Causa
Tentando usar UI Kit 1 depreciado.

### Solução

```bash
# 1. Atualizar package.json
# Remover: "@forge/ui": "..."
# Adicionar: "@forge/react": "^latest"

# 2. Atualizar código
# Trocar todos os imports de @forge/ui para @forge/react

# 3. Reinstalar
npm install
```

## 🔴 Problema: AGENTS.md interfere com prompts do toolkit

### Sintomas
- Agente AI responde de forma inconsistente ou inesperada
- Instruções do toolkit não são seguidas corretamente
- Comportamento diferente do esperado nos comandos `/forge-*`

### Causa
O Forge CLI gera automaticamente um arquivo `AGENTS.md` na raiz do projeto que contém instruções próprias para agentes de IA, causando conflito com os prompts do Forge SDD Toolkit.

### Solução

**1. Remover AGENTS.md imediatamente após criar app:**

```bash
# Se usar o script do toolkit (remove automaticamente)
scripts/bash/create-forge-app.sh --template jira-issue-panel-ui-kit --name my-app

# Se usar forge create diretamente
forge create -t jira-issue-panel-ui-kit my-app
cd my-app
rm -f AGENTS.md  # ✅ REMOVER imediatamente
```

**2. Se já criou o app e está tendo problemas:**

```bash
# Na raiz do projeto Forge
rm -f AGENTS.md

# Verificar que foi removido
ls -la | grep AGENTS
# Não deve aparecer nada
```

**3. Adicionar ao .gitignore (prevenção):**

```bash
# Na raiz do projeto
echo "AGENTS.md" >> .gitignore
```

### Por Que Remover

**O arquivo `AGENTS.md` do Forge CLI:**
- Contém instruções genéricas para agentes de IA
- **Conflita** com os prompts específicos do toolkit em `.github/prompts/`
- Pode fazer o agente ignorar regras críticas (UI Kit 2, resolver obrigatório, etc.)
- Não é necessário quando se usa o Forge SDD Toolkit

**O Forge SDD Toolkit usa:**
- `.github/prompts/*.prompt.md` - Prompts específicos de cada fase
- `.github/copilot-instructions.md` - Regras automáticas do GitHub Copilot
- `templates/` - Templates de especificação e planejamento

### Prevenção Automática

O script `scripts/bash/create-forge-app.sh` **remove automaticamente** o `AGENTS.md`:

```bash
# ✅ Usa o script do toolkit (recomendado)
scripts/bash/create-forge-app.sh --template jira-issue-panel-ui-kit --name my-app --json
# AGENTS.md é removido automaticamente

# ❌ Se usar forge create diretamente
forge create -t jira-issue-panel-ui-kit my-app
# AGENTS.md é criado - você deve remover manualmente!
```

### Validação

**Verificar que não existe AGENTS.md:**

```bash
# Na raiz do projeto Forge
if [ -f "AGENTS.md" ]; then
    echo "❌ AGENTS.md encontrado - remova com: rm AGENTS.md"
else
    echo "✅ AGENTS.md não existe - OK"
fi
```

### Estrutura Correta

**Arquivos de instruções AI que DEVEM existir:**
```
my-app/
├── .github/
│   ├── copilot-instructions.md   # ✅ Regras do Copilot
│   └── prompts/
│       ├── forge-ideate.prompt.md
│       ├── forge-plan.prompt.md
│       └── forge-implement.prompt.md
├── src/
├── manifest.yml
└── AGENTS.md                      # ❌ NÃO DEVE EXISTIR!
```

## 🟡 Checklist de Prevenção

Ao criar um novo app Forge com UI:

- [ ] **Usar template correto UI Kit 2** (com sufixo `-ui-kit`)
  ```bash
  forge create -t jira-issue-panel-ui-kit my-app
  ```

- [ ] **Verificar imports no código:**
  ```javascript
  // ✅ Deve ter
  import ForgeReconciler from '@forge/react';
  import { Box, Text } from '@forge/react';

  // ❌ NÃO deve ter
  import ForgeUI from '@forge/ui';
  import React from 'react';  // (em UI Kit)
  ```

- [ ] **Verificar render:**
  ```javascript
  // ✅ UI Kit 2
  ForgeReconciler.render(<App />);

  // ❌ UI Kit 1
  render(<App />);
  ```

- [ ] **Testar build antes de implementar:**
  ```bash
  forge lint
  forge deploy -e development
  ```

## 📚 Referências Rápidas

### Templates Corretos UI Kit 2

```bash
# Jira
jira-issue-panel-ui-kit
jira-global-page-ui-kit
jira-issue-action-ui-kit
jira-project-page-ui-kit

# Confluence
confluence-global-page-ui-kit
confluence-macro-ui-kit
confluence-space-page-ui-kit

# Ver todos
forge create --help
```

### Estrutura Básica UI Kit 2

```javascript
// src/index.jsx
import ForgeReconciler from '@forge/react';
import { Box, Text, Button, useState } from '@forge/react';

const App = () => {
  const [count, setCount] = useState(0);

  return (
    <Box padding="space.200">
      <Text>Contador: {count}</Text>
      <Button
        text="Incrementar"
        onClick={() => setCount(count + 1)}
      />
    </Box>
  );
};

ForgeReconciler.render(<App />);
```

## 🆘 Ainda com Problemas?

1. **Limpar e reconstruir:**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   forge deploy -e development
   ```

2. **Verificar versões:**
   ```bash
   forge --version  # Deve ser recente
   node --version   # Deve ser 18.x ou superior
   npm --version
   ```

3. **Ver logs detalhados:**
   ```bash
   forge deploy --verbose -e development
   forge logs -e development
   ```

4. **Consultar documentação oficial:**
   - https://developer.atlassian.com/platform/forge/
   - https://developer.atlassian.com/platform/forge/ui-kit-2/

---

**Regra de Ouro:** Se estiver usando UI Kit, SEMPRE use UI Kit 2 (`@forge/react`)!
