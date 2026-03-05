# backend/agents/langgraph_agent.py
"""
LangGraph-based Agent Implementation for Multimodal Search
Production-ready with streaming, checkpointing, and monitoring
"""

import operator
from typing import Annotated, TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
import logging
import os

logger = logging.getLogger(__name__)

# Enable LangSmith tracing (optional)
os.environ.setdefault("LANGCHAIN_TRACING_V2", "false")


# ============================================================================
# State Definition
# ============================================================================

class MultimodalSearchState(TypedDict):
    """State for multimodal search agent"""
    # Input
    query: str
    user_id: Optional[str]
    
    # Processing
    messages: Annotated[List, operator.add]  # Conversation history
    intent: Dict[str, Any]
    search_results: List[Dict]
    intermediate_steps: List[Dict]
    
    # Output
    final_results: List[Dict]
    explanation: str
    confidence: float
    
    # Control flow
    should_refine: bool
    refinement_count: int
    max_refinements: int


# ============================================================================
# LangChain Tools (Replace MCP Servers)
# ============================================================================

@tool
def vector_search(query: str, modalities: List[str] = None, limit: int = 20) -> List[Dict]:
    """
    Search for content across modalities using vector similarity.
    
    Args:
        query: Search query
        modalities: List of modalities to search (text, image, video, audio)
        limit: Maximum number of results
        
    Returns:
        List of search results with scores
    """
    # This would call your actual vector DB service
    from backend.services.vector_db import get_vector_db
    from backend.services.embeddings import get_embedding_service
    
    vector_db = get_vector_db()
    embedding_service = get_embedding_service()
    
    # Generate embedding
    import asyncio
    query_embedding = asyncio.run(
        embedding_service.generate_text_embedding(query)
    )
    
    # Search
    if modalities is None or 'all' in modalities:
        modalities = ['text', 'image', 'video', 'audio']
    
    all_results = []
    for modality in modalities:
        collection = f"{modality}_embeddings"
        results = asyncio.run(
            vector_db.search(
                collection_name=collection,
                query_vector=query_embedding,
                limit=limit
            )
        )
        
        for result in results:
            all_results.append({
                'id': result['id'],
                'modality': modality,
                'score': result['score'],
                'title': result.get('payload', {}).get('title', ''),
                'url': result.get('payload', {}).get('url', ''),
                'metadata': result.get('payload', {})
            })
    
    # Sort by score
    all_results.sort(key=lambda x: x['score'], reverse=True)
    return all_results[:limit]


@tool
def get_user_preferences(user_id: str) -> Dict:
    """
    Get user preferences and interaction history.
    
    Args:
        user_id: User identifier
        
    Returns:
        User preferences including favorite modalities and topics
    """
    # Mock implementation - replace with actual user DB
    return {
        'user_id': user_id,
        'favorite_modalities': {
            'video': 0.6,
            'image': 0.3,
            'text': 0.1
        },
        'favorite_topics': ['wildlife', 'nature', 'technology'],
        'recent_searches': ['lion', 'tiger', 'elephant'],
        'engagement_level': 'high'
    }


@tool
def analyze_content_quality(results: List[Dict]) -> Dict:
    """
    Analyze the quality and relevance of search results.
    
    Args:
        results: List of search results
        
    Returns:
        Quality analysis with recommendations
    """
    if not results:
        return {
            'quality': 'poor',
            'avg_score': 0.0,
            'recommendation': 'refine_query',
            'issues': ['no_results']
        }
    
    scores = [r.get('score', 0) for r in results]
    avg_score = sum(scores) / len(scores)
    
    quality = 'excellent' if avg_score > 0.8 else \
              'good' if avg_score > 0.6 else \
              'fair' if avg_score > 0.4 else 'poor'
    
    issues = []
    if len(results) < 5:
        issues.append('few_results')
    if avg_score < 0.5:
        issues.append('low_relevance')
    
    return {
        'quality': quality,
        'avg_score': avg_score,
        'result_count': len(results),
        'recommendation': 'accept' if not issues else 'refine_query',
        'issues': issues
    }


