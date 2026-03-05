# backend/agents/orchestrator.py
"""
Agent Orchestrator - The Brain of the Agentic System
Handles query understanding, planning, tool selection, and result synthesis
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import time

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Agent execution states"""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentThought:
    """Represents an agent's reasoning step"""
    step_number: int
    thought: str
    action: str
    tool: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    confidence: float = 1.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class ExecutionPlan:
    """Multi-step execution plan"""
    query: str
    intent: Dict[str, Any]
    steps: List[Dict[str, Any]]
    estimated_time: float
    requires_context: bool = False
    fallback_plan: Optional['ExecutionPlan'] = None


class ConversationMemory:
    """Maintains conversation context and history"""
    
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.history: List[Dict] = []
        self.context: Dict[str, Any] = {}
    
    def add_turn(self, user_query: str, agent_response: Any, metadata: Dict = None):
        """Add conversation turn"""
        self.history.append({
            'user': user_query,
            'agent': agent_response,
            'metadata': metadata or {},
            'timestamp': time.time()
        })
        
        # Trim to max turns
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]
    
    def get_context(self) -> Dict[str, Any]:
        """Get relevant context from conversation"""
        if not self.history:
            return {}
        
        # Extract entities, topics, preferences from history
        recent_topics = []
        recent_entities = []
        
        for turn in self.history[-3:]:  # Last 3 turns
            if 'metadata' in turn:
                recent_topics.extend(turn['metadata'].get('topics', []))
                recent_entities.extend(turn['metadata'].get('entities', []))
        
        return {
            'recent_topics': list(set(recent_topics)),
            'recent_entities': list(set(recent_entities)),
            'conversation_length': len(self.history)
        }
    
    def clear(self):
        """Clear conversation history"""
        self.history = []
        self.context = {}


