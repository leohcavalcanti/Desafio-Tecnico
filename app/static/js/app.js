const API_URL = '/api/plano';

function navigateTo(view) {
    document.getElementById('view-list').classList.add('hidden');
    document.getElementById('view-form').classList.add('hidden');
    document.getElementById(`view-${view}`).classList.remove('hidden');

    if (view === 'list'){
        carregarPlanos();
    }
    if (view === 'form'){
        document.getElementById('plano-form').reset();
        document.getElementById('plano-id').value = '';
        document.getElementById('form-title').innerText = 'Cadastrar Novo Plano';
    }
}

// 1. Listar Planos (GET)
async function carregarPlanos() {
    const tituloBusca = document.getElementById('filtro-titulo').value;
    let url = API_URL;
    if (tituloBusca) url += `?titulo=${tituloBusca}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        const tbody = document.querySelector('#tabela-planos tbody');
        tbody.innerHTML = '';

        data.planos.forEach(plano => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${plano.titulo}</td>
                <td>${plano.disciplina}</td>
                <td>${plano.data_prevista || 'N/A'}</td>
                <td>
                    <button onclick="editarPlano(${plano.id})">✏️</button>
                    <button class="btn-secondary" onclick="excluirPlano(${plano.id})">🗑️</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        alert("Erro ao carregar planos de aula.");
    }
}

// 2. Salvar Plano (POST / PUT)
async function salvarPlano(event) {
    event.preventDefault();
    
    const tagsInput = document.getElementById('tags').value;
    const tagsArray = tagsInput ? tagsInput.split(',').map(tag => tag.trim()) : [];

    const plano = {
        titulo: document.getElementById('titulo').value,
        disciplina: document.getElementById('disciplina').value,
        data_prevista: document.getElementById('data_prevista').value,
        ementa: document.getElementById('ementa').value,
        objetivo: document.getElementById('objetivo').value,
        conteudos: document.getElementById('conteudos').value,
        recursos_apoio: document.getElementById('recursos_apoio').value,
        tags: tagsArray
    };

    const id = document.getElementById('plano-id').value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_URL}/${id}` : API_URL;

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(plano)
        });

        if (response.ok) {
            alert(id ? "Plano atualizado!" : "Plano criado com sucesso!");
            navigateTo('list');
        } else {
            const error = await response.json();
            alert("Erro: " + error.erro);
        }
    } catch (error) {
        alert("Erro de conexão com o servidor.");
    }
}

// 3. Integração com IA (Smart Assist)
async function gerarComIA() {
    const titulo = document.getElementById('titulo').value;
    const disciplina = document.getElementById('disciplina').value;
    const ementa = document.getElementById('ementa').value;

    if (!titulo || !disciplina || !ementa) {
        alert("Preencha Título, Disciplina e Ementa para usar a IA.");
        return;
    }

    document.getElementById('loading-overlay').classList.remove('hidden');

    try {
        const response = await fetch(`${API_URL}/recomendar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ titulo, disciplina, ementa })
        });

        if (response.ok) {
            const sugestoes = await response.json();
            
            document.getElementById('conteudos').value = sugestoes.conteudos_complementares;
            document.getElementById('recursos_apoio').value = sugestoes.topicos_relacionados.join(', ');
            document.getElementById('tags').value = sugestoes.tags_recomendadas.join(', ');
        } else {
            alert("A IA não conseguiu gerar recomendações. Tente novamente.");
        }
    } catch (error) {
        alert("Erro na comunicação com o assistente de IA. Timeout ou falha de rede.");
    } finally {
        document.getElementById('loading-overlay').classList.add('hidden');
    }
}

// 4. Editar Plano (GET específico e preenchimento de tela)
async function editarPlano(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);
        
        if (response.ok) {
            const plano = await response.json();
            
            navigateTo('form');
            
            document.getElementById('form-title').innerText = '✏️ Editar Plano de Aula';
            document.getElementById('plano-id').value = plano.id;
            document.getElementById('titulo').value = plano.titulo;
            document.getElementById('disciplina').value = plano.disciplina;
            document.getElementById('data_prevista').value = plano.data_prevista;
            document.getElementById('ementa').value = plano.ementa;
            
            document.getElementById('objetivo').value = plano.objetivo || '';
            document.getElementById('conteudos').value = plano.conteudos || '';
            document.getElementById('recursos_apoio').value = plano.recursos_apoio || '';
            
            document.getElementById('tags').value = plano.tags ? plano.tags.join(', ') : '';
            
        } else {
            alert("Erro ao buscar os detalhes deste plano.");
        }
    } catch (error) {
        alert("Erro de conexão ao tentar editar.");
    }
}


// 5. Excluir Plano (DELETE)
async function excluirPlano(id) {
    // Pergunta de confirmação para o usuário não excluir sem querer
    const confirmacao = confirm("Tem certeza que deseja excluir permanentemente este plano de aula?");
    
    if (!confirmacao) {
        return; // Se o usuário clicar em "Cancelar", a função para aqui
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert("Plano excluído com sucesso!");
            carregarPlanos();
        } else {
            const error = await response.json();
            alert("Erro ao excluir: " + error.erro);
        }
    } catch (error) {
        alert("Erro de conexão ao tentar excluir.");
    }
}

carregarPlanos();