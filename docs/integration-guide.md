# 🔗 Integration Guide

This guide explains how to integrate the Sustainable Shopping Advisor with existing e-commerce platforms.

## 🎯 Integration Methods

### 1. 🖱️ Universal Bookmarklet (Recommended)

The easiest way to add sustainability intelligence to any e-commerce site:

```javascript
// Drag this to your bookmarks bar
javascript:(function(){
  const script = document.createElement('script');
  script.src = 'http://YOUR-WIDGET-URL/bookmarklet.js?v=' + Date.now();
  document.head.appendChild(script);
})();
```

**Advantages:**
- ✅ Works on any e-commerce website
- ✅ No code changes required
- ✅ Instant deployment
- ✅ Zero maintenance overhead

### 2. 🔌 Direct API Integration

For platforms that want deeper integration:

```javascript
// Example: Shopify integration
async function getSustainabilityData(productId) {
  const response = await fetch(`http://YOUR-ADVISOR-URL/recommendations?product=${productId}`);
  const data = await response.json();
  
  return {
    score: data.sustainability_score,
    alternatives: data.alternatives,
    recommendations: data.recommendations
  };
}

// Display sustainability score on product page
function displaySustainabilityScore(productElement, score) {
  const scoreElement = document.createElement('div');
  scoreElement.className = 'sustainability-score';
  scoreElement.innerHTML = `
    <div class="score-badge ${getScoreClass(score)}">
      🌱 Sustainability Score: ${score}/100
    </div>
  `;
  productElement.appendChild(scoreElement);
}
```

### 3. 🏗️ Microservice Integration

For platforms using microservices architecture:

```yaml
# kubernetes-integration.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-ecommerce-app
spec:
  template:
    spec:
      containers:
      - name: main-app
        image: your-ecommerce:latest
        env:
        - name: SUSTAINABILITY_API_URL
          value: "http://sustainable-advisor:5002"
        - name: RECOMMENDER_API_URL
          value: "http://recommender-agent:5001"
```

## 🛠️ Platform-Specific Integration

### Shopify

```liquid
<!-- In product.liquid template -->
<div id="sustainability-widget-{{ product.id }}"></div>

<script>
async function loadSustainabilityData() {
  const productData = {
    id: {{ product.id }},
    title: "{{ product.title | escape }}",
    price: {{ product.price }},
    tags: {{ product.tags | json }}
  };
  
  const response = await fetch('http://YOUR-ADVISOR-URL/recommendations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product: productData })
  });
  
  const sustainability = await response.json();
  displaySustainabilityWidget(sustainability);
}

loadSustainabilityData();
</script>
```

### WooCommerce

```php
// functions.php
add_action('woocommerce_single_product_summary', 'add_sustainability_widget', 25);

function add_sustainability_widget() {
    global $product;
    
    $product_data = array(
        'id' => $product->get_id(),
        'name' => $product->get_name(),
        'price' => $product->get_price(),
        'categories' => wp_get_post_terms($product->get_id(), 'product_cat', array('fields' => 'names'))
    );
    
    ?>
    <div id="sustainability-widget" data-product='<?php echo json_encode($product_data); ?>'></div>
    <script src="http://YOUR-WIDGET-URL/integration.js"></script>
    <?php
}
```

### Magento 2

```xml
<!-- view/frontend/layout/catalog_product_view.xml -->
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <body>
        <referenceContainer name="product.info.main">
            <block class="YourModule\SustainabilityWidget\Block\Widget" 
                   name="sustainability.widget" 
                   template="YourModule_SustainabilityWidget::widget.phtml" />
        </referenceContainer>
    </body>
</page>
```

## 🔧 Configuration Options

### Environment Variables

```bash
# Advisor Configuration
SUSTAINABILITY_API_URL=http://sustainable-advisor:5002
RECOMMENDER_API_URL=http://recommender-agent:5001
WIDGET_API_URL=http://widget-server:8080

