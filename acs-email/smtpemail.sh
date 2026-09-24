#!/bin/bash

send_count="${1:-1}"
recipients=(
  "<recipient-email-1>"
  # "<recipient-email-2>"
)

if [[ ! "$send_count" =~ ^[1-9][0-9]*$ ]]; then
  echo "Usage: $0 [positive_integer]" >&2
  exit 1
fi

for ((email_number = 1; email_number <= send_count; email_number++)); do
  recipient="${recipients[RANDOM % ${#recipients[@]}]}"
  printf 'Sending email \033[1;36m%s/%s\033[0m to \033[1;32m%s\033[0m...\n' \
    "$email_number" "$send_count" "$recipient"
  swaks \
    --server smtp.azurecomm.net:587 \
    --tls \
    --auth \
    --auth-user "<smtp-auth-user>" \
    --auth-password "<smtp-auth-password>" \
    --from "<sender-address>" \
    --to "$recipient" \
    --h-Subject "Test Email on SMTP" \
    --h-From "Booking System <sender-address>" \
    --add-header "Reply-To: <reply-to-address>" \
    --body "Test ACS Email with SMTP."
done