@tool
def filter_by_metadata(
    results: List[Dict],
    category: Optional[str] = None,
    min_score: float = 0.0,
    modality: Optional[str] = None
) -> List[Dict]:
    """
    Filter results by metadata criteria.
    
    Args:
        results: List of results to filter
        category: Category filter
        min_score: Minimum relevance score
        modality: Modality filter
        
    Returns:
        Filtered results
    """
    filtered = results
    
    if category:
        filtered = [r for r in filtered if r.get('metadata', {}).get('category') == category]
    
    if min_score > 0:
        filtered = [r for r in filtered if r.get('score', 0) >= min_score]
    
    if modality:
        filtered = [r for r in filtered if r.get('modality') == modality]
    
    return filtered


@tool
def record_interaction(
    query: str,
    result_id: str,
    interaction_type: str,
    relevance_score: float
) -> Dict:
    """
    Record user interaction for continuous learning.
    
    Args:
        query: Search query
        result_id: Result that was interacted with
        interaction_type: Type of interaction (click, view, skip)
        relevance_score: User's relevance rating
        
    Returns:
        Success status
    """
    from backend.services.contrastive_learning import get_interaction_learner
    
    learner = get_interaction_learner()
    learner.record_interaction(
        query=query,
        result_id=result_id,
        modality='unknown',  # Would be extracted from result
        interaction_type=interaction_type,
        relevance_score=relevance_score
    )
    
    return {'success': True, 'recorded': True}


# ============================================================================
# Graph Nodes (Processing Steps)
# ============================================================================

def analyze_intent_node(state: MultimodalSearchState) -> MultimodalSearchState:
    """Analyze query intent and complexity"""
    query = state['query'].lower()
    
    intent = {
        'type': 'simple_search',
        'complexity': 'low',
        'temporal': False,
        'personalized': False,
        'comparison': False,
        'modality_preference': None
    }
    
    # Detect complexity
    if any(word in query for word in ['compare', 'vs', 'versus', 'difference']):
        intent['type'] = 'comparative'
        intent['complexity'] = 'high'
        intent['comparison'] = True
    
    if any(word in query for word in ['my', 'i like', 'for me', 'recommend']):
        intent['personalized'] = True
        intent['complexity'] = 'medium'
    
    if any(word in query for word in ['today', 'recent', 'last week', 'trending']):
        intent['temporal'] = True
    
    if 'video' in query:
        intent['modality_preference'] = 'video'
    elif 'image' in query or 'picture' in query:
        intent['modality_preference'] = 'image'
    
    state['intent'] = intent
    state['messages'].append(
        AIMessage(content=f"Analyzing query: {intent['type']}, complexity: {intent['complexity']}")
    )
    
    return state


def search_node(state: MultimodalSearchState) -> MultimodalSearchState:
    """Execute vector search"""
    query = state['query']
    intent = state['intent']
    
    # Determine modalities
    modalities = ['all']
    if intent.get('modality_preference'):
        modalities = [intent['modality_preference']]
    
    # Execute search
    results = vector_search.invoke({
        'query': query,
        'modalities': modalities,
        'limit': 30
    })
    
    state['search_results'] = results
    state['messages'].append(
        AIMessage(content=f"Found {len(results)} results")
    )
    
    return state


def personalize_node(state: MultimodalSearchState) -> MultimodalSearchState:
    """Personalize results based on user preferences"""
    if not state.get('user_id'):
        state['final_results'] = state['search_results']
        return state
    
    # Get user preferences
    preferences = get_user_preferences.invoke({'user_id': state['user_id']})
    
    # Boost results from preferred modalities
    results = state['search_results'].copy()
    modality_prefs = preferences.get('favorite_modalities', {})
    
    for result in results:
        modality = result.get('modality', 'text')
        boost = modality_prefs.get(modality, 0.5)
        result['score'] = result['score'] * (1 + boost * 0.5)
    
    # Re-sort
    results.sort(key=lambda x: x['score'], reverse=True)
    
    state['search_results'] = results
    state['messages'].append(
        AIMessage(content="Personalized results based on user preferences")
    )
    
    return state


def evaluate_node(state: MultimodalSearchState) -> MultimodalSearchState:
    """Evaluate result quality"""
    results = state['search_results']
    
    # Analyze quality
    analysis = analyze_content_quality.invoke({'results': results})
    
    # Determine if refinement needed
    should_refine = (
        analysis['recommendation'] == 'refine_query' and
        state.get('refinement_count', 0) < state.get('max_refinements', 2)
    )
    
    state['should_refine'] = should_refine
    state['confidence'] = analysis['avg_score']
    
    state['messages'].append(
        AIMessage(content=f"Quality: {analysis['quality']}, Score: {analysis['avg_score']:.2f}")
    )
    
    return state


