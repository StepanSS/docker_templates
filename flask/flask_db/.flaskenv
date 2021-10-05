COMPOSE_PROJECT_NAME=sqlalchemy

FLASK_APP=web/project
FLASK_RUN_PORT=5500
FLASK_ENV=development

# dialect+driver://username:password@host:port/database
DATABASE_URL=postgresql://sqlalchemy:sqlalchemy@localhost:8032/sqlalchemy_dev