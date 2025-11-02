#!/bin/bash

# Script para criar commits individuais por arquivo
# Mensagens em português seguindo Conventional Commits

# Função que escolhe o tipo de commit baseado no arquivo
get_commit_message() {
    file=$1

    if [[ $file == src/adapters/web/routers/* ]]; then
        echo "feat (backend): rota ou endpoint adicionado/alterado em $file"
    elif [[ $file == src/adapters/web/schemas/* ]]; then
        echo "feat (backend): schema DTO adicionado/alterado em $file"
    elif [[ $file == src/adapters/services/* ]]; then
        echo "feat (backend): serviço adicionado/alterado em $file"
    elif [[ $file == src/domain/* ]]; then
        echo "feat (domain): modelo, exceção ou caso de uso adicionado/alterado em $file"
    elif [[ $file == database/* || $file == ../database/* ]]; then
        echo "chore (infra): script de banco de dados alterado em $file"
    elif [[ $file == *.md ]]; then
        echo "docs: documentação atualizada em $file"
    elif [[ $file == *.py ]]; then
        echo "refactor (backend): código python alterado em $file"
    else
        echo "chore: alteração em $file"
    fi
}

# Pega arquivos modificados
modified_files=$(git diff --name-only)

# Pega arquivos não rastreados
untracked_files=$(git ls-files --others --exclude-standard)

# Junta todos os arquivos
all_files="$modified_files"$'\n'"$untracked_files"

# Loop para commitar arquivo por arquivo
while IFS= read -r file; do
    if [[ -n "$file" ]]; then
        git add "$file"
        message=$(get_commit_message "$file")
        git commit -m "$message"
    fi
done <<< "$all_files"

echo "✅ Commits individuais criados para cada arquivo!"