class QueryPlanner:
    """Plans query execution strategy"""
    
    def __init__(self):
        self.strategy_templates = self._load_strategies()
    
    def _load_strategies(self) -> Dict[str, Any]:
        """Load query strategy templates"""
        return {
            'simple_search': {
                'pattern': 'single keyword or concept',
                'steps': ['vector_search', 'rank_results']
            },
            'filtered_search': {
                'pattern': 'search with filters (date, category, etc.)',
                'steps': ['vector_search', 'apply_filters', 'rank_results']
            },
            'comparative_search': {
                'pattern': 'compare X and Y',
                'steps': [
                    'search_concept_a',
                    'search_concept_b',
                    'extract_features',
                    'compare_features',
                    'synthesize_comparison'
                ]
            },
            'contextual_search': {
                'pattern': 'requires conversation context',
                'steps': ['retrieve_context', 'augment_query', 'vector_search']
            },
            'personalized_search': {
                'pattern': 'user-specific preferences',
                'steps': [
                    'get_user_profile',
                    'analyze_preferences',
                    'vector_search',
                    'personalize_ranking'
                ]
            },
            'multi_step_research': {
                'pattern': 'complex multi-faceted query',
                'steps': [
                    'decompose_query',
                    'parallel_searches',
                    'aggregate_results',
                    'analyze_patterns',
                    'synthesize_insights'
                ]
            }
        }
    
    async def analyze_intent(self, query: str, context: Dict) -> Dict[str, Any]:
        """Analyze query intent and complexity"""
        intent = {
            'query': query,
            'type': 'simple_search',  # default
            'complexity': 'low',
            'requires_context': False,
            'requires_personalization': False,
            'temporal_constraint': None,
            'modality_preference': None,
            'comparison_needed': False,
            'entities': [],
            'topics': []
        }
        
        query_lower = query.lower()
        
        # Detect comparison
        if any(word in query_lower for word in ['compare', 'vs', 'versus', 'difference', 'versus']):
            intent['type'] = 'comparative_search'
            intent['complexity'] = 'medium'
            intent['comparison_needed'] = True
        
        # Detect temporal constraints
        temporal_words = ['today', 'yesterday', 'last week', 'this month', 'recent']
        if any(word in query_lower for word in temporal_words):
            intent['temporal_constraint'] = 'recent'
            intent['type'] = 'filtered_search'
        
        # Detect personalization cues
        personal_words = ['my', 'i like', 'for me', 'surprise me', 'recommend']
        if any(word in query_lower for word in personal_words):
            intent['requires_personalization'] = True
            intent['type'] = 'personalized_search'
        
        # Detect contextual queries
        contextual_words = ['more like this', 'similar', 'also', 'another', 'more']
        if any(word in query_lower for word in contextual_words):
            intent['requires_context'] = True
            intent['type'] = 'contextual_search'
        
        # Detect modality preference
        if 'video' in query_lower:
            intent['modality_preference'] = 'video'
        elif 'image' in query_lower or 'picture' in query_lower or 'photo' in query_lower:
            intent['modality_preference'] = 'image'
        elif 'audio' in query_lower or 'sound' in query_lower:
            intent['modality_preference'] = 'audio'
        
        # Extract entities (simplified)
        # In production, use NER model
        words = query.split()
        capitalized = [w for w in words if w[0].isupper() and len(w) > 2]
        intent['entities'] = capitalized
        
        # Determine complexity
        if len(query.split()) > 15:
            intent['complexity'] = 'high'
            intent['type'] = 'multi_step_research'
        elif intent['comparison_needed'] or intent['requires_personalization']:
            intent['complexity'] = 'medium'
        
        return intent
    
    async def create_plan(self, intent: Dict[str, Any]) -> ExecutionPlan:
        """Create execution plan based on intent"""
        query_type = intent['type']
        strategy = self.strategy_templates.get(query_type, self.strategy_templates['simple_search'])
        
        steps = []
        
        if query_type == 'simple_search':
            steps = [
                {
                    'action': 'vector_search',
                    'tool': 'vector_search_mcp',
                    'parameters': {
                        'query': intent['query'],
                        'modalities': [intent.get('modality_preference', 'all')],
                        'limit': 20
                    }
                },
                {
                    'action': 'rank_results',
                    'tool': 'local',
                    'parameters': {'ranking_method': 'relevance'}
                }
            ]
        
        elif query_type == 'filtered_search':
            filters = {}
            if intent.get('temporal_constraint'):
                filters['date_constraint'] = intent['temporal_constraint']
            
            steps = [
                {
                    'action': 'vector_search',
                    'tool': 'vector_search_mcp',
                    'parameters': {
                        'query': intent['query'],
                        'filters': filters,
                        'limit': 30
                    }
                },
                {
                    'action': 'apply_filters',
                    'tool': 'metadata_mcp',
                    'parameters': filters
                },
                {
                    'action': 'rank_results',
                    'tool': 'local',
                    'parameters': {'ranking_method': 'relevance'}
                }
            ]
        
        elif query_type == 'personalized_search':
            steps = [
                {
                    'action': 'get_user_profile',
                    'tool': 'user_preferences_mcp',
                    'parameters': {}
                },
                {
                    'action': 'vector_search',
                    'tool': 'vector_search_mcp',
                    'parameters': {
                        'query': intent['query'],
                        'personalized': True,
                        'limit': 30
                    }
                },
                {
                    'action': 'personalized_ranking',
                    'tool': 'analytics_mcp',
                    'parameters': {'use_user_preferences': True}
                }
            ]
        
        elif query_type == 'contextual_search':
            steps = [
                {
                    'action': 'retrieve_context',
                    'tool': 'local',
                    'parameters': {}
                },
                {
                    'action': 'augment_query',
                    'tool': 'local',
                    'parameters': {}
                },
                {
                    'action': 'vector_search',
                    'tool': 'vector_search_mcp',
                    'parameters': {
                        'query': 'augmented_query',
                        'limit': 20
                    }
                }
            ]
        
        elif query_type == 'comparative_search':
            steps = [
                {
                    'action': 'decompose_comparison',
                    'tool': 'local',
                    'parameters': {}
                },
                {
                    'action': 'parallel_search',
                    'tool': 'vector_search_mcp',
                    'parameters': {'parallel': True}
                },
                {
                    'action': 'compare_results',
                    'tool': 'analytics_mcp',
                    'parameters': {}
                },
                {
                    'action': 'synthesize_comparison',
                    'tool': 'local',
                    'parameters': {}
                }
            ]
        
        estimated_time = len(steps) * 0.1  # 100ms per step estimate
        
        plan = ExecutionPlan(
            query=intent['query'],
            intent=intent,
            steps=steps,
            estimated_time=estimated_time,
            requires_context=intent.get('requires_context', False)
        )
        
        # Create fallback plan for complex queries
        if intent['complexity'] == 'high':
            fallback_steps = [
                {
                    'action': 'vector_search',
                    'tool': 'vector_search_mcp',
                    'parameters': {'query': intent['query'], 'limit': 20}
                }
            ]
            plan.fallback_plan = ExecutionPlan(
                query=intent['query'],
                intent=intent,
                steps=fallback_steps,
                estimated_time=0.1,
                requires_context=False
            )
        
        return plan