# Feature Flags
ENABLE_REAL_TIME_SCORING=true
ENABLE_A2A_COMMUNICATION=true
ENABLE_CARBON_FOOTPRINT=true
ENABLE_ECO_ALTERNATIVES=true

# Performance Settings
CACHE_TTL_SECONDS=300
MAX_RECOMMENDATIONS=5
API_TIMEOUT_MS=2000
```

### Widget Customization

```javascript
// Custom widget configuration
window.SustainableShoppingConfig = {
  // Appearance
  theme: 'light', // 'light' | 'dark' | 'auto'
  position: 'top-right', // 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left'
  size: 'medium', // 'small' | 'medium' | 'large'
  
  // Features
  showScore: true,
  showAlternatives: true,
  showCarbonFootprint: true,
  showEcoTips: true,
  
  // Behavior
  autoShow: true,
  closeOnClick: false,
  persistPosition: true,
  
  // API Endpoints
  advisorUrl: 'http://YOUR-ADVISOR-URL',
  recommenderUrl: 'http://YOUR-RECOMMENDER-URL',
  
  // Callbacks
  onScoreCalculated: (score) => console.log('Score:', score),
  onRecommendationClick: (product) => console.log('Clicked:', product),
  onWidgetClose: () => console.log('Widget closed')
};
```

## 📊 Data Format Specifications

### Product Data Input

```json
{
  "product": {
    "id": "prod_123",
    "name": "Reusable Water Bottle",
    "description": "Eco-friendly stainless steel water bottle",
    "price": 25.99,
    "currency": "USD",
    "categories": ["Home & Garden", "Kitchen", "Drinkware"],
    "tags": ["eco-friendly", "reusable", "stainless-steel"],
    "brand": "EcoBrand",
    "materials": ["stainless steel", "silicone"],
    "dimensions": {
      "height": 25,
      "diameter": 7,
      "weight": 350
    },
    "certifications": ["BPA-free", "FDA-approved"],
    "images": ["https://example.com/image1.jpg"],
    "url": "https://example.com/product/123"
  }
}
```

### Sustainability Response

```json
{
  "sustainability_score": 87,
  "carbon_footprint": {
    "production": 2.5,
    "transportation": 0.8,
    "packaging": 0.3,
    "total_kg_co2": 3.6
  },
  "certifications": {
    "eco_friendly": true,
    "recyclable": true,
    "biodegradable": false,
    "fair_trade": false
  },
  "alternatives": [
    {
      "name": "Glass Water Bottle",
      "score": 92,
      "price": 19.99,
      "savings": "20% off",
      "reason": "Lower carbon footprint"
    },
    {
      "name": "Bamboo Water Bottle",
      "score": 95,
      "price": 22.99,
      "savings": "15% off",
      "reason": "Biodegradable material"
    }
  ],
  "recommendations": [
    "Consider glass alternatives for better recyclability",
    "Look for local manufacturers to reduce transportation impact",
    "Check for refill stations in your area"
  ],
  "impact_comparison": {
    "vs_disposable": {
      "co2_saved_yearly": 45.2,
      "plastic_saved_kg": 12.3,
      "cost_saved_usd": 180
    }
  }
}
```

## 🚀 Performance Optimization

### Caching Strategy

```javascript
// Client-side caching
const sustainabilityCache = new Map();

