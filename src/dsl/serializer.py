class DSLSerializer:
    """Convierte un objeto ResumeModel de Python de vuelta a texto en sintaxis DSL."""

    @staticmethod
    def serialize_to_dsl(model) -> str:
        """Toma el objeto AST y genera el texto estructurado del DSL."""
        lines = []

        # 1. Encabezado y Título
        lines.append(f'CANDIDATE_PROFILE "{model.name}"')
        lines.append(f'TITLE: "{model.title}"')

        # 2. Información de Contacto
        lines.append('CONTACT')
        lines.append(f'email= "{model.contact.email}"')
        if hasattr(model.contact, 'phone') and model.contact.phone:
            lines.append(f'phone= "{model.contact.phone}"')
        if hasattr(model.contact, 'github') and model.contact.github:
            lines.append(f'github= "{model.contact.github}"')
        if hasattr(model.contact, 'linkedin') and model.contact.linkedin:
            lines.append(f'linkedin= "{model.contact.linkedin}"')

        # 3. Experiencia Laboral
        lines.append('EXPERIENCE:')
        for exp in getattr(model, 'experiences', []):
            lines.append(f'- "{exp.position}" at "{exp.company}" ({exp.years} years)')

        # 4. Educación
        lines.append('EDUCATION:')
        for edu in getattr(model, 'education', []):
            lines.append(f'- "{edu.degree}" from "{edu.institution}"')

        # 5. Habilidades (Skills)
        skills_formatted = ', '.join([f'"{s}"' for s in getattr(model, 'skills', [])])
        lines.append(f'SKILLS: {skills_formatted}')

        # 6. Evaluaciones de Perfil
        lines.append('EVALUATIONS:')
        for eval_item in getattr(model, 'evaluations', []):
            lines.append(f'"{eval_item.profile}" : {eval_item.status}')

        return '\n'.join(lines)