def refine_node(state: MultimodalSearchState) -> MultimodalSearchState:
    """Refine query and re-search"""
    # Broaden query by removing restrictive terms
    query = state['query']
    
    # Simple refinement: make query broader
    if ' and ' in query:
        query = query.split(' and ')[0]
    elif ' with ' in query:
        query = query.split(' with ')[0]
    
    state['query'] = query
    state['refinement_count'] = state.get('refinement_count', 0) + 1
    
    state['messages'].append(
        AIMessage(content=f"Refining query to: {query}")
    )
    
    return state


def synthesize_node(state: MultimodalSearchState) -> MultimodalSearchState:
    """Synthesize final response"""
    results = state['search_results'][:20]  # Top 20
    intent = state['intent']
    
    # Generate explanation
    explanation_parts = [f"Found {len(results)} results for '{state['query']}'"]
    
    if intent.get('personalized'):
        explanation_parts.append("Results personalized based on your preferences")
    
    if state.get('refinement_count', 0) > 0:
        explanation_parts.append(f"Refined query {state['refinement_count']} times for better results")
    
    # Aggregate by modality
    modality_counts = {}
    for r in results:
        mod = r.get('modality', 'unknown')
        modality_counts[mod] = modality_counts.get(mod, 0) + 1
    
    if len(modality_counts) > 1:
        counts_str = ', '.join(f"{count} {mod}" for mod, count in modality_counts.items())
        explanation_parts.append(f"Including {counts_str}")
    
    state['final_results'] = results
    state['explanation'] = '. '.join(explanation_parts) + '.'
    
    state['messages'].append(
        AIMessage(content=state['explanation'])
    )
    
    return state


# ============================================================================
# Conditional Edge Functions
# ============================================================================

def should_personalize(state: MultimodalSearchState) -> str:
    """Decide if personalization is needed"""
    if state['intent'].get('personalized') and state.get('user_id'):
        return "personalize"
    return "evaluate"


def should_continue(state: MultimodalSearchState) -> str:
    """Decide if we should refine or finish"""
    if state.get('should_refine', False):
        return "refine"
    return "synthesize"


# ============================================================================
# Build LangGraph Workflow
# ============================================================================

def create_multimodal_search_graph(checkpointer=None):
    """
    Create the multimodal search workflow graph
    
    Args:
        checkpointer: Optional checkpointer for state persistence
        
    Returns:
        Compiled graph
    """
    # Initialize workflow
    workflow = StateGraph(MultimodalSearchState)
    
    # Add nodes
    workflow.add_node("analyze_intent", analyze_intent_node)
    workflow.add_node("search", search_node)
    workflow.add_node("personalize", personalize_node)
    workflow.add_node("evaluate", evaluate_node)
    workflow.add_node("refine", refine_node)
    workflow.add_node("synthesize", synthesize_node)
    
    # Set entry point
    workflow.set_entry_point("analyze_intent")
    
    # Add edges
    workflow.add_edge("analyze_intent", "search")
    
    # Conditional: personalize or not
    workflow.add_conditional_edges(
        "search",
        should_personalize,
        {
            "personalize": "personalize",
            "evaluate": "evaluate"
        }
    )
    
    workflow.add_edge("personalize", "evaluate")
    
    # Conditional: refine or finish
    workflow.add_conditional_edges(
        "evaluate",
        should_continue,
        {
            "refine": "refine",
            "synthesize": "synthesize"
        }
    )
    
    # Loop back from refine to search
    workflow.add_edge("refine", "search")
    
    # End after synthesis
    workflow.add_edge("synthesize", END)
    
    # Compile with optional checkpointer
    if checkpointer:
        graph = workflow.compile(checkpointer=checkpointer)
    else:
        graph = workflow.compile()
    
    return graph


# ============================================================================
# Main Agent Class
# ============================================================================

