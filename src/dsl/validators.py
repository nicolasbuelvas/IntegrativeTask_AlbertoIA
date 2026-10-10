class DSLValidationError(Exception):
    pass
def validate_resume_model(model) -> bool:

    # 1. Validar que el nombre no esté vacío
    if not model.name or not model.name.strip():
        raise DSLValidationError("El nombre del candidato no puede estar vacío.")
    # 2. Validar formato básico del correo
    if not model.contact.email or "@" not in model.contact.email:
        raise DSLValidationError(f"El correo '{model.contact.email}' no tiene un formato válido.")
    # 3. Validar que tenga al menos una evaluación
    if not hasattr(model, 'evaluations') or len(model.evaluations) == 0:
        raise DSLValidationError("El perfil debe incluir al menos una evaluación de perfil.")

    return True