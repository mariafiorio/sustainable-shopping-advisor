// Teste simples do widget
console.log('🧪 Testando widget...');

// Teste básico de criação
(function testWidget() {
    if (document.getElementById('sustainableWidget')) {
        console.log('✅ Widget já existe');
        return;
    }
    
    console.log('🌱 Criando widget de teste...');
    
    const testDiv = document.createElement('div');
    testDiv.id = 'sustainableWidget';
    testDiv.style.cssText = `
        position: fixed;
        right: 20px;
        top: 20px;
        width: 300px;
        height: 200px;
        background: linear-gradient(135deg, #4CAF50, #8BC34A);
        color: white;
        border-radius: 15px;
        padding: 20px;
        z-index: 999999;
        font-family: Arial, sans-serif;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    `;
    
    testDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="margin: 0;">🌱 Widget Teste</h3>
            <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: rgba(255,255,255,0.3); border: none; color: white; 
                           padding: 5px 10px; border-radius: 5px; cursor: pointer;">×</button>
        </div>
        <p style="margin: 0 0 10px 0;">✅ Widget funcionando!</p>
        <p style="margin: 0; font-size: 14px; opacity: 0.9;">URL: ${window.location.href}</p>
        <button onclick="loadFullWidget()" 
                style="background: white; color: #4CAF50; border: none; padding: 8px 15px; 
                       border-radius: 20px; cursor: pointer; margin-top: 15px; font-weight: bold;">
            🌱 Carregar Widget Completo
        </button>
    `;
    
    document.body.appendChild(testDiv);
    console.log('✅ Widget de teste criado');
    
    // Função para carregar o widget completo
    window.loadFullWidget = function() {
        console.log('🔄 Carregando widget completo...');
        testDiv.remove();
        
        const script = document.createElement('script');
        script.src = 'http://localhost:8080/bookmarklet.js?v=' + Date.now();
        script.onload = () => console.log('✅ Widget completo carregado');
        script.onerror = () => console.error('❌ Erro ao carregar widget completo');
        document.head.appendChild(script);
    };
})();