---
description: Transformar especificação de funcionalidade em plano técnico de implementação para Atlassian Forge
scripts:
  sh: scripts/bash/create-implementation-plan.sh --json "{ARGS}"
---

A entrada do usuário para você pode ser fornecida diretamente pelo agente ou como um argumento de comando — você **DEVE** considerá-la antes de prosseguir com o prompt (se não estiver vazia).

Entrada do usuário:

$ARGUMENTS

O usuário está solicitando a criação de um plano técnico de implementação baseado em uma especificação existente. A branch/feature pode ser especificada ou você deve usar a branch atual.

Dada essa solicitação, faça o seguinte:

1. Execute o script `{SCRIPT}` para obter BRANCH_NAME, SPEC_FILE e PLAN_FILE. O script identificará a feature atual.
  **IMPORTANTE** Execute esse script apenas uma única vez. O JSON é fornecido no terminal como saída.
2. Carregue SPEC_FILE para entender os requisitos da funcionalidade
3. Carregue `templates/plan-template.md` para entender a estrutura do plano técnico
4. Crie o plano técnico em PLAN_FILE, incluindo:
   - **Arquitetura Forge**: Estrutura de diretórios, módulos, funções
   - **Implementação de Módulos**: Código específico para cada módulo Forge
   - **Configuração do Manifest**: Detalhamento completo do manifest.yml
   - **APIs e Integrações**: Quais APIs do Forge/Atlassian serão usadas
   - **Storage e Estado**: Como dados serão armazenados (Forge Storage, Properties API)
   - **Testes**: Estratégia de testes para apps Forge
   - **Deploy**: Processo de deploy com forge-cli

**Observações**:
- O plano deve ser técnico e específico para Atlassian Forge
- Considere sempre as limitações da plataforma
- Inclua exemplos de código quando relevante
- Referencie a documentação oficial do Forge quando apropriado

---

## Regras de Planejamento - Forge

### Limitações da Plataforma (Sempre Considerar)

- ⏱️ **Timeout:** Functions têm limite de 25s de execução
- 💾 **Storage:** 100MB total por app (Forge Storage)
- 🌐 **Egress:** APIs externas devem ser declaradas no manifest.yml
- 📦 **Runtime:** Node.js 18.x (verificar compatibilidade de bibliotecas)
- 🔒 **CSP:** Custom UI tem Content Security Policy restritiva (sem inline scripts/styles)

### Escolha de Tecnologia

#### UI Kit vs Custom UI

**⚠️ IMPORTANTE: Se escolher UI Kit, use APENAS UI Kit 2!**

**UI Kit 2** (`@forge/react`) - **Recomendado para:**
- Projetos simples a médios
- Usuários com baixo/médio conhecimento em Forge
- Necessidade de consistência com UI nativa do Atlassian
- Time de desenvolvimento reduzido
- Menor complexidade de deploy

**Templates corretos UI Kit 2:**
```bash
# ✅ Use estes templates (UI Kit 2)
jira-issue-panel-ui-kit
jira-global-page-ui-kit
confluence-global-page-ui-kit
confluence-macro-ui-kit
```

**❌ NUNCA use:**
- Templates antigos sem sufixo `-ui-kit`
- UI Kit 1 (`@forge/ui`) - DEPRECIADO desde 28/Fev/2025

**Custom UI** - Recomendado para:
- Projetos complexos com UI altamente customizada
- Usuários com conhecimento avançado em React
- Necessidade de bibliotecas React específicas de terceiros
- Maior controle sobre UX e comportamento
- Requisitos de performance específicos

**Templates Custom UI:**
```bash
# Custom UI com React completo
jira-issue-panel-custom-ui
confluence-global-page-custom-ui
```

⚠️ **CRÍTICO para Custom UI: Configuração do Build Tool**

