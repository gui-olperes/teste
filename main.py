from flask import render_template, request, redirect, url_for, Flask

app = Flask(__name__)


# Dados fictícios
processos_ficticios = [
    {"id": 1, "nome": "Processo 1"},
    {"id": 2, "nome": "Processo 2"},
    # Adicione mais dados fictícios aqui
]

@app.route('/', methods=['GET', 'POST'])
def index():
    page = int(request.args.get('page', 1))
    processos_por_pagina = 3
    total_processos = len(processos_ficticios)
    total_pages = (total_processos + processos_por_pagina - 1) // processos_por_pagina

    start_idx = (page - 1) * processos_por_pagina
    end_idx = min(start_idx + processos_por_pagina, total_processos)
    paginated_processos = processos_ficticios[start_idx:end_idx]

    if request.method == 'POST':
        selected_processos = request.form.getlist('processo')
        checkbox_states = {str(processo['id']): 'checked' for processo in processos_ficticios if str(processo['id']) in selected_processos}
    else:
        checkbox_states = {}

    return render_template(
        'index.html',
        processos=paginated_processos,
        checkbox_states=checkbox_states,
        total_pages=total_pages,
        current_page=page
    )