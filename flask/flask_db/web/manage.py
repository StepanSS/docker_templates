from flask.cli import FlaskGroup
from flask.cli import with_appcontext

from project import (create_app, db, UserDemo as User, Person, Address, Product)


app = create_app()

cli = FlaskGroup(app)


@cli.command("create_db")
@with_appcontext
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("one_to_many")
def one_to_many():
    #========= One to many =============================================

    person_1 = Person(name="John")
    person_2 = Person(name="Jim")

    address_1 = Address(email="email_1@gmail.com", person_id=person_1.id)
    address_2 = Address(email="email_2@gmail.com", person_id=person_1.id)
    address_3 = Address(email="email_3@gmail.com", person_id=person_2.id)

    person_1.addresses.append(address_1)
    person_1.addresses.append(address_2)
    person_2.addresses.append(address_3)

    db.session.add(person_1)
    db.session.add(person_2)

    db.session.add(address_1)
    db.session.add(address_2)
    db.session.add(address_3)

    db.session.commit()

    print(person_1)
    print(person_2)


@cli.command("many_to_many")
def many_to_many():
    #========= many to many =============================================

    person_1 = User(name="John", active=True)
    person_2 = User(name="Jim", active=False)

    product_1 = Product(product_name="phone")
    product_2 = Product(product_name="book")
    product_3 = Product(product_name="keyboard")

    product_1.users.append(person_1)
    product_1.users.append(person_2)

    product_2.users.append(person_1)

    product_3.users.append(person_1)
    product_3.users.append(person_2)

    db.session.add(product_1)
    db.session.add(product_2)
    db.session.add(product_3)

    db.session.commit()

    print(person_1)
    print(person_2)


@cli.command("del_one")
def del_one():
    """Delete record from parent table and all relevant 
        records in child table
    """
    person_1 = Person.query.filter_by(name="John").first()
    print(person_1)

    db.session.delete(person_1)
    db.session.commit()


@cli.command("del_left_fm_many")
def del_left_fm_many():
    """Delete record from Product table and all relevant 
        records in association_table
    """
    product = Product.query.filter_by(product_name="keyboard").first()
    print(product)

    db.session.delete(product)
    db.session.commit()


@cli.command("del_right_fm_many")
def del_right_fm_many():
    """Delete record from User table and all relevant 
        records in association_table
    """
    user = User.query.filter_by(name="Jim").first()
    print(user)

    db.session.delete(user)
    db.session.commit()


if __name__ == "__main__":
    cli()