async function getCachedSustainabilityData(productId) {
  const cacheKey = `sustainability_${productId}`;
  
  if (sustainabilityCache.has(cacheKey)) {
    const cached = sustainabilityCache.get(cacheKey);
    if (Date.now() - cached.timestamp < 300000) { // 5 minutes
      return cached.data;
    }
  }
  
  const data = await fetchSustainabilityData(productId);
  sustainabilityCache.set(cacheKey, {
    data,
    timestamp: Date.now()
  });
  
  return data;
}
```

### Batch Processing

```javascript
// Batch multiple product requests
async function getBatchSustainabilityData(productIds) {
  const response = await fetch('http://YOUR-ADVISOR-URL/batch-recommendations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_ids: productIds })
  });
  
  return await response.json();
}
```

## 🔒 Security Considerations

### CORS Configuration

```javascript
// Server-side CORS setup
app.use(cors({
  origin: [
    'https://yourstore.com',
    'https://admin.yourstore.com',
    /\.yourstore\.com$/
  ],
  credentials: true,
  optionsSuccessStatus: 200
}));
```

### API Rate Limiting

```javascript
// Rate limiting configuration
const rateLimit = require('express-rate-limit');

const sustainabilityLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});

app.use('/recommendations', sustainabilityLimiter);
```

## 🧪 Testing Integration

### Unit Tests

```javascript
// Jest test example
describe('Sustainability Widget', () => {
  test('should load sustainability data', async () => {
    const productData = { id: '123', name: 'Test Product' };
    const sustainability = await getSustainabilityData(productData);
    
    expect(sustainability.sustainability_score).toBeGreaterThan(0);
    expect(sustainability.alternatives).toBeInstanceOf(Array);
  });
  
  test('should handle API errors gracefully', async () => {
    // Mock API failure
    jest.spyOn(global, 'fetch').mockRejectedValue(new Error('API Error'));
    
    const result = await getSustainabilityData({ id: '123' });
    expect(result.error).toBeDefined();
  });
});
```

### End-to-End Tests

```javascript
// Cypress test example
describe('Sustainability Widget E2E', () => {
  it('should display sustainability score on product page', () => {
    cy.visit('/product/123');
    cy.get('[data-testid="sustainability-widget"]').should('be.visible');
    cy.get('[data-testid="sustainability-score"]').should('contain', '/100');
    cy.get('[data-testid="eco-alternatives"]').should('exist');
  });
});
```

## 📈 Monitoring & Analytics

### Health Checks

```javascript
// Health check endpoint
app.get('/health', (req, res) => {
  const healthStatus = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    services: {
      advisor: await checkAdvisorHealth(),
      recommender: await checkRecommenderHealth(),
      database: await checkDatabaseHealth()
    }
  };
  
  res.json(healthStatus);
});
```

### Usage Analytics

```javascript
// Track widget usage
function trackSustainabilityInteraction(event, data) {
  analytics.track('Sustainability Widget', {
    event: event, // 'view', 'score_calculated', 'alternative_clicked'
    product_id: data.productId,
    score: data.score,
    alternatives_shown: data.alternatives?.length,
    user_action: data.action
  });
}
```

## 🎯 Best Practices

### 1. Progressive Enhancement
- Load sustainability features asynchronously
- Don't block main page rendering
- Provide fallbacks for API failures

### 2. User Experience
- Show loading states during API calls
- Cache results to avoid repeated requests
- Respect user preferences (show/hide widget)

### 3. Performance
- Implement proper caching strategies
- Use batch requests when possible
- Optimize API response times

### 4. Accessibility
- Ensure widget is keyboard navigable
- Provide screen reader support
- Use semantic HTML and ARIA labels

### 5. Mobile Optimization
- Responsive design for all screen sizes
- Touch-friendly interface elements
- Optimized loading for mobile networks

## 📞 Support & Troubleshooting

### Common Issues

**Widget not appearing:**
- Check CORS configuration
- Verify API endpoints are accessible
- Check browser console for errors

**Slow performance:**
- Implement caching
- Check API response times
- Optimize database queries

**Incorrect sustainability scores:**
- Verify product data format
- Check category mappings
- Review sustainability algorithm configuration

### Getting Help

- 📧 Email: support@sustainable-advisor.com
- 📚 Documentation: https://docs.sustainable-advisor.com
- 🐛 Issues: https://github.com/mariafiorio/sustainable-shopping-advisor/issues
- 💬 Community: https://discord.gg/sustainable-ai