class AgentOrchestrator:
    """
    Main agent orchestrator - coordinates all agent activities
    Implements ReAct (Reasoning + Acting) pattern
    """
    
    def __init__(self, mcp_clients: Dict[str, Any]):
        self.mcp_clients = mcp_clients
        self.memory = ConversationMemory()
        self.planner = QueryPlanner()
        self.state = AgentState.IDLE
        self.thoughts: List[AgentThought] = []
        self.max_refinement_attempts = 3
    
    async def process_query(
        self,
        query: str,
        user_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for query processing
        Implements full ReAct loop: Reason → Act → Observe → Reflect
        """
        self.state = AgentState.PLANNING
        self.thoughts = []
        
        try:
            # Step 1: Understand intent (Reasoning)
            conversation_context = self.memory.get_context()
            if context:
                conversation_context.update(context)
            
            intent = await self.planner.analyze_intent(query, conversation_context)
            
            self._add_thought(
                thought=f"Query intent: {intent['type']}, complexity: {intent['complexity']}",
                action="analyze_intent",
                confidence=0.9
            )
            
            # Step 2: Create execution plan (Reasoning)
            plan = await self.planner.create_plan(intent)
            
            self._add_thought(
                thought=f"Created plan with {len(plan.steps)} steps",
                action="create_plan",
                confidence=0.95
            )
            
            # Step 3: Execute plan (Acting)
            self.state = AgentState.EXECUTING
            results = await self._execute_plan(plan, user_id)
            
            # Step 4: Reflect on results (Reflection)
            self.state = AgentState.REFLECTING
            is_satisfactory, issues = await self._evaluate_results(results, intent)
            
            if not is_satisfactory and plan.fallback_plan:
                self._add_thought(
                    thought=f"Results unsatisfactory: {issues}. Trying fallback plan.",
                    action="use_fallback",
                    confidence=0.7
                )
                results = await self._execute_plan(plan.fallback_plan, user_id)
            
            # Step 5: Synthesize response (Synthesis)
            self.state = AgentState.SYNTHESIZING
            response = await self._synthesize_response(results, intent, plan)
            
            # Step 6: Update memory
            self.memory.add_turn(
                user_query=query,
                agent_response=response,
                metadata={
                    'intent': intent,
                    'thoughts': [t.__dict__ for t in self.thoughts],
                    'execution_time': sum(t.timestamp for t in self.thoughts[-3:])
                }
            )
            
            self.state = AgentState.COMPLETED
            
            return {
                'success': True,
                'query': query,
                'intent': intent,
                'results': response,
                'thoughts': [self._serialize_thought(t) for t in self.thoughts],
                'execution_time_ms': (time.time() - self.thoughts[0].timestamp) * 1000
            }
            
        except Exception as e:
            self.state = AgentState.FAILED
            logger.error(f"Agent orchestration failed: {e}", exc_info=True)
            
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'thoughts': [self._serialize_thought(t) for t in self.thoughts]
            }
    
    async def _execute_plan(
        self,
        plan: ExecutionPlan,
        user_id: Optional[str]
    ) -> Dict[str, Any]:
        """Execute the plan step by step"""
        results = {
            'steps': [],
            'data': {},
            'metadata': {}
        }
        
        for idx, step in enumerate(plan.steps):
            self._add_thought(
                thought=f"Executing step {idx + 1}: {step['action']}",
                action=step['action'],
                tool=step.get('tool')
            )
            
            try:
                # Execute step
                if step['tool'] == 'local':
                    step_result = await self._execute_local_action(step, results)
                else:
                    step_result = await self._execute_mcp_tool(
                        step['tool'],
                        step['action'],
                        step.get('parameters', {}),
                        user_id
                    )
                
                results['steps'].append({
                    'step': idx + 1,
                    'action': step['action'],
                    'success': True,
                    'result': step_result
                })
                
                # Update results data
                results['data'][step['action']] = step_result
                
            except Exception as e:
                logger.error(f"Step {idx + 1} failed: {e}")
                results['steps'].append({
                    'step': idx + 1,
                    'action': step['action'],
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    async def _execute_local_action(
        self,
        step: Dict,
        current_results: Dict
    ) -> Any:
        """Execute local (non-MCP) actions"""
        action = step['action']
        
        if action == 'retrieve_context':
            return self.memory.get_context()
        
        elif action == 'augment_query':
            # Augment query with context
            context = current_results['data'].get('retrieve_context', {})
            original_query = step['parameters'].get('query', '')
            
            # Add context entities
            entities = context.get('recent_entities', [])
            if entities:
                augmented = f"{original_query} {' '.join(entities[:3])}"
                return {'augmented_query': augmented}
            
            return {'augmented_query': original_query}
        
        elif action == 'rank_results':
            # Simple ranking logic
            search_results = current_results['data'].get('vector_search', [])
            return sorted(search_results, key=lambda x: x.get('score', 0), reverse=True)
        
        elif action == 'decompose_comparison':
            # Extract concepts to compare
            query = step['parameters'].get('query', '')
            # Simplified: split by comparison words
            parts = query.replace(' vs ', '|').replace(' versus ', '|').split('|')
            return {'concepts': [p.strip() for p in parts]}
        
        elif action == 'synthesize_comparison':
            # Combine comparison results
            return {'comparison': 'Comparison synthesis logic here'}
        
        return {}
    
    async def _execute_mcp_tool(
        self,
        mcp_server: str,
        action: str,
        parameters: Dict,
        user_id: Optional[str]
    ) -> Any:
        """Execute MCP server tool"""
        if mcp_server not in self.mcp_clients:
            raise ValueError(f"MCP server not available: {mcp_server}")
        
        client = self.mcp_clients[mcp_server]
        
        # Execute based on MCP server type
        if mcp_server == 'vector_search_mcp':
            return await client.search(**parameters)
        
        elif mcp_server == 'user_preferences_mcp':
            return await client.get_preferences(user_id)
        
        elif mcp_server == 'metadata_mcp':
            return await client.filter_by_metadata(**parameters)
        
        elif mcp_server == 'analytics_mcp':
            return await client.analyze(**parameters)
        
        return {}
    
    async def _evaluate_results(
        self,
        results: Dict,
        intent: Dict
    ) -> tuple[bool, List[str]]:
        """Evaluate if results satisfy the query intent"""
        issues = []
        
        # Check if we have results
        final_data = results.get('data', {})
        if not final_data:
            issues.append("No results obtained")
            return False, issues
        
        # Check result count
        search_results = final_data.get('vector_search', [])
        if len(search_results) == 0:
            issues.append("Zero search results")
        
        # Check if all steps succeeded
        failed_steps = [s for s in results.get('steps', []) if not s.get('success')]
        if failed_steps:
            issues.append(f"{len(failed_steps)} steps failed")
        
        # If high complexity query, need at least 5 results
        if intent.get('complexity') == 'high' and len(search_results) < 5:
            issues.append("Insufficient results for complex query")
        
        is_satisfactory = len(issues) == 0
        
        self._add_thought(
            thought=f"Results evaluation: {'satisfactory' if is_satisfactory else 'needs refinement'}",
            action="evaluate_results",
            confidence=0.8 if is_satisfactory else 0.5
        )
        
        return is_satisfactory, issues
    
    async def _synthesize_response(
        self,
        results: Dict,
        intent: Dict,
        plan: ExecutionPlan
    ) -> Dict[str, Any]:
        """Synthesize final response from execution results"""
        response = {
            'query': intent['query'],
            'intent_type': intent['type'],
            'results': [],
            'metadata': {},
            'explanation': None
        }
        
        # Extract final results
        final_data = results.get('data', {})
        
        # Get search results
        if 'vector_search' in final_data:
            response['results'] = final_data['vector_search']
        elif 'personalized_ranking' in final_data:
            response['results'] = final_data['personalized_ranking']
        elif 'rank_results' in final_data:
            response['results'] = final_data['rank_results']
        
        # Add metadata
        response['metadata'] = {
            'execution_steps': len(plan.steps),
            'successful_steps': sum(1 for s in results['steps'] if s.get('success')),
            'total_results': len(response['results'])
        }
        
        # Generate explanation
        response['explanation'] = self._generate_explanation(intent, results)
        
        return response
    
    def _generate_explanation(self, intent: Dict, results: Dict) -> str:
        """Generate natural language explanation of results"""
        query_type = intent['type']
        
        explanations = {
            'simple_search': f"Found relevant content for '{intent['query']}'",
            'filtered_search': f"Searched for '{intent['query']}' with filters applied",
            'personalized_search': f"Found personalized results based on your preferences",
            'contextual_search': f"Found content related to your previous queries",
            'comparative_search': f"Compared different aspects as requested"
        }
        
        return explanations.get(query_type, "Search completed successfully")
    
    def _add_thought(
        self,
        thought: str,
        action: str,
        tool: Optional[str] = None,
        confidence: float = 1.0
    ):
        """Add agent reasoning step"""
        agent_thought = AgentThought(
            step_number=len(self.thoughts) + 1,
            thought=thought,
            action=action,
            tool=tool,
            confidence=confidence
        )
        self.thoughts.append(agent_thought)
        logger.debug(f"Agent thought: {thought}")
    
    def _serialize_thought(self, thought: AgentThought) -> Dict:
        """Serialize thought for response"""
        return {
            'step': thought.step_number,
            'thought': thought.thought,
            'action': thought.action,
            'tool': thought.tool,
            'confidence': thought.confidence
        }
    
    def clear_conversation(self):
        """Clear conversation memory"""
        self.memory.clear()
        self.thoughts = []
        self.state = AgentState.IDLE


# Singleton instance
_orchestrator_instance = None


def get_orchestrator(mcp_clients: Dict[str, Any]) -> AgentOrchestrator:
    """Get or create orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = AgentOrchestrator(mcp_clients)
    return _orchestrator_instance