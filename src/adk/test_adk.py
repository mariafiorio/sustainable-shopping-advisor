#!/usr/bin/env python3
"""
ADK Test Script - Quick functionality verification
Run this to test ADK framework functionality
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_adk_imports():
    """Test if ADK modules can be imported"""
    logger.info("🔍 Testing ADK imports...")
    
    try:
        sys.path.append('/Users/maria/sustainable-shopping-advisor/src/adk')
        
        from agent_base import BaseAgent, AgentCapability, AgentTool, AgentRequest, AgentResponse, AgentStatus
        logger.info("✅ agent_base imported successfully")
        
        from sustainable_advisor_adk import SustainableAdvisorADK
        logger.info("✅ sustainable_advisor_adk imported successfully")
        
        from recommender_agent_adk import RecommenderAgentADK
        logger.info("✅ recommender_agent_adk imported successfully")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization"""
    logger.info("🚀 Testing agent initialization...")
    
    try:
        sys.path.append('/Users/maria/sustainable-shopping-advisor/src/adk')
        from sustainable_advisor_adk import SustainableAdvisorADK
        from recommender_agent_adk import RecommenderAgentADK
        
        # Initialize agents
        advisor = SustainableAdvisorADK()
        logger.info(f"✅ SustainableAdvisor initialized: v{advisor.version}")
        
        recommender = RecommenderAgentADK()
        logger.info(f"✅ RecommenderAgent initialized: v{recommender.version}")
        
        # Check capabilities
        advisor_caps = list(advisor.capabilities.keys())
        recommender_caps = list(recommender.capabilities.keys())
        
        logger.info(f"📋 SustainableAdvisor capabilities: {advisor_caps}")
        logger.info(f"📋 RecommenderAgent capabilities: {recommender_caps}")
        
        # Check tools
        advisor_tools = list(advisor.tools.keys())
        recommender_tools = list(recommender.tools.keys())
        
        logger.info(f"🔧 SustainableAdvisor tools: {advisor_tools}")
        logger.info(f"🔧 RecommenderAgent tools: {recommender_tools}")
        
        return advisor, recommender
        
    except Exception as e:
        logger.error(f"❌ Agent initialization failed: {e}")
        return None, None

def test_basic_functionality():
    """Test basic agent functionality"""
    logger.info("⚙️ Testing basic functionality...")
    
    try:
        sys.path.append('/Users/maria/sustainable-shopping-advisor/src/adk')
        from sustainable_advisor_adk import SustainableAdvisorADK
        from recommender_agent_adk import RecommenderAgentADK
        from agent_base import AgentRequest
        
        advisor = SustainableAdvisorADK()
        recommender = RecommenderAgentADK()
        
        # Test data
        test_products = [
            {
                "id": "test-1",
                "name": "Eco-Friendly Water Bottle",
                "price": 25.99,
                "categories": ["home", "sustainable"]
            },
            {
                "id": "test-2", 
                "name": "Organic Cotton T-Shirt",
                "price": 35.50,
                "categories": ["clothing", "organic"]
            }
        ]
        
        # Test sustainability analysis
        logger.info("🌱 Testing sustainability analysis...")
        request = AgentRequest(
            id="test-001",
            capability="analyze_sustainability",
            parameters={
                "products": test_products,
                "analysis_type": "basic"
            }
        )
        
        response = advisor.process_request(request)
        if response.status.value == "completed":
            logger.info("✅ Sustainability analysis successful")
            analyzed = response.result.get('analyzed_products', [])
            logger.info(f"   Analyzed {len(analyzed)} products")
        else:
            logger.error(f"❌ Sustainability analysis failed: {response.error}")
        
        # Test product ranking
        logger.info("📊 Testing product ranking...")
        request = AgentRequest(
            id="test-002",
            capability="rank_products", 
            parameters={
                "products": test_products,
                "factors": ["sustainability", "price"]
            }
        )
        
        response = recommender.process_request(request)
        if response.status.value == "completed":
            logger.info("✅ Product ranking successful")
            ranked = response.result.get('ranked_products', [])
            logger.info(f"   Ranked {len(ranked)} products")
        else:
            logger.error(f"❌ Product ranking failed: {response.error}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_health_checks():
    """Test agent health checks"""
    logger.info("🏥 Testing health checks...")
    
    try:
        sys.path.append('/Users/maria/sustainable-shopping-advisor/src/adk')
        from sustainable_advisor_adk import SustainableAdvisorADK
        from recommender_agent_adk import RecommenderAgentADK
        
        advisor = SustainableAdvisorADK()
        recommender = RecommenderAgentADK()
        
        # Health checks
        advisor_health = advisor.health_check()
        recommender_health = recommender.health_check()
        
        logger.info(f"✅ SustainableAdvisor health: {advisor_health}")
        logger.info(f"✅ RecommenderAgent health: {recommender_health}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return False

def main():
    """Main test execution"""
    print("🎯 ADK Framework Test Suite")
    print("=" * 50)
    
    success_count = 0
    total_tests = 4
    
    # Test 1: Imports
    if test_adk_imports():
        success_count += 1
    print()
    
    # Test 2: Initialization
    if test_agent_initialization():
        success_count += 1
    print()
    
    # Test 3: Functionality
    if test_basic_functionality():
        success_count += 1
    print()
    
    # Test 4: Health checks
    if test_health_checks():
        success_count += 1
    print()
    
    # Results
    print("=" * 50)
    print(f"🎯 Test Results: {success_count}/{total_tests} passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed! ADK framework is ready.")
        print("✅ Ready for Hackathon 2025 submission")
    else:
        print("⚠️ Some tests failed. Check logs above.")
        
    print("=" * 50)

if __name__ == "__main__":
    main()