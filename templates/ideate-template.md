# Especificação de Funcionalidade: [NOME DA FUNCIONALIDADE]

**Branch da Feature**: `[###-nome-da-feature]`
**Criado em**: [DATA]
**Status**: Rascunho
**Entrada**: Descrição do usuário: "$ARGUMENTOS"

## Contexto Atlassian Forge *(obrigatório)*

**Produto Alvo**: [Jira | Confluence | Bitbucket | Compass | etc.]
**Tipo de App**: [Connect App | Custom UI | UI Kit | Forge Function | Trigger]
**Módulos Forge Envolvidos**:
- [ ] `jira:issuePanel` - Painel lateral em issues
- [ ] `jira:globalPage` - Página global no Jira
- [ ] `confluence:contentBylineItem` - Item na linha de conteúdo
- [ ] `confluence:globalPage` - Página global no Confluence
- [ ] `function` - Função serverless
- [ ] `trigger` - Gatilho de eventos
- [ ] `webtrigger` - Webhook externo
- [ ] `customUI` - Interface customizada com iframe
- [ ] Outros: [especificar]

**Escopos/Permissões Necessárias** *(manifest.yml)*:
- `read:jira-work` - [justificar necessidade]
- `write:jira-work` - [justificar necessidade]
- `storage:app` - [justificar necessidade]
- Outros: [especificar e justificar]

**Limitações Consideradas**:
- [ ] Tempo de execução (max 25s para functions)
- [ ] Tamanho de storage (max 100MB para app storage)
- [ ] Rate limits de APIs
- [ ] Bibliotecas permitidas no runtime
- [ ] CORS e segurança de Custom UI

## Fluxo de Execução (principal)
```
1. Analisar a descrição do usuário a partir da Entrada
   → Se vazio: ERRO "Nenhuma descrição de funcionalidade fornecida"
2. Extrair conceitos-chave da descrição
   → Identificar: atores, ações, dados, restrições
3. Para cada aspecto não claro:
   → Marcar com [NEEDS CLARIFICATION: questão específica]
4. Preencher seção de Cenários de Usuário & Testes
   → Se não houver fluxo de usuário claro: ERRO "Não é possível determinar cenários de usuário"
5. Gerar Requisitos Funcionais
   → Cada requisito deve ser testável
   → Marcar requisitos ambíguos
6. Identificar Entidades-Chave (se houver dados envolvidos)
7. Executar Checklist de Revisão
   → Se houver [NEEDS CLARIFICATION]: AVISO "A especificação tem incertezas"
   → Se encontrados detalhes de implementação: ERRO "Remover detalhes técnicos"
8. Retornar: SUCESSO (especificação pronta para planejamento)
```

---

## ⚡ Diretrizes Rápidas
- ✅ Foque no **O QUÊ** os usuários precisam e **POR QUÊ**
- ❌ Evite **COMO** implementar (sem stack técnico, APIs, estrutura de código)
- 👥 Escrito para stakeholders de negócio, não desenvolvedores

### Requisitos de Seção
- **Seções obrigatórias**: Devem ser preenchidas para toda funcionalidade
- **Seções opcionais**: Incluir apenas quando relevante para a funcionalidade
- Quando uma seção não se aplicar, removê-la totalmente (não deixar como "N/A")

### Para Geração por IA
Ao criar esta especificação a partir de um prompt de usuário:
1. **Marque todas as ambiguidades**: Use [NEEDS CLARIFICATION: questão específica] para qualquer suposição necessária
2. **Não adivinhe**: Se o prompt não especificar algo (ex: "sistema de login" sem método de autenticação), marque
3. **Pense como um testador**: Todo requisito vago deve falhar no checklist "testável e não ambíguo"
4. **Áreas comuns subespecificadas**:
   - Tipos de usuários e permissões
   - Políticas de retenção/exclusão de dados
   - Metas de desempenho e escala
   - Comportamentos de tratamento de erro
   - Requisitos de integração
   - Necessidades de segurança/conformidade

### Específico para Atlassian Forge
5. **Sempre especifique**:
   - Qual produto Atlassian será usado
   - Quais módulos Forge são necessários
   - Quais permissões/escopos justificam a funcionalidade
   - Se há limitações da plataforma que impactam a funcionalidade
   - Se precisa de Custom UI (React) ou UI Kit (componentes Atlassian)
6. **Perguntas críticas para Forge**:
   - A funcionalidade precisa de processamento assíncrono? (considerar timeouts)
   - Precisa armazenar dados? (considerar limites de storage)
   - Precisa integrar com APIs externas? (considerar egress)
   - Precisa de autenticação de terceiros? (considerar OAuth)

---

## Cenários de Usuário & Testes *(obrigatório)*

### História de Usuário Principal
[Descreva a jornada principal do usuário em linguagem simples]

### Cenários de Aceitação
1. **Dado** [estado inicial], **Quando** [ação], **Então** [resultado esperado]
2. **Dado** [estado inicial], **Quando** [ação], **Então** [resultado esperado]

### Casos de Borda
- O que acontece quando [condição limite]?
- Como o sistema lida com [cenário de erro]?

## Requisitos *(obrigatório)*

### Requisitos Funcionais
- **RF-001**: O sistema DEVE [capacidade específica, ex: "permitir que usuários criem contas"]
- **RF-002**: O sistema DEVE [capacidade específica, ex: "validar endereços de e-mail"]  
- **RF-003**: Usuários DEVEM poder [interação-chave, ex: "redefinir sua senha"]
- **RF-004**: O sistema DEVE [requisito de dados, ex: "persistir preferências do usuário"]
- **RF-005**: O sistema DEVE [comportamento, ex: "registrar todos os eventos de segurança"]

*Exemplo de marcação de requisitos pouco claros:*
- **RF-006**: O sistema DEVE autenticar usuários via [NEEDS CLARIFICATION: método de autenticação não especificado – e-mail/senha, SSO, OAuth?]
- **RF-007**: O sistema DEVE reter dados do usuário por [NEEDS CLARIFICATION: período de retenção não especificado]

### Entidades-Chave *(incluir se a funcionalidade envolver dados)*
- **[Entidade 1]**: [O que representa, atributos-chave sem implementação]
- **[Entidade 2]**: [O que representa, relações com outras entidades]

---

## Checklist de Revisão & Aceitação
*GATE: verificações automáticas executadas durante main()*

### Qualidade do Conteúdo
- [ ] Sem detalhes de implementação (linguagens, frameworks, APIs)
- [ ] Foco em valor do usuário e necessidades de negócio
- [ ] Escrito para stakeholders não técnicos
- [ ] Todas as seções obrigatórias preenchidas

### Completude dos Requisitos
- [ ] Nenhum marcador [NEEDS CLARIFICATION] restante
- [ ] Requisitos são testáveis e não ambíguos  
- [ ] Critérios de sucesso são mensuráveis
- [ ] Escopo claramente delimitado
- [ ] Dependências e premissas identificadas

---

## Status de Execução
*Atualizado por main() durante o processamento*

- [ ] Descrição do usuário analisada
- [ ] Conceitos-chave extraídos
- [ ] Ambiguidades marcadas
- [ ] Cenários de usuário definidos
- [ ] Requisitos gerados
- [ ] Entidades identificadas
- [ ] Checklist de revisão aprovado
