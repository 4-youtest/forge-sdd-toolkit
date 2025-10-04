---
description: Testar funcionalidade implementada em Atlassian Forge
---

## 📚 Contexto Necessário

**ANTES de executar qualquer ação, carregue automaticamente estes arquivos de referência:**

1. 📄 **`.github/copilot-instructions.md`** - Regras técnicas do Atlassian Forge (carregado automaticamente)

**Identifique a feature atual e carregue:**

2. 📄 **`forge-sdd/specs/[feature]/implementation-plan.md`** - Plano técnico para validar implementação
3. 📄 **`forge-sdd/specs/[feature]/feature-spec.md`** - Especificação para validar critérios de aceite
4. 📄 **`manifest.yml`** - Configuração do app para validar módulos e permissões

Aguarde o carregamento completo antes de prosseguir.

---

A entrada do usuário pode especificar a feature ou módulos específicos para testar.

Entrada do usuário:

$ARGUMENTS

O usuário está solicitando testes da implementação. Isso inclui validação local, testes de integração e preparação para deploy.

Para testar a implementação, faça o seguinte:

1. **Validação Estática**:
   ```bash
   forge lint
   ```
   - Valide que todos os módulos estão declarados no manifest
   - Verifique se as permissões estão corretas
   - Confirme que não há erros de sintaxe

2. **Revisão do Código**:
   - Verifique se todos os requisitos da spec foram implementados
   - Confirme tratamento de erros em todos os módulos
   - Valide que as limitações do Forge foram consideradas:
     - Functions com timeout < 25s
     - Storage usage < 100MB
     - APIs externas declaradas no manifest

3. **Testes de Funções**:
   Para cada Forge Function implementada:
   ```bash
   forge function invoke [function-key] --payload '{"test":"data"}'
   ```
   - Teste cenário de sucesso
   - Teste cenários de erro
   - Valide performance (tempo de execução)

4. **Testes Locais com Tunnel**:
   ```bash
   forge tunnel
   ```
   - Instale o app em site de desenvolvimento
   - Teste cada módulo UI (panels, pages, etc.)
   - Valide fluxos de usuário da especificação
   - Teste cenários de borda identificados

5. **Checklist de Validação**:
   - [ ] Todos os requisitos funcionais implementados
   - [ ] Tratamento de erros em todos os fluxos
   - [ ] Logs adequados para debugging
   - [ ] Performance dentro dos limites (< 25s)
   - [ ] Storage usage monitorado
   - [ ] UI responsiva e acessível (se aplicável)
   - [ ] Dados sensíveis não expostos em logs

6. **Preparação para Deploy**:
   - Documente resultados dos testes
   - Liste quaisquer issues encontrados
   - Confirme que app está pronto para staging

**Comandos úteis**:
```bash
# Ver logs em tempo real
forge logs

# Limpar dados de desenvolvimento
forge storage delete --all

# Deploy para staging
forge deploy --environment staging
```

**Relatório de Testes**:
Ao final, crie um sumário em `forge-sdd/specs/[feature]/test-results.md`:
- Testes executados
- Resultados (pass/fail)
- Issues encontrados
- Próximos passos

---

## Regras de Testes - Forge

### Limitações da Plataforma (Sempre Considerar)

- ⏱️ **Timeout:** Functions têm limite de 25s de execução
- 💾 **Storage:** 100MB total por app (Forge Storage)
- 🌐 **Egress:** APIs externas devem ser declaradas no manifest.yml
- 📦 **Runtime:** Node.js 18.x (verificar compatibilidade de bibliotecas)
- 🔒 **CSP:** Custom UI tem Content Security Policy restritiva (sem inline scripts/styles)

### Validação Estática

#### Forge Lint (SEMPRE executar)

```bash
# Validar manifest e código
forge lint
```

**O que valida:**
- Sintaxe do manifest.yml
- Módulos declarados corretamente
- Permissões válidas
- Estrutura de arquivos

**Para comandos com falha, use --verbose:**
```bash
forge lint --verbose
```

### Deployment

#### Comando Padrão de Deploy

```bash
forge deploy --non-interactive -e development
```

**Ambientes disponíveis:**
- `development` (padrão - use se não especificado)
- `staging`
- `production`

⚠️ **NUNCA use `--no-verify`** (a menos que usuário solicite explicitamente)

**Exemplo de deploy para staging:**
```bash
forge deploy --non-interactive -e staging
```

