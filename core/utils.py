from .models import (Group, Person, Profession, AgeGroup, Sex, Region)
import random
from sqlmodel import Session, select
import numpy as np

attrs = [Profession, AgeGroup, Sex, Region]
attr_map = {
    "profession": Profession,
    "sex": Sex,
    "age_group": AgeGroup,
    "region": Region
}

def create_person(session: Session, attr: str, attr_value: str):
    anchor = attr_map[attr]
    profession = random.choice(list(session.exec(select(Profession)).all()))
    region = random.choice(list(session.exec(select(Region)).all()))
    sex = random.choice(list(Sex))
    age_group = random.choice(list(AgeGroup))
    prob = np.random.normal(loc=0.75, scale=0.1, size=1)[0]
    person = Person(
        profession=profession,
        sex=sex,
        age_group=age_group,
        region=region,
        prob=float(prob)
    )
    if attr == "sex":
        attr_value_entry = Sex[attr_value]
        person.sex = attr_value_entry
    elif attr == "age_group":
        attr_value_entry = AgeGroup[attr_value]
        person.age_group = attr_value_entry
    else:
        attr_value_entry = session.exec(select(attr_map[attr]).where(name=attr_value)).first()
        person.__setattr__(attr, attr_value_entry)

    return person




    # attr_value_entry = session.exec(select(attr_map[attr]).where(name=attr_value)
    # person.__setattr__(attr, )

    

def create_group(session: Session, n: int):
    anchor = random.choice(attrs)
    if anchor == AgeGroup:
        attr = "age_group"
        grps = list(AgeGroup)
        grps.remove(AgeGroup.infant)
        grps.remove(AgeGroup.toddler)
        grps.remove(AgeGroup.pre_schoolers)
        anchor_value = random.choice(grps)
    elif anchor == Sex:
        attr = "sex"
        grps = list(Sex)
        anchor_value = random.choice(grps)
    else:
        attr = f"{anchor}".lower()
        grps = session.exec(select(anchor)).all()
        anchor_value = random.choice(list(grps))
    group = Group()
    session.add(group)
    for i in range(n):
        person = create_person(session, attr, str(anchor_value))
        person.group = group
        session.add(person)
    session.commit()
    session.refresh(group)
    return group



