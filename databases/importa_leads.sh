#!/usr/bin/env bash

DB="vitaliciosimplifica"
USER="root"
PASS="GxgLTr201@#$"
TABLE="leads"
CSV="${1:-leads.csv}"  # passe o caminho do CSV como 1º argumento

# pula o cabeçalho e insere linha a linha
tail -n +2 "$CSV" | while IFS=';' read -r email desconto; do
  # escapa aspas simples para evitar erros no SQL
  email_esc=$(printf "%s" "$email"    | sed "s/'/''/g")
  desc_esc=$(printf "%s" "$desconto"  | sed "s/'/''/g")
  MYSQL_PWD="$PASS" mysql -u"$USER" -D"$DB" \
    -e "INSERT INTO \`$TABLE\` (email, tipo, desconto) VALUES ('$email_esc','aluno','$desc_esc');"
done

echo "✅ Importação concluída."