#### Instalação do App

**Primeira instalação:**
```bash
forge install --non-interactive \
  --site <site-url> \
  --product <jira|confluence> \
  --environment development
```

**Exemplo concreto:**
```bash
forge install --non-interactive \
  --site mycompany.atlassian.net \
  --product jira \
  --environment development
```

**Atualização (após mudança de escopos/permissões):**
```bash
forge install --non-interactive --upgrade \
  --site <site-url> \
  --product <jira|confluence> \
  --environment development
```

⚠️ **Só é necessário atualizar se:**
- Escopos/permissões mudaram no manifest.yml
- Regras de egress foram adicionadas/modificadas

### Desenvolvimento Local com Tunnel

#### Iniciar Tunnel

```bash
forge tunnel
```

**O que o tunnel faz:**
- Permite testar código local sem deploy
- Hot reload automático de mudanças de código
- Útil para desenvolvimento iterativo

#### Quando Reimplantar

**✅ DEVE reimplantar e reiniciar tunnel se:**
- Alterou o `manifest.yml`
- Adicionou novos módulos
- Modificou escopos/permissões
- Alterou configurações de app

**Processo:**
```bash
# 1. Parar tunnel (Ctrl+C)
# 2. Reimplantar
forge deploy --non-interactive -e development
# 3. Reiniciar tunnel
forge tunnel
```

**❌ NÃO precisa reimplantar se:**
- Mudou apenas código (JavaScript/TypeScript)
- Alterou arquivos de UI
- Modificou estilos (CSS)

**Hot reload automático** funcionará para mudanças de código

#### Se Usuário Fechar Tunnel

**SEMPRE perguntar:**
- "Deseja reimplantar o app para aplicar as alterações permanentemente?"
- Explicar que mudanças no tunnel são apenas locais

### Debugging

#### Visualizar Logs

**Logs recentes (padrão: 15 minutos):**
```bash
forge logs -e development
```

**Número específico de linhas:**
```bash
forge logs -n 100 -e development
```

**Período específico:**
```bash
# Últimos 15 minutos
forge logs --since 15m -e development

# Últimas 12 horas
forge logs --since 12h -e development

# Últimos 2 dias
forge logs --since 2d -e development
```

**Com filtro por módulo/função:**
```bash
forge logs -e development | grep "function-key"
```

#### Uso de Logs para Debugging

**Para resolver:**
- Erros de runtime
- Validar fluxos de execução
- Verificar outputs de `console.log()`
- Identificar problemas de performance
- Debugar issues de permissões

**Exemplo de análise:**
```bash
# Ver logs e procurar erros
forge logs -n 200 -e development | grep -i "error"

# Ver logs de uma função específica
forge logs --since 30m -e development | grep "my-function"
```

### Testes de Performance

#### Validar Timeout (< 25s)

**Para Functions:**
```bash
# Invocar com payload e medir tempo
time forge function invoke my-function \
  --payload '{"issueKey":"PROJ-123"}'
```

**Verificar nos logs:**
- Tempo de execução reportado
- Se há warnings de timeout
- Gargalos de performance

**Se aproximando do limite (> 20s):**
- Otimizar chamadas de API (paralelizar quando possível)
- Reduzir processamento síncrono
- Considerar processamento assíncrono (triggers/webhooks)

#### Validar Storage Usage

```bash
# Ver uso atual de storage
forge storage list -e development

# Limpar dados de teste
forge storage delete --all -e development
```

⚠️ **Lembrar:** Limite de 100MB total

### Checklist Final Antes de Deploy

**Validação técnica:**
- [ ] `forge lint` passou sem erros
- [ ] Todos os testes de função passaram
- [ ] Performance < 25s para todas as functions
- [ ] Storage usage dentro do limite
- [ ] Logs não expõem dados sensíveis

**Validação funcional:**
- [ ] Todos os requisitos da spec implementados
- [ ] Fluxos de usuário testados
- [ ] Cenários de erro tratados
- [ ] UI responsiva (se aplicável)

**Validação de segurança:**
- [ ] Escopos mínimos necessários
- [ ] `asUser()` usado quando apropriado
- [ ] Validações de autorização implementadas (se usa `asApp()`)
- [ ] Dados sensíveis não expostos

**Documentação:**
- [ ] Resultados de testes documentados
- [ ] Issues conhecidos listados
- [ ] Próximos passos definidos
