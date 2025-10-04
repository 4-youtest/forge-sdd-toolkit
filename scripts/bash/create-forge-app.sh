#!/usr/bin/env bash

set -e

# Script para criar app Forge com template apropriado
# Pode ser chamado manualmente ou por prompts de IA

JSON_MODE=false
TEMPLATE=""
APP_NAME=""
INTERACTIVE=true

# Parse argumentos
while [[ $# -gt 0 ]]; do
    case "$1" in
        --json)
            JSON_MODE=true
            shift
            ;;
        --template|-t)
            TEMPLATE="$2"
            INTERACTIVE=false
            shift 2
            ;;
        --name|-n)
            APP_NAME="$2"
            INTERACTIVE=false
            shift 2
            ;;
        --help|-h)
            cat <<EOF
Uso: $0 [opções]

Cria um novo app Atlassian Forge com template apropriado.

Opções:
  --template, -t <template>  Template do Forge a usar
  --name, -n <nome>          Nome do app
  --json                     Output em formato JSON
  --help, -h                 Mostrar esta ajuda

Exemplos:
  # Modo interativo (pergunta template e nome)
  $0

  # Modo não-interativo (para IA)
  $0 --template jira-issue-panel-ui-kit --name my-app --json

Templates recomendados:
  UI Kit 2 (Recomendado):
    - jira-issue-panel-ui-kit
    - jira-global-page-ui-kit
    - confluence-global-page-ui-kit
    - confluence-macro-ui-kit

  Custom UI:
    - jira-issue-panel-custom-ui
    - confluence-global-page-custom-ui

  Functions/Triggers:
    - product-trigger
    - webtrigger
    - scheduled-trigger
EOF
            exit 0
            ;;
        *)
            echo "Argumento desconhecido: $1" >&2
            exit 1
            ;;
    esac
done

# Verificar se forge CLI está instalado
if ! command -v forge &> /dev/null; then
    if $JSON_MODE; then
        echo '{"error":"forge CLI não encontrado","message":"Instale com: npm install -g @forge/cli"}'
    else
        echo "❌ Erro: forge CLI não encontrado" >&2
        echo "Instale com: npm install -g @forge/cli" >&2
    fi
    exit 1
fi

# Templates disponíveis organizados por categoria
declare -A TEMPLATES_UI_KIT=(
    ["1"]="jira-issue-panel-ui-kit|Jira Issue Panel (UI Kit 2)"
    ["2"]="jira-global-page-ui-kit|Jira Global Page (UI Kit 2)"
    ["3"]="jira-project-page-ui-kit|Jira Project Page (UI Kit 2)"
    ["4"]="confluence-global-page-ui-kit|Confluence Global Page (UI Kit 2)"
    ["5"]="confluence-macro-ui-kit|Confluence Macro (UI Kit 2)"
)

declare -A TEMPLATES_CUSTOM_UI=(
    ["1"]="jira-issue-panel-custom-ui|Jira Issue Panel (Custom UI)"
    ["2"]="jira-global-page-custom-ui|Jira Global Page (Custom UI)"
    ["3"]="confluence-global-page-custom-ui|Confluence Global Page (Custom UI)"
)

declare -A TEMPLATES_FUNCTIONS=(
    ["1"]="product-trigger|Product Trigger (evento de produto)"
    ["2"]="webtrigger|Web Trigger (webhook)"
    ["3"]="scheduled-trigger|Scheduled Trigger (cron job)"
)

