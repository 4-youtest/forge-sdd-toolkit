# Regras Gerais do Forge SDD Toolkit

Este documento contém regras aplicáveis a todas as fases do desenvolvimento.

## Limitações da Plataforma (Sempre Considerar)

- ⏱️ **Timeout:** Functions têm limite de 25s de execução
- 💾 **Storage:** 100MB total por app (Forge Storage)
- 🌐 **Egress:** APIs externas devem ser declaradas no manifest.yml
- 📦 **Runtime:** Node.js 18.x (verificar compatibilidade de bibliotecas)
- 🔒 **CSP:** Custom UI tem Content Security Policy restritiva (sem inline scripts/styles)

## Escolha de Tecnologia

### UI Kit vs Custom UI

**UI Kit** (recomendado para):
- Projetos simples a médios
- Usuários com baixo/médio conhecimento em Forge
- Necessidade de consistência com UI nativa do Atlassian
- Time de desenvolvimento reduzido
- Menor complexidade de deploy

**Custom UI** (recomendado para):
- Projetos complexos com UI altamente customizada
- Usuários com conhecimento avançado em React
- Necessidade de bibliotecas React específicas de terceiros
- Maior controle sobre UX e comportamento
- Requisitos de performance específicos

**⚠️ SEMPRE confirmar com usuário antes de decidir**

### JavaScript vs TypeScript

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

**⚠️ SEMPRE confirmar com usuário antes de decidir**

## Estilo de Código

### Comentários
- **DEVE** sempre usar comentários verbosos no código
- Nível de detalhe: suficiente para desenvolvedores de nível intermediário com experiência limitada em Forge
- Explicar "por quê", não apenas "o quê"

**Exemplo:**
```javascript
// Busca dados da issue usando asUser() para manter contexto
// de permissões do usuário atual. Isso é mais seguro que asApp()
// pois a API já implementa verificação de autorização automática.
const response = await api.asUser().requestJira(
  route`/rest/api/3/issue/${issueKey}`
);
```

## Templates de Projeto Forge

Lista completa de templates disponíveis:

**Rovo:**
- `action-rovo`
- `rovo-agent-rovo`

**Confluence:**
- `confluence-content-action-ui-kit` / `confluence-content-action-custom-ui`
- `confluence-content-byline-ui-kit` / `confluence-content-byline-custom-ui`
- `confluence-context-menu-ui-kit` / `confluence-context-menu-custom-ui`
- `confluence-global-page-ui-kit` / `confluence-global-page-custom-ui`
- `confluence-global-settings-ui-kit` / `confluence-global-settings-custom-ui`
- `confluence-homepage-feed-ui-kit` / `confluence-homepage-feed-custom-ui`
- `confluence-macro-ui-kit` / `confluence-macro-custom-ui`
- `confluence-macro-with-custom-configuration-ui-kit` / `confluence-macro-with-custom-configuration-custom-ui`
- `confluence-space-page-ui-kit` / `confluence-space-page-custom-ui`
- `confluence-space-settings-ui-kit` / `confluence-space-settings-custom-ui`

**Jira:**
- `jira-admin-page-ui-kit` / `jira-admin-page-custom-ui`
- `jira-backlog-action-ui-kit` / `jira-backlog-action-custom-ui`
- `jira-board-action-ui-kit` / `jira-board-action-custom-ui`
- `jira-command-ui-kit` / `jira-command-custom-ui`
- `jira-custom-field-type-ui-kit` / `jira-custom-field-type-custom-ui`
- `jira-custom-field-ui-kit` / `jira-custom-field-custom-ui`
- `jira-dashboard-background-script-ui-kit` / `jira-dashboard-background-script-custom-ui`
- `jira-dashboard-gadget-ui-kit` / `jira-dashboard-gadget-custom-ui`
- `jira-entity-property`
- `jira-global-page-ui-kit` / `jira-global-page-custom-ui`
- `jira-global-permission`
- `jira-issue-action-ui-kit` / `jira-issue-action-custom-ui`
- `jira-issue-activity-ui-kit` / `jira-issue-activity-custom-ui`
- `jira-issue-context-ui-kit` / `jira-issue-context-custom-ui`
- `jira-issue-glance-ui-kit` / `jira-issue-glance-custom-ui`
- `jira-issue-navigator-action-ui-kit` / `jira-issue-navigator-action-custom-ui`
- `jira-issue-panel-ui-kit` / `jira-issue-panel-custom-ui`
- `jira-issue-view-background-script-ui-kit` / `jira-issue-view-background-script-custom-ui`
- `jira-jql-function`
- `jira-personal-settings-page-ui-kit` / `jira-personal-settings-page-custom-ui`
- `jira-project-page-ui-kit` / `jira-project-page-custom-ui`
- `jira-project-permission`
- `jira-project-settings-page-ui-kit` / `jira-project-settings-page-custom-ui`

**Jira Service Management:**
- `jira-service-management-assets-import-type-ui-kit` / `jira-service-management-assets-import-type-custom-ui`
- `jira-service-management-organization-panel-ui-kit` / `jira-service-management-organization-panel-custom-ui`
- `jira-service-management-portal-footer-ui-kit` / `jira-service-management-portal-footer-custom-ui`
- `jira-service-management-portal-header-ui-kit` / `jira-service-management-portal-header-custom-ui`
- `jira-service-management-portal-profile-panel-ui-kit` / `jira-service-management-portal-profile-panel-custom-ui`
- `jira-service-management-portal-request-create-property-panel-ui-kit` / `jira-service-management-portal-request-create-property-panel-custom-ui`
- `jira-service-management-portal-request-detail-panel-ui-kit` / `jira-service-management-portal-request-detail-panel-custom-ui`
- `jira-service-management-portal-request-detail-ui-kit` / `jira-service-management-portal-request-detail-custom-ui`
- `jira-service-management-portal-request-view-action-ui-kit` / `jira-service-management-portal-request-view-action-custom-ui`
- `jira-service-management-portal-subheader-ui-kit` / `jira-service-management-portal-subheader-custom-ui`
- `jira-service-management-portal-user-menu-action-ui-kit` / `jira-service-management-portal-user-menu-action-custom-ui`
- `jira-service-management-queue-page-ui-kit` / `jira-service-management-queue-page-custom-ui`

**Jira Workflow:**
- `jira-sprint-action-ui-kit` / `jira-sprint-action-custom-ui`
- `jira-time-tracking-provider`
- `jira-workflow-condition`
- `jira-workflow-postfunction`
- `jira-workflow-validator`

**Triggers:**
- `product-trigger`
- `scheduled-trigger`
- `webtrigger`
