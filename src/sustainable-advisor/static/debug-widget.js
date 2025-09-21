// Debug Widget - Versão Simplificada para Depuração
(function() {
    console.log('🔍 Debug Widget - Iniciando...');
    console.log('🌍 URL atual:', window.location.href);
    console.log('📍 Host:', window.location.hostname);
    
    // Verificar se já existe widget
    const existing = document.getElementById('sustainableWidget');
    if (existing) {
        console.log('🌱 Widget já existe, removendo...');
        existing.remove();
    }
    
    // Criar widget super simples para debug
    const widget = document.createElement('div');
    widget.id = 'sustainableWidget';
    widget.style.cssText = `
        position: fixed !important;
        top: 20px !important;
        right: 20px !important;
        width: 300px !important;
        height: 150px !important;
        background: linear-gradient(135deg, #4CAF50, #8BC34A) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        z-index: 2147483647 !important;
        font-family: Arial, sans-serif !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
    `;
    
    widget.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="margin: 0; font-size: 18px;">🌱 Debug Widget</h3>
            <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: rgba(255,255,255,0.3); border: none; color: white; 
                           padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 16px;">×</button>
        </div>
        <div style="font-size: 14px; line-height: 1.4;">
            <div>✅ Widget criado com sucesso!</div>
            <div>🌍 Host: ${window.location.hostname}</div>
            <div>📍 URL: ${window.location.pathname}</div>
            <button onclick="testAPI()" 
                    style="background: white; color: #4CAF50; border: none; padding: 8px 15px; 
                           border-radius: 20px; cursor: pointer; margin-top: 10px; font-weight: bold;">
                🧪 Testar API
            </button>
        </div>
    `;
    
    // Função de teste de API
    window.testAPI = async function() {
        console.log('🧪 Testando API...');
        const button = widget.querySelector('button:last-child');
        button.innerHTML = '🔄 Testando...';
        
        try {
            const response = await fetch('http://localhost:5002/health', {
                method: 'GET',
                mode: 'cors'
            });
            
            if (response.ok) {
                button.innerHTML = '✅ API OK!';
                button.style.background = '#4CAF50';
                button.style.color = 'white';
                console.log('✅ API funcionando');
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            button.innerHTML = '❌ API Offline';
            button.style.background = '#f44336';
            button.style.color = 'white';
            console.error('❌ Erro na API:', error);
        }
    };
    
    // Adicionar ao DOM
    try {
        document.body.appendChild(widget);
        console.log('✅ Widget adicionado ao DOM');
        console.log('📦 Widget element:', widget);
        
        // Verificar se foi realmente adicionado
        const check = document.getElementById('sustainableWidget');
        if (check) {
            console.log('✅ Widget confirmado no DOM');
        } else {
            console.error('❌ Widget não encontrado no DOM após inserção');
        }
        
    } catch (error) {
        console.error('❌ Erro ao adicionar widget:', error);
        alert('❌ Erro ao criar widget: ' + error.message);
    }
    
    console.log('🎉 Debug Widget finalizado');
})();