class LangGraphMultimodalAgent:
    """
    Main agent class using LangGraph
    Provides simple interface for multimodal search
    """
    
    def __init__(self, use_checkpoints: bool = True):
        """
        Initialize agent
        
        Args:
            use_checkpoints: Whether to use state checkpointing
        """
        # Setup checkpointing
        if use_checkpoints:
            self.checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
        else:
            self.checkpointer = None
        
        # Create graph
        self.graph = create_multimodal_search_graph(self.checkpointer)
        
        logger.info("LangGraph Multimodal Agent initialized")
    
    async def search(
        self,
        query: str,
        user_id: Optional[str] = None,
        thread_id: Optional[str] = None,
        max_refinements: int = 2
    ) -> Dict[str, Any]:
        """
        Execute multimodal search
        
        Args:
            query: Search query
            user_id: Optional user ID for personalization
            thread_id: Optional thread ID for conversation continuity
            max_refinements: Maximum number of query refinements
            
        Returns:
            Search results with explanation and reasoning
        """
        # Initialize state
        initial_state = {
            'query': query,
            'user_id': user_id,
            'messages': [HumanMessage(content=query)],
            'intent': {},
            'search_results': [],
            'intermediate_steps': [],
            'final_results': [],
            'explanation': '',
            'confidence': 0.0,
            'should_refine': False,
            'refinement_count': 0,
            'max_refinements': max_refinements
        }
        
        # Configure execution
        config = {"configurable": {"thread_id": thread_id or "default"}}
        
        # Execute graph
        try:
            final_state = self.graph.invoke(initial_state, config)
            
            return {
                'success': True,
                'query': query,
                'original_query': query,
                'final_query': final_state.get('query', query),
                'intent': final_state['intent'],
                'results': final_state['final_results'],
                'explanation': final_state['explanation'],
                'confidence': final_state['confidence'],
                'refinement_count': final_state.get('refinement_count', 0),
                'messages': [m.content for m in final_state['messages']],
                'total_results': len(final_state['final_results'])
            }
            
        except Exception as e:
            logger.error(f"Search failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'query': query
            }
    
    async def stream_search(
        self,
        query: str,
        user_id: Optional[str] = None,
        thread_id: Optional[str] = None
    ):
        """
        Stream search execution for real-time updates
        
        Args:
            query: Search query
            user_id: Optional user ID
            thread_id: Optional thread ID
            
        Yields:
            State updates as they occur
        """
        initial_state = {
            'query': query,
            'user_id': user_id,
            'messages': [HumanMessage(content=query)],
            'intent': {},
            'search_results': [],
            'intermediate_steps': [],
            'final_results': [],
            'explanation': '',
            'confidence': 0.0,
            'should_refine': False,
            'refinement_count': 0,
            'max_refinements': 2
        }
        
        config = {"configurable": {"thread_id": thread_id or "default"}}
        
        # Stream execution
        async for event in self.graph.astream(initial_state, config):
            yield event
    
    def get_graph_visualization(self) -> str:
        """Get Mermaid diagram of the workflow"""
        return self.graph.get_graph().draw_mermaid()
    
    def print_graph(self):
        """Print ASCII representation of graph"""
        print(self.graph.get_graph().print_ascii())


# ============================================================================
# Singleton Instance
# ============================================================================

_agent_instance = None

def get_langgraph_agent() -> LangGraphMultimodalAgent:
    """Get or create LangGraph agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = LangGraphMultimodalAgent(use_checkpoints=True)
    return _agent_instance


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        """Test the agent"""
        agent = get_langgraph_agent()
        
        # Print graph structure
        print("=== Graph Structure ===")
        agent.print_graph()
        print()
        
        # Test simple search
        print("=== Test 1: Simple Search ===")
        result = await agent.search("lion")
        print(f"Query: {result['query']}")
        print(f"Results: {result['total_results']}")
        print(f"Explanation: {result['explanation']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print()
        
        # Test personalized search
        print("=== Test 2: Personalized Search ===")
        result = await agent.search(
            "show me something I'd like",
            user_id="user_123"
        )
        print(f"Results: {result['total_results']}")
        print(f"Explanation: {result['explanation']}")
        print()
        
        # Test streaming
        print("=== Test 3: Streaming Search ===")
        async for event in agent.stream_search("tiger"):
            print(f"Event: {list(event.keys())}")
    
    asyncio.run(test_agent())