# Modo interativo
if $INTERACTIVE; then
    echo "=== Criar App Atlassian Forge ==="
    echo ""
    echo "Escolha a categoria:"
    echo "1) UI Kit 2 (Recomendado - UI consistente com Atlassian)"
    echo "2) Custom UI (UI completamente customizada)"
    echo "3) Functions/Triggers (Backend apenas)"
    echo ""
    read -p "Categoria [1-3]: " category

    case "$category" in
        1)
            echo ""
            echo "Templates UI Kit 2 disponíveis:"
            for key in $(echo "${!TEMPLATES_UI_KIT[@]}" | tr ' ' '\n' | sort -n); do
                IFS='|' read -r template desc <<< "${TEMPLATES_UI_KIT[$key]}"
                echo "$key) $desc"
            done
            echo ""
            read -p "Escolha o template [1-${#TEMPLATES_UI_KIT[@]}]: " choice
            IFS='|' read -r TEMPLATE desc <<< "${TEMPLATES_UI_KIT[$choice]}"
            ;;
        2)
            echo ""
            echo "Templates Custom UI disponíveis:"
            for key in $(echo "${!TEMPLATES_CUSTOM_UI[@]}" | tr ' ' '\n' | sort -n); do
                IFS='|' read -r template desc <<< "${TEMPLATES_CUSTOM_UI[$key]}"
                echo "$key) $desc"
            done
            echo ""
            read -p "Escolha o template [1-${#TEMPLATES_CUSTOM_UI[@]}]: " choice
            IFS='|' read -r TEMPLATE desc <<< "${TEMPLATES_CUSTOM_UI[$choice]}"
            ;;
        3)
            echo ""
            echo "Templates Functions/Triggers disponíveis:"
            for key in $(echo "${!TEMPLATES_FUNCTIONS[@]}" | tr ' ' '\n' | sort -n); do
                IFS='|' read -r template desc <<< "${TEMPLATES_FUNCTIONS[$key]}"
                echo "$key) $desc"
            done
            echo ""
            read -p "Escolha o template [1-${#TEMPLATES_FUNCTIONS[@]}]: " choice
            IFS='|' read -r TEMPLATE desc <<< "${TEMPLATES_FUNCTIONS[$choice]}"
            ;;
        *)
            echo "❌ Categoria inválida" >&2
            exit 1
            ;;
    esac

    echo ""
    read -p "Nome do app: " APP_NAME
fi

# Validar inputs
if [ -z "$TEMPLATE" ]; then
    echo "❌ Erro: Template não especificado" >&2
    exit 1
fi

if [ -z "$APP_NAME" ]; then
    echo "❌ Erro: Nome do app não especificado" >&2
    exit 1
fi

# Verificar se diretório já existe
if [ -d "$APP_NAME" ]; then
    if $JSON_MODE; then
        echo "{\"error\":\"directory_exists\",\"message\":\"Diretório '$APP_NAME' já existe\"}"
    else
        echo "❌ Erro: Diretório '$APP_NAME' já existe" >&2
    fi
    exit 1
fi

# Criar app com forge CLI
if ! $JSON_MODE; then
    echo ""
    echo "🚀 Criando app Forge..."
    echo "Template: $TEMPLATE"
    echo "Nome: $APP_NAME"
    echo ""
fi

# Executar forge create
if forge create -t "$TEMPLATE" "$APP_NAME"; then
    APP_PATH="$(pwd)/$APP_NAME"

    # ✅ CRÍTICO: Remover AGENTS.md gerado pelo Forge CLI
    # Este arquivo interfere com os prompts do toolkit
    if [ -f "$APP_PATH/AGENTS.md" ]; then
        rm "$APP_PATH/AGENTS.md"
        if ! $JSON_MODE; then
            echo "🗑️  Removido AGENTS.md (interfere com toolkit)"
        fi
    fi

    if $JSON_MODE; then
        cat <<EOF
{
  "success": true,
  "template": "$TEMPLATE",
  "app_name": "$APP_NAME",
  "app_path": "$APP_PATH",
  "manifest": "$APP_PATH/manifest.yml",
  "src_dir": "$APP_PATH/src",
  "next_steps": [
    "cd $APP_NAME",
    "npm install",
    "forge deploy -e development"
  ]
}
EOF
    else
        echo ""
        echo "✅ App criado com sucesso!"
        echo ""
        echo "📂 Localização: $APP_PATH"
        echo ""
        echo "Próximos passos:"
        echo "  1. cd $APP_NAME"
        echo "  2. npm install"
        echo "  3. forge deploy -e development"
        echo ""
        echo "Ou use o toolkit:"
        echo "  1. cd $APP_NAME"
        echo "  2. forge-sdd init --here (instalar toolkit)"
        echo "  3. /forge-implement (no Copilot)"
    fi
else
    if $JSON_MODE; then
        echo '{"success":false,"error":"forge_create_failed","message":"forge create falhou"}'
    else
        echo "❌ Erro ao criar app com forge create" >&2
    fi
    exit 1
fi
