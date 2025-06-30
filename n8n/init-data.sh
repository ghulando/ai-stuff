#!/bin/bash
set -e

echo "🚀 Initializing n8n PostgreSQL database..."

if [ -n "${POSTGRES_NON_ROOT_USER:-}" ] && [ -n "${POSTGRES_NON_ROOT_PASSWORD:-}" ]; then
    echo "Creating n8n database user: ${POSTGRES_NON_ROOT_USER}"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER ${POSTGRES_NON_ROOT_USER} WITH PASSWORD '${POSTGRES_NON_ROOT_PASSWORD}';
        GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_NON_ROOT_USER};
        GRANT CREATE ON SCHEMA public TO ${POSTGRES_NON_ROOT_USER};
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${POSTGRES_NON_ROOT_USER};
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${POSTGRES_NON_ROOT_USER};
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO ${POSTGRES_NON_ROOT_USER};
EOSQL
    echo "✅ n8n database user created successfully!"
else
    echo "⚠️  SETUP WARNING: No environment variables given for non-root user!"
fi

echo "🎉 Database initialization completed!"
