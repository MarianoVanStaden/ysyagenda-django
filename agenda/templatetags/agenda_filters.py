from django import template

register = template.Library()


@register.filter(name='ofuscar_email')
def ofuscar_email(email):
    """
    Ofusca un email ocultando los primeros 6 caracteres antes del @
    Ejemplo: lupalacio13@gmail.com -> ******io13@gmail.com
    """
    if not email or '@' not in email:
        return email

    partes = email.split('@')
    usuario = partes[0]
    dominio = partes[1]

    # Si el usuario tiene 6 o menos caracteres, ocultar todos
    if len(usuario) <= 6:
        usuario_ofuscado = '*' * len(usuario)
    else:
        # Ocultar los primeros 6 caracteres
        usuario_ofuscado = '*' * 6 + usuario[6:]

    return f"{usuario_ofuscado}@{dominio}"
