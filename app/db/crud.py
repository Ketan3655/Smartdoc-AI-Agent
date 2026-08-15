from app.db.models import Document


def get_user_by_email(
    db,
    email
):
    return (
        db.query()
        .filter(email == email)
        .first()
    )

def create_user(
    db,
    email,
    password_hash
):

    user =(
        email==email,
        password_hash==password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_document(
    db,
    doc_id,
    filename,
    file_type,
    total_chunks,
    status
):

    document = Document(
        doc_id=doc_id,
        filename=filename,
        file_type=file_type,
        total_chunks=total_chunks,
        status=status
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document