// Sustainable Shopping Widget - Bookmarklet v2.1
// Este código pode ser injetado em qualquer página web

(function() {
    'use strict';
    
    console.log('🌱 Sustainable Shopping Widget - Iniciando v2.1...');
    
    // Verificar se já existe
    const existingWidget = document.getElementById('sustainableWidget');
    if (existingWidget) {
        console.log('🌱 Widget já existe, alternando visibilidade...');
        if (existingWidget.style.display === 'none') {
            existingWidget.style.display = 'block';
            console.log('✅ Widget mostrado');
        } else {
            existingWidget.style.display = 'none';
            console.log('✅ Widget ocultado');
        }
        return;
    }
    
    console.log('🌱 Criando novo widget...');
    
    // Remover estilos antigos se existirem
    const oldStyles = document.getElementById('sustainableWidgetStyles');
    if (oldStyles) {
        oldStyles.remove();
    }
    
    // Criar estilos CSS com !important para override
    const style = document.createElement('style');
    style.id = 'sustainableWidgetStyles';
    style.textContent = `
        .sustainable-widget {
            position: fixed !important;
            right: 20px !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            width: 360px !important;
            max-height: 85vh !important;
            background: linear-gradient(145deg, #2E7D32, #4CAF50, #8BC34A) !important;
            border-radius: 20px !important;
            padding: 0 !important;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.1) !important;
            color: white !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            z-index: 2147483647 !important;
            overflow: hidden !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            animation: slideInWidget 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        }
        
        @keyframes slideInWidget {
            from {
                opacity: 0 !important;
                transform: translateY(-50%) translateX(100px) scale(0.9) !important;
            }
            to {
                opacity: 1 !important;
                transform: translateY(-50%) translateX(0) scale(1) !important;
            }
        }
        
        .sustainable-widget * {
            box-sizing: border-box !important;
        }
        
        .sw-header {
            background: rgba(255,255,255,0.1) !important;
            padding: 20px 25px !important;
            border-bottom: 1px solid rgba(255,255,255,0.1) !important;
            display: flex !important;
            align-items: center !important;
            position: relative !important;
        }
        
        .sw-icon {
            width: 40px !important;
            height: 40px !important;
            background: rgba(255,255,255,0.15) !important;
            border-radius: 12px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 20px !important;
            margin-right: 15px !important;
        }
        
        .sw-title-container {
            flex: 1 !important;
        }
        
        .sw-title {
            font-size: 18px !important;
            font-weight: 600 !important;
            margin: 0 0 4px 0 !important;
            color: white !important;
        }
        
        .sw-subtitle {
            font-size: 13px !important;
            color: rgba(255,255,255,0.8) !important;
            margin: 0 !important;
        }
        
        .sw-close-btn {
            position: absolute !important;
            top: 15px !important;
            right: 20px !important;
            background: rgba(255,255,255,0.1) !important;
            border: none !important;
            color: white !important;
            font-size: 16px !important;
            cursor: pointer !important;
            border-radius: 8px !important;
            width: 32px !important;
            height: 32px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.2s ease !important;
        }
        
        .sw-close-btn:hover {
            background: rgba(255,255,255,0.2) !important;
            transform: scale(1.05) !important;
        }
        
        .sw-content {
            padding: 20px 25px !important;
            max-height: calc(85vh - 100px) !important;
            overflow-y: auto !important;
        }
        
        .sw-content::-webkit-scrollbar {
            width: 6px !important;
        }
        
        .sw-content::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1) !important;
            border-radius: 3px !important;
        }
        
        .sw-content::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.3) !important;
            border-radius: 3px !important;
        }
        
        .sw-product-card {
            background: rgba(255,255,255,0.1) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 16px !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            transition: all 0.3s ease !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .sw-product-card:hover {
            background: rgba(255,255,255,0.15) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
        }
        
        .sw-product-card::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            height: 3px !important;
            background: linear-gradient(90deg, #81C784, #4CAF50, #2E7D32) !important;
        }
        
        .sw-product-header {
            display: flex !important;
            justify-content: space-between !important;
            align-items: flex-start !important;
            margin-bottom: 12px !important;
        }
        
        .sw-product-name {
            font-weight: 600 !important;
            font-size: 16px !important;
            color: white !important;
            margin: 0 !important;
            flex: 1 !important;
            line-height: 1.4 !important;
        }
        
        .sw-score {
            background: rgba(255,255,255,0.95) !important;
            color: #2E7D32 !important;
            padding: 6px 12px !important;
            border-radius: 20px !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            margin-left: 12px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }
        
        .sw-reasons {
            margin: 12px 0 !important;
        }
        
        .sw-reason {
            display: flex !important;
            align-items: center !important;
            font-size: 14px !important;
            color: rgba(255,255,255,0.9) !important;
            margin-bottom: 8px !important;
            line-height: 1.4 !important;
        }
        
        .sw-reason::before {
            content: '🌿' !important;
            margin-right: 8px !important;
            opacity: 0.8 !important;
        }
        
        .sw-footer {
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            margin-top: 15px !important;
        }
        
        .sw-price {
            font-size: 16px !important;
            font-weight: 700 !important;
            color: white !important;
            margin: 0 !important;
        }
        
        .sw-promotion {
            background: linear-gradient(135deg, #FF6B35, #F7931E) !important;
            color: white !important;
            padding: 6px 12px !important;
            border-radius: 12px !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(255,107,53,0.3) !important;
            animation: pulsePromo 2s infinite !important;
        }
        
        @keyframes pulsePromo {
            0%, 100% { transform: scale(1) !important; }
            50% { transform: scale(1.05) !important; }
        }
        
        .sw-loading {
            text-align: center !important;
            padding: 40px 20px !important;
            color: white !important;
            font-size: 16px !important;
        }
        
        .sw-loading-spinner {
            display: inline-block !important;
            width: 20px !important;
            height: 20px !important;
            border: 2px solid rgba(255,255,255,0.3) !important;
            border-radius: 50% !important;
            border-top-color: white !important;
            animation: spin 1s ease-in-out infinite !important;
            margin-right: 10px !important;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg) !important; }
        }
        
        .sw-error {
            color: #FFCDD2 !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
            text-align: center !important;
            padding: 20px !important;
        }
        
        .sw-error-icon {
            font-size: 32px !important;
            margin-bottom: 10px !important;
            display: block !important;
        }
        
        .sw-debug {
            font-size: 12px !important;
            color: rgba(255,255,255,0.7) !important;
            margin-top: 15px !important;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace !important;
            background: rgba(0,0,0,0.2) !important;
            padding: 10px !important;
            border-radius: 8px !important;
        }
        
        .sw-stats {
            background: rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            margin-top: 15px !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
        }
        
        .sw-stats-title {
            font-size: 14px !important;
            font-weight: 600 !important;
            color: white !important;
            margin-bottom: 10px !important;
            display: flex !important;
            align-items: center !important;
        }
        
        .sw-stats-grid {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 10px !important;
        }
        
        .sw-stat-item {
            text-align: center !important;
        }
        
        .sw-stat-value {
            font-size: 18px !important;
            font-weight: 700 !important;
            color: white !important;
            display: block !important;
        }
        
        .sw-stat-label {
            font-size: 12px !important;
            color: rgba(255,255,255,0.7) !important;
            margin-top: 2px !important;
        }
    `;
    
    // Garantir que estilos são adicionados primeiro
    if (!document.head) {
        console.error('❌ Head element não encontrado');
        return;
    }
    document.head.appendChild(style);
    console.log('✅ Estilos CSS adicionados');
    
    // Criar widget
    const widget = document.createElement('div');
    widget.id = 'sustainableWidget';
    widget.className = 'sustainable-widget';
    widget.innerHTML = `
        <div class="sw-header">
            <div class="sw-icon">🌱</div>
            <div class="sw-title-container">
                <div class="sw-title">Sustainable Shopping</div>
                <div class="sw-subtitle">Recomendações AI Sustentáveis</div>
            </div>
            <button class="sw-close-btn" onclick="document.getElementById('sustainableWidget').style.display='none'">×</button>
        </div>
        
        <div class="sw-content">
            <div id="swContent" class="sw-loading">
                <div class="sw-loading-spinner"></div>
                Consultando agentes sustentáveis...
            </div>
        </div>
    `;
    
    // Garantir que body existe antes de adicionar
    if (!document.body) {
        console.error('❌ Body element não encontrado');
        return;
    }
    
    document.body.appendChild(widget);
    console.log('✅ Widget HTML criado e adicionado à página');
    
    // Verificar se widget foi realmente adicionado
    const addedWidget = document.getElementById('sustainableWidget');
    if (!addedWidget) {
        console.error('❌ Widget não foi adicionado corretamente');
        return;
    }
    console.log('✅ Widget confirmado no DOM');
    
    // Função para carregar recomendações
    function loadRecommendations() {
        console.log('🔄 Iniciando carregamento de recomendações...');
        const contentDiv = document.getElementById('swContent');
        
        if (!contentDiv) {
            console.error('❌ Elemento de conteúdo não encontrado');
            return;
        }
        
        // URLs para tentar (em ordem de prioridade)
        const urls = [
            'http://localhost:5002/recommendations',
            'http://127.0.0.1:5002/recommendations'
        ];
        
        let attempts = 0;
        
        function tryUrl(urlIndex) {
            if (urlIndex >= urls.length) {
                console.error('❌ Todas as URLs falharam');
                contentDiv.innerHTML = `
                    <div class="sw-error">
                        <span class="sw-error-icon">🔌</span>
                        <div style="font-weight: 600; margin-bottom: 10px;">Erro de Conexão</div>
                        <div style="font-size: 13px; margin-bottom: 15px;">
                            Certifique-se que os agentes estão rodando
                        </div>
                        <div class="sw-debug">
                            <div>📡 Tentativas realizadas: ${attempts}</div>
                            <div>🔗 URLs testadas:</div>
                            ${urls.map(url => `<div>• ${url}</div>`).join('')}
                            <div style="margin-top: 10px;">🚀 Para iniciar os serviços:</div>
                            <div>python3 api.py (porta 5002)</div>
                            <div>python3 app.py (porta 5001)</div>
                        </div>
                    </div>
                `;
                return;
            }
            
            const url = urls[urlIndex];
            attempts++;
            console.log(`🌐 Tentativa ${attempts}: ${url}`);
            
            // Usar fetch com configurações específicas para CORS
            fetch(url, {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                console.log(`📡 Resposta recebida: status ${response.status}`);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('📊 Dados recebidos:', data);
                if (data.status === 'success' && data.recommendations && data.recommendations.length > 0) {
                    renderRecommendations(data.recommendations);
                } else {
                    console.warn('⚠️ Nenhuma recomendação encontrada');
                    contentDiv.innerHTML = `
                        <div class="sw-loading">
                            ❌ Nenhum produto sustentável encontrado no momento.
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error(`❌ Erro na URL ${url}:`, error);
                // Tentar próxima URL
                setTimeout(() => tryUrl(urlIndex + 1), 1000);
            });
        }
        
        // Iniciar tentativas
        tryUrl(0);
    }
    
    function renderRecommendations(recommendations) {
        console.log(`🎨 Renderizando ${recommendations.length} recomendações`);
        
        const totalProducts = recommendations.length;
        const avgScore = Math.round(recommendations.reduce((sum, p) => sum + (p.sustainability_analysis?.sustainability_score || 0), 0) / totalProducts);
        
        const content = recommendations.slice(0, 3).map((product, index) => {
            const analysis = product.sustainability_analysis || {};
            const ranking = product.ranking_metadata || {};
            const price = product.price_usd || {};
            
            console.log(`📦 Produto ${index + 1}:`, product.name, `Score: ${analysis.sustainability_score}`);
            
            return `
                <div class="sw-product-card">
                    <div class="sw-product-header">
                        <div class="sw-product-name">${product.name || 'Produto'}</div>
                        <div class="sw-score">🌱 ${analysis.sustainability_score || 0}/100</div>
                    </div>
                    
                    <div class="sw-reasons">
                        ${(analysis.reasons || ['Produto analisado pelos agentes sustentáveis']).slice(0, 2).map(reason => 
                            `<div class="sw-reason">${reason}</div>`
                        ).join('')}
                    </div>
                    
                    <div class="sw-footer">
                        <div class="sw-price">$${price.units || 0}.${String(price.nanos || 0).slice(0,2).padStart(2, '0')}</div>
                        ${ranking.has_promotion ? 
                            `<div class="sw-promotion">🎉 ${ranking.promotion_discount_percent || 0}% OFF</div>` : 
                            ''
                        }
                    </div>
                </div>
            `;
        }).join('');
        
        const statsSection = `
            <div class="sw-stats">
                <div class="sw-stats-title">📊 Resumo da Análise</div>
                <div class="sw-stats-grid">
                    <div class="sw-stat-item">
                        <span class="sw-stat-value">${totalProducts}</span>
                        <div class="sw-stat-label">Produtos</div>
                    </div>
                    <div class="sw-stat-item">
                        <span class="sw-stat-value">${avgScore}/100</span>
                        <div class="sw-stat-label">Score Médio</div>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('swContent').innerHTML = content + statsSection;
        console.log('✅ Recomendações renderizadas com sucesso');
    }
    
    // Aguardar um pouco para garantir que o widget foi renderizado
    setTimeout(() => {
        console.log('🔄 Iniciando carregamento de dados...');
        loadRecommendations();
    }, 100);
    
    console.log('🎉 Widget inicializado com sucesso!');
    
    // Retornar uma referência para debugging
    return {
        widget: addedWidget,
        reload: loadRecommendations
    };
    
})();