**Se usar Vite (recomendado), SEMPRE adicione `base: './'`:**

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',              // ✅ OBRIGATÓRIO - Caminhos relativos para Forge CDN
  build: {
    outDir: 'static',      // Output para static/
    emptyOutDir: true,
  },
});
```

**Por que é obrigatório:**
- Forge CDN requer caminhos relativos (`./assets/`)
- Vite gera caminhos absolutos (`/assets/`) por padrão → 404
- Sem `base: './'`, assets não carregam após deploy

**Outras ferramentas:**
- **Webpack:** `publicPath: './'` no webpack.config.js
- **Create React App:** `"homepage": "."` no package.json

⚠️ **VALIDAÇÃO OBRIGATÓRIA:**

1. **Verificar se a escolha já foi feita no IDEATE:**
   - Leia o arquivo `feature-spec.md` da feature
   - Procure pela seção que especifica UI Kit 2 ou Custom UI

2. **Se a escolha NÃO estiver clara ou NÃO foi feita:**
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

   **AGUARDE a resposta antes de continuar o planejamento!**

3. **Após obter a escolha, atualize o plano técnico de acordo**

#### JavaScript vs TypeScript

**JavaScript:**
- Projetos simples
- Prototipagem rápida
- Usuários com baixo conhecimento
- Apps de escopo pequeno

**TypeScript (com tipagem forte):**
- Projetos médios a complexos
- Equipes múltiplas ou colaboração
- Apps com manutenção de longo prazo
- Necessidade de documentação implícita via tipos
- Refatorações frequentes

⚠️ **VALIDAÇÃO OBRIGATÓRIA:**

1. **Verificar se a escolha já foi feita no IDEATE:**
   - Leia o arquivo `feature-spec.md` da feature
   - Procure pela seção que especifica JavaScript ou TypeScript

2. **Se a escolha NÃO estiver clara:**
   ```
   Você prefere JavaScript ou TypeScript para este projeto?

   1. **JavaScript** - Mais simples, prototipagem rápida
   2. **TypeScript** - Type safety, melhor para projetos complexos

   Digite 1 ou 2:
   ```

   **AGUARDE a resposta antes de continuar!**

### Arquitetura de Dados

#### Opções de Armazenamento

**1. Entity Properties** (recomendado quando possível):
- **Uso:** Dados vinculados a entidades específicas (issues, páginas, projetos, etc.)
- **Jira:** Issue Properties, Project Properties, User Properties, etc.
- **Confluence:** Content Properties
- **Acesso:** Via REST APIs específicas do produto (NÃO há API dedicada no Forge)
- **Vantagens:** Dados vinculados ao ciclo de vida da entidade
- **Limitações:** Dependente da entidade existir

**Exemplo de acesso (Jira Issue Properties):**
```javascript
// Salvar propriedade
await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}/properties/custom-data`,
  {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ myData: 'value' })
  }
);

// Ler propriedade
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}/properties/custom-data`
);
const data = await response.json();
```

**2. Forge Storage:**
- **Forge SQL:** Para consultas relacionais complexas
- **Forge Key-Value Storage:** Para dados simples chave-valor
- **Forge Custom Entities:** Para modelos de dados estruturados
- **Acesso:** Via resolvers backend com `asApp()` (NÃO há API no frontend)
- **Vantagens:** Não dependente de entidades, maior flexibilidade
- **Limitações:** 100MB total, apenas backend

**Exemplo (Key-Value Storage):**
```javascript
// Backend resolver
import { storage } from '@forge/api';

export async function saveData(key, value) {
  await storage.set(key, value);
}

export async function getData(key) {
  return await storage.get(key);
}
```

#### Chamadas de API - Estratégia

**Frontend (simples):**
- Use `requestJira/requestConfluence` do `@forge/bridge`
- Para operações CRUD diretas
- Quando não há lógica de negócio complexa

**Exemplo:**
```javascript
import { invoke } from '@forge/bridge';

// Chamar API diretamente do frontend
const response = await invoke('requestJira',
  `/rest/api/3/issue/${issueKey}`
);
```

**Backend (complexo):**
- Use resolvers com validação
- Para múltiplas chamadas de API
- Lógica de negócio complexa
- Processamento de dados sensíveis

**Exemplo:**
```javascript
// Backend resolver
export async function processIssue(issueKey) {
  // Múltiplas validações e chamadas
  const issue = await fetchIssue(issueKey);
  const validated = await validateData(issue);
  const processed = await processData(validated);
  return processed;
}
```

### Segurança

#### asUser() vs asApp()

**Prefira `asUser()`:**
- Operações no contexto do usuário atual
- Autorização automática baseada em permissões do usuário
- Mais seguro por padrão
- Recomendado para a maioria dos casos

**Exemplo:**
```javascript
// Respeita permissões do usuário
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}`
);
```

**Use `asApp()` com cuidado:**
- Quando precisa de permissões elevadas
- Para operações de sistema/admin
- **SEMPRE implemente verificações de autorização explícitas**
- Use APIs de permissões do produto para validar acesso

**Exemplo:**
```javascript
// Verificar permissões antes de usar asApp()
const hasPermission = await checkUserPermission(accountId, 'ADMIN');
if (!hasPermission) {
  throw new Error('Unauthorized');
}

// Só então usar asApp()
const response = await api.asApp().requestJira(
  route`/rest/api/3/project`
);
```

#### Minimização de Escopos

**Princípio:** Solicite apenas os escopos estritamente necessários

**Liste e justifique:**
| Escopo | Justificativa | Módulos que usam |
|--------|---------------|------------------|
| `read:jira-work` | Ler dados de issues para exibir no painel | `issue-panel` |
| `write:jira-work` | Atualizar status da issue via action | `issue-action` |
| `storage:app` | Persistir configurações do usuário | `global-settings` |

**Evite:**
- ❌ Escopos amplos sem necessidade
- ❌ Pedir `write` quando só precisa `read`
- ❌ Escopos "por precaução" ou "para o futuro"

### Estrutura do manifest.yml (CRÍTICO)

⚠️ **REGRA OBRIGATÓRIA: NUNCA remova componentes obrigatórios do manifest!**

**Para módulos com UI (UI Kit 2 e Custom UI), o manifest SEMPRE requer:**

```yaml
modules:
  jira:issuePanel:  # ou outro módulo UI
    - key: my-panel
      resource: main              # ✅ OBRIGATÓRIO
      resolver:
        function: panel-resolver  # ✅ OBRIGATÓRIO (NUNCA REMOVA!)
      render: native              # ✅ OBRIGATÓRIO
      title: My Panel

  function:
    - key: panel-resolver         # ✅ OBRIGATÓRIO
      handler: index.run          # ou index.handler

resources:
  - key: main                     # ✅ OBRIGATÓRIO
    path: src/index.jsx           # UI Kit 2
    # ou path: static/            # Custom UI
```

**Por que o resolver é SEMPRE obrigatório:**
1. O Forge usa o `resolver` para determinar o tipo de módulo
2. Conecta frontend com backend (mesmo sem lógica customizada)
3. Habilita comunicação entre camadas via `invoke()`

**Backend obrigatório:**
```javascript
// src/index.js ou src/index.jsx
import Resolver from '@forge/resolver';

const resolver = new Resolver();

// Registrar funções backend (opcional, mas resolver é obrigatório)
resolver.define('getData', async (req) => {
  return { data: 'example' };
});

// ✅ OBRIGATÓRIO - Exportar como handler
export const run = resolver.getDefinitions();  // UI Kit 2
// ou export const handler = resolver.getDefinitions();  // Custom UI
```

**Checklist de validação do manifest:**
- [ ] Módulo UI tem `resource` (referencia `resources` section)
- [ ] Módulo UI tem `resolver.function` (referencia `function` section) ← **NUNCA REMOVA!**
- [ ] Módulo UI tem `render: native`
- [ ] `function` section define o resolver handler
- [ ] `resources` section define path correto
- [ ] Backend exporta `resolver.getDefinitions()`

**Consulte:** `templates/manifest-structures.md` para estruturas completas e exemplos
