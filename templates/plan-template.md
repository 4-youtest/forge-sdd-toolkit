# Plano Técnico de Implementação: [NOME DA FUNCIONALIDADE]

**Feature**: `[###-nome-da-feature]`
**Criado em**: [DATA]
**Status**: Planejamento
**Baseado em**: `forge-specs/[###-nome-da-feature]/feature-spec.md`

---

## Arquitetura da Solução

### Estrutura de Diretórios
```
src/
├── index.js                 # Entry point, exports de resolvers
├── modules/
│   ├── [module-name]/
│   │   ├── ui.jsx          # UI Kit ou Custom UI
│   │   └── resolver.js     # Lógica de negócio
├── functions/
│   └── [function-name].js  # Forge Functions
├── triggers/
│   └── [trigger-name].js   # Event handlers
├── services/
│   └── [service-name].js   # Lógica compartilhada
└── utils/
    └── storage.js          # Helpers para Forge Storage

manifest.yml                 # Configuração do app
```

### Módulos Forge Implementados

#### [Nome do Módulo] (`tipo:identificador`)
**Tipo**: [jira:issuePanel | function | trigger | etc.]
**Propósito**: [Descrição do que faz]
**Localização**: `src/modules/[nome]/`

**Configuração no manifest.yml**:
```yaml
modules:
  [tipo]:[identificador]:
    - key: [module-key]
      function: [function-key]
      title: [Título exibido]
      # Outras configurações específicas
```

---

## Configuração do Manifest

### manifest.yml Completo
```yaml
modules:
  # Listar todos os módulos necessários
  jira:issuePanel:
    - key: example-panel
      function: example-function
      title: Example Panel
      icon: https://example.com/icon.png

  function:
    - key: example-function
      handler: index.handler

permissions:
  scopes:
    - read:jira-work
    - write:jira-work
    - storage:app

  external:
    fetch:
      backend:
        - '*.example.com'

app:
  id: [APP_ID]
  runtime:
    name: nodejs18.x
```

### Justificativa de Permissões
| Escopo | Justificativa | Módulos que usam |
|--------|---------------|------------------|
| `read:jira-work` | [Por que precisa ler dados do Jira] | [lista de módulos] |
| `storage:app` | [Por que precisa storage] | [lista de módulos] |

---

## Implementação dos Módulos

### [Nome do Módulo 1]

**Arquivo**: `src/modules/[nome]/ui.jsx` (UI Kit)
```jsx
import ForgeUI, { render, IssuePanel, Text, useState } from '@forge/ui';
import api, { route } from '@forge/api';

const Panel = () => {
  const [data, setData] = useState(null);

  // Implementação

  return (
    <IssuePanel>
      <Text>Example content</Text>
    </IssuePanel>
  );
};

export const run = render(<Panel />);
```

**Arquivo**: `src/modules/[nome]/resolver.js`
```javascript
import api, { route } from '@forge/api';
import { storage } from '@forge/api';

export async function handler(event) {
  // Lógica do resolver

  return {
    // Resposta
  };
}
```

### [Nome da Function]

**Arquivo**: `src/functions/[nome].js`
```javascript
import api, { route } from '@forge/api';

export async function run(event, context) {
  const { payload } = event;

  // Implementação
  // Considerar timeout de 25s

  return {
    statusCode: 200,
    body: JSON.stringify({ success: true })
  };
}
```

### [Nome do Trigger]

**Arquivo**: `src/triggers/[nome].js`
```javascript
import api, { route } from '@forge/api';
import { storage } from '@forge/api';

export async function run(event) {
  const { issue, changelog } = event;

  // Processar evento
  // Considerar execução assíncrona

  console.log('Trigger executado:', event);
}
```

---

## APIs e Integrações

### APIs do Atlassian Utilizadas

| API | Endpoint | Propósito | Módulo |
|-----|----------|-----------|--------|
| Jira Platform REST API | `/rest/api/3/issue/{issueKey}` | Buscar dados de issue | [module-name] |
| Forge Storage API | `storage.set(key, value)` | Persistir dados | [module-name] |

**Exemplo de uso**:
```javascript
// Buscar issue do Jira
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}`
);
const issue = await response.json();

// Salvar no Forge Storage
await storage.set(`issue-${issueKey}`, issue);
```

### APIs Externas (se aplicável)

**API**: [Nome da API externa]
**Endpoint**: `https://api.example.com/endpoint`
**Autenticação**: [Método de autenticação]
**Configuração no manifest**:
```yaml
permissions:
  external:
    fetch:
      backend:
        - 'api.example.com'
```

---

## Gestão de Estado e Storage

### Forge Storage
**Limite**: 100MB total para o app
**Estrutura de chaves**:
```
app-config         → Configurações globais
user:{accountId}   → Dados por usuário
issue:{issueKey}   → Dados por issue
```

**Exemplo de implementação**:
```javascript
// src/utils/storage.js
import { storage } from '@forge/api';

export async function getUserData(accountId) {
  const data = await storage.get(`user:${accountId}`);
  return data || { preferences: {} };
}

export async function setUserData(accountId, data) {
  await storage.set(`user:${accountId}`, data);
}
```

### Jira Entity Properties (alternativa)
Para dados vinculados a entidades do Jira:
```javascript
await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}/properties/custom-data`,
  {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ myData: 'value' })
  }
);
```

---

## Estratégia de Testes

### Testes Locais
```bash
# Rodar app localmente
forge tunnel

# Testar função específica
forge function invoke [function-key] --payload '{"key":"value"}'
```

### Testes de Integração
- [ ] Testar cada módulo no ambiente de desenvolvimento
- [ ] Validar permissões com `forge lint`
- [ ] Testar limites de storage
- [ ] Verificar performance (timeouts)
- [ ] Testar com dados reais do Jira/Confluence

### Checklist de Validação
- [ ] Todos os módulos declarados no manifest
- [ ] Permissões mínimas necessárias
- [ ] Tratamento de erros implementado
- [ ] Logs adequados para debugging
- [ ] Documentação de APIs atualizadas

---

## Processo de Deploy

### Ambiente de Desenvolvimento
```bash
# Instalar dependências
npm install

# Deploy para desenvolvimento
forge deploy --environment development

# Instalar em site de teste
forge install --site <site-name> --environment development
```

### Ambiente de Produção
```bash
# Deploy para staging
forge deploy --environment staging

# Testar em staging
# [Executar testes de aceitação]

# Deploy para produção
forge deploy --environment production

# Criar release
forge release
```

### Versionamento
- Seguir semver: `MAJOR.MINOR.PATCH`
- Documentar breaking changes
- Manter changelog atualizado

---

## Limitações e Considerações

### Performance
- [ ] Functions têm timeout de 25s
- [ ] Implementar processamento assíncrono para tarefas longas
- [ ] Usar queue pattern se necessário (via webhooks)

### Storage
- [ ] Limite de 100MB total
- [ ] Implementar limpeza de dados antigos
- [ ] Considerar Entity Properties para dados vinculados a Jira

### Rate Limits
- [ ] Respeitar rate limits das APIs do Atlassian
- [ ] Implementar retry logic com backoff
- [ ] Cachear dados quando possível

### Segurança
- [ ] Nunca expor dados sensíveis em logs
- [ ] Validar todas as entradas de usuário
- [ ] Usar `api.asUser()` para contexto correto de permissões

---

## Próximos Passos

1. [ ] Revisar e aprovar este plano técnico
2. [ ] Criar estrutura de diretórios
3. [ ] Configurar manifest.yml
4. [ ] Implementar módulos em ordem de prioridade
5. [ ] Escrever testes
6. [ ] Deploy e validação
