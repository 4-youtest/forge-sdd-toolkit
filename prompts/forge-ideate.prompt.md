---
description: Criar ou atualizar a especificação de funcionalidade a partir de uma descrição em linguagem natural.
scripts:
  sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
---

A entrada do usuário para você pode ser fornecida diretamente pelo agente ou como um argumento de comando — você **DEVE** considerá-la antes de prosseguir com o prompt (se não estiver vazia).

Entrada do usuário:

$ARGUMENTS

O texto que o usuário digitou após `/specify` na mensagem que acionou **é** a descrição da funcionalidade. Pressuponha que você sempre a tem disponível nesta conversa, mesmo que `{ARGS}` apareça literalmente abaixo. Não peça para o usuário repeti-la a menos que ele tenha fornecido um comando vazio.

Dada essa descrição de funcionalidade, faça o seguinte:

1. Execute o script `{SCRIPT}` a partir da raiz do repositório e analise seu JSON de saída para obter BRANCH_NAME, SPEC_FILE e MANIFEST_NOTES. Todos os caminhos de arquivo devem ser absolutos.
  **IMPORTANTE** Você deve executar esse script apenas uma única vez. O JSON é fornecido no terminal como saída — consulte-o sempre para obter o conteúdo exato que você procura.
2. Carregue `templates/ideate-template.md` para entender as seções obrigatórias e a estrutura específica do Atlassian Forge.
3. Escreva a especificação em SPEC_FILE usando a estrutura do template, com atenção especial para:
   - **Contexto Atlassian Forge**: Identifique produto alvo, módulos, permissões e limitações
   - **Módulos Forge**: Marque quais módulos (jira:issuePanel, function, trigger, etc.) são necessários
   - **Escopos**: Liste e justifique cada permissão necessária no manifest.yml
   - **Limitações**: Considere timeouts (25s), storage (100MB), rate limits e runtime restrictions
   - Substitua placeholders por detalhes concretos derivados da descrição da funcionalidade
   - Preserve a ordem das seções e títulos do template
4. Preencha MANIFEST_NOTES com as configurações necessárias do manifest.yml baseado na especificação
5. **OBRIGATÓRIO:** Se a funcionalidade requer UI, você DEVE perguntar ao usuário:

   ```
   Esta funcionalidade requer interface de usuário. Por favor, escolha uma das opções:

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

   Qual você prefere? (Digite 1 para UI Kit 2 ou 2 para Custom UI)
   ```

   **AGUARDE a resposta do usuário antes de prosseguir!**

   Após a escolha, especifique no arquivo de spec:
   - **UI Kit 2**: Template `jira-issue-panel-ui-kit`, `confluence-global-page-ui-kit`, etc.
   - **Custom UI**: Template `jira-issue-panel-custom-ui`, `confluence-global-page-custom-ui`, etc.
   - ❌ NUNCA especifique UI Kit 1 (`@forge/ui`) - DEPRECIADO!

6. Informe a conclusão com:
   - Nome da branch
   - Caminhos dos arquivos criados
   - **Template recomendado** (se aplicável)
   - Próximos passos sugeridos

**Observações**:
- O script cria e faz checkout da nova branch automaticamente
- Dois arquivos são criados: feature-spec.md (especificação) e manifest-updates.md (configurações)
- Sempre considere as limitações da plataforma Forge ao especificar requisitos
- **Se UI for necessária, SEMPRE especifique UI Kit 2 ou Custom UI** (nunca UI Kit 1)

---

## Regras de Ideação - Forge

### Limitações da Plataforma (Sempre Considerar)

- ⏱️ **Timeout:** Functions têm limite de 25s de execução
- 💾 **Storage:** 100MB total por app (Forge Storage)
- 🌐 **Egress:** APIs externas devem ser declaradas no manifest.yml
- 📦 **Runtime:** Node.js 18.x (verificar compatibilidade de bibliotecas)
- 🔒 **CSP:** Custom UI tem Content Security Policy restritiva (sem inline scripts/styles)

### Escopo e Clareza

- **SEMPRE** busque esclarecimentos do usuário sobre requisitos não claros
- Se algo não for possível nativamente no Forge, sugira alternativas viáveis
- Foque sempre na solução mais simples possível para o problema
- Marque ambiguidades com `[NEEDS CLARIFICATION: questão específica]`

### Seleção de Módulos

- Se não houver módulo adequado para a necessidade, use **módulo de página global** como padrão:
  - **Jira:** `jira-global-page-ui-kit` ou `jira-global-page-custom-ui`
  - **Confluence:** `confluence-global-page-ui-kit` ou `confluence-global-page-custom-ui`

- Considere o contexto ao selecionar módulos:
  - **Painéis:** Para exibir informação contextual (ex: `jira:issuePanel`)
  - **Actions:** Para ações do usuário em contextos específicos (ex: `jira:issueAction`)
  - **Functions:** Para lógica backend e integrações
  - **Triggers:** Para reagir a eventos do produto

### Segurança desde o Início

- **Minimize escopos:** Adicione permissões somente quando estritamente necessárias
- **Prefira `asUser()`:** Para operações no contexto do usuário (autorização automática)
- **Se usar `asApp()`:** Planeje verificações de autorização explícitas usando APIs de permissões do produto
- **Liste e justifique:** Cada escopo deve ter justificativa clara na especificação

**Exemplo de escopos mínimos:**
```yaml
permissions:
  scopes:
    - read:jira-work    # Ler dados de issues (necessário para exibir painel)
```

### Arquitetura de Chamadas de API

- **Frontend (simples):** Use `requestJira/requestConfluence` do `@forge/bridge` quando possível
- **Backend (complexo):** Use resolvers para lógica complexa, validações ou múltiplas chamadas

**Quando usar cada abordagem:**
- **Frontend:** Buscar dados simples, operações CRUD diretas
- **Backend:** Processamento complexo, múltiplas APIs, lógica de negócio, dados sensíveis

### Escolhas de Tecnologia (OBRIGATÓRIO PERGUNTAR)

⚠️ **REGRA CRÍTICA: Se a funcionalidade requer UI, você DEVE perguntar explicitamente:**

**UI Kit 2 vs Custom UI:**
```
Esta funcionalidade requer interface. Escolha:

1. **UI Kit 2** - UI consistente, rápido, menos customização
2. **Custom UI** - Controle total, mais complexo

Digite 1 ou 2:
```

**NÃO prossiga sem a resposta do usuário!**

**Após obter a resposta:**
- Documente claramente a escolha na especificação
- Recomende o template correto baseado na escolha
- Se escolher UI Kit 2: SEMPRE use templates com sufixo `-ui-kit`
- Se escolher Custom UI: Use templates com sufixo `-custom-ui`
