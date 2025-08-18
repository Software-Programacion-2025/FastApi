import typer
from faker import Faker
from config.cnx import SessionLocal
from users.model import User
from middlewares.auth import hash_password

def main(count: int = typer.Option(10, help="Número de usuarios a crear")):
    """Crea usuarios de ejemplo en la base de datos."""
    fake = Faker()
    db = SessionLocal()
    users = []
    for _ in range(count):
        user = User(
            id=fake.uuid4(),
            firstName=fake.first_name(),
            lastName=fake.last_name(),
            emails=fake.email(),
            password=hash_password("password"),
            ages=fake.random_int(min=18, max=80)
        )
        users.append(user)
        db.add(user)
    db.commit()
    db.close()
    typer.echo(f"{count} usuarios creados exitosamente.")

if __name__ == "__main__":
    typer.run(main)
