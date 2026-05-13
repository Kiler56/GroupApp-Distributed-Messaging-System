#!/bin/bash

# =====================================================
# NEW IPS
# =====================================================

NEW_GRUPOS_IP=""
NEW_AUTH_IP=""
NEW_MESSAGE_IP=""

# =====================================================
# OLD IPS
# =====================================================

OLD_GRUPOS_IP="100.55.62.88"
OLD_AUTH_IP="54.234.48.182"
OLD_MESSAGE_IP="54.234.233.18"

# =====================================================
# SCRIPT
# =====================================================

echo "Searching for env files..."

find . \
  -path "./GroupApp-Distributed-Messaging-System" -prune -o \
  -maxdepth 2 \
  \( -name ".env" -o -name ".*-env" \) \
  -type f \
  -print | while read -r file
do
    echo "Updating: $file"

    sed -i \
        -e "s/${OLD_GRUPOS_IP}/${NEW_GRUPOS_IP}/g" \
        -e "s/${OLD_AUTH_IP}/${NEW_AUTH_IP}/g" \
        -e "s/${OLD_MESSAGE_IP}/${NEW_MESSAGE_IP}/g" \
        "$file"
done

echo "Done."