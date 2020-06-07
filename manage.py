from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask.cli import FlaskGroup

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
    manager.run()