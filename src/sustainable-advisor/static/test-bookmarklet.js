// Test Widget - Versão Simples para Debug
(function() {
    console.log('🧪 Test Widget - Iniciando...');
    
    // Remover widget existente se houver
    const existing = document.getElementById('testWidget');
    if (existing) {
        existing.remove();
    }
    
    // Criar widget de teste simples
    const widget = document.createElement('div');
    widget.id = 'testWidget';
    widget.style.cssText = `
        position: fixed;
        top: 50px;
        right: 50px;
        width: 300px;
        height: 200px;
        background: linear-gradient(135deg, #4CAF50, #8BC34A);
        color: white;
        border-radius: 15px;
        padding: 20px;
        z-index: 999999;
        font-family: Arial, sans-serif;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 3px solid #fff;
    `;
    
    widget.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="margin: 0; font-size: 18px;">🌱 Widget Teste</h3>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer;">×</button>
        </div>
        <div style="font-size: 14px; line-height: 1.5;">
            <p>✅ Widget injetado com sucesso!</p>
            <p>📍 Localização: ${window.location.hostname}</p>
            <p>🔄 Timestamp: ${new Date().toLocaleTimeString()}</p>
            <button onclick="loadSustainableData()" style="background: white; color: #4CAF50; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; margin-top: 10px; font-weight: bold;">
                🌱 Carregar Produtos Sustentáveis
            </button>
        </div>
    `;
    
    document.body.appendChild(widget);
    console.log('✅ Widget de teste criado com sucesso!');
    
    // Função para carregar dados sustentáveis
    window.loadSustainableData = function() {
        const button = widget.querySelector('button:last-child');
        button.innerHTML = '🔄 Carregando...';
        button.disabled = true;
        
        fetch('http://localhost:5002/recommendations')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                button.innerHTML = `✅ ${data.recommendations.length} produtos encontrados!`;
                button.style.background = '#4CAF50';
                button.style.color = 'white';
                
                // Mostrar primeira recomendação
                if (data.recommendations.length > 0) {
                    const first = data.recommendations[0];
                    widget.innerHTML += `
                        <div style="margin-top: 10px; padding: 10px; background: rgba(255,255,255,0.2); border-radius: 8px; font-size: 12px;">
                            <strong>${first.name}</strong><br>
                            Score: ${first.sustainability_analysis?.sustainability_score || 0}/100
                        </div>
                    `;
                }
            } else {
                throw new Error('Resposta inválida');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            button.innerHTML = '❌ Erro de conexão';
            button.style.background = '#f44336';
            button.style.color = 'white';
        })
        .finally(() => {
            button.disabled = false;
        });
    };
    
    alert('🌱 Widget de teste injetado! Verifique o canto superior direito da página.');
})();