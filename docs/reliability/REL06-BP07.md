---
title: REL06-BP07 - Monitor end-to-end tracing of requests through your system
layout: default
parent: REL06 - How do you monitor workload resources?
grand_parent: Reliability
nav_order: 7
---

# REL06-BP07: Monitor end-to-end tracing of requests through your system

## Overview

Implement comprehensive distributed tracing to monitor requests as they flow through your entire system architecture. End-to-end tracing provides visibility into request paths, performance bottlenecks, error propagation, and service dependencies, enabling rapid troubleshooting and optimization of complex distributed systems.

## Implementation Steps

### 1. Design Distributed Tracing Architecture
- Implement trace context propagation across all services
- Design trace sampling strategies for performance and cost optimization
- Establish trace correlation and span relationship modeling
- Configure trace data retention and storage policies

### 2. Instrument Applications and Services
- Add tracing instrumentation to application code
- Configure automatic instrumentation for frameworks and libraries
- Implement custom spans for business logic and critical operations
- Establish trace metadata and tagging strategies

### 3. Configure Service Mesh and Infrastructure Tracing
- Implement service mesh tracing for network-level visibility
- Configure load balancer and API gateway tracing
- Enable database and cache operation tracing
- Establish infrastructure component trace integration

### 4. Set Up Trace Collection and Processing
- Configure trace collectors and aggregation pipelines
- Implement trace data enrichment and correlation
- Design trace data processing and analysis workflows
- Establish real-time trace streaming and batch processing

### 5. Create Trace Analysis and Visualization
- Implement trace search and filtering capabilities
- Configure service dependency mapping and topology visualization
- Design performance analysis and bottleneck identification
- Establish error tracking and root cause analysis

### 6. Monitor and Optimize Tracing Performance
- Track tracing overhead and system performance impact
- Optimize sampling rates and trace data volume
- Monitor trace collection completeness and accuracy
- Implement continuous improvement based on trace insights

## Implementation Examples

### Example 1: Comprehensive Distributed Tracing System
```python
import boto3
import json
import logging
import asyncio
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from contextlib import contextmanager

class SpanKind(Enum):
    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"
    INTERNAL = "internal"

class SpanStatus(Enum):
    OK = "ok"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"

@dataclass
class TraceContext:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    trace_flags: int
    trace_state: str

@dataclass
class Span:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    operation_name: str
    service_name: str
    span_kind: SpanKind
    start_time: datetime
    end_time: Optional[datetime]
    duration_ms: Optional[float]
    status: SpanStatus
    tags: Dict[str, Any]
    logs: List[Dict[str, Any]]
    baggage: Dict[str, str]

@dataclass
class Trace:
    trace_id: str
    spans: List[Span]
    root_span: Optional[Span]
    start_time: datetime
    end_time: Optional[datetime]
    duration_ms: Optional[float]
    service_count: int
    span_count: int
    error_count: int

class DistributedTracer:
    """Comprehensive distributed tracing system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.service_name = config.get('service_name', 'unknown-service')
        
        # AWS clients
        self.xray = boto3.client('xray')
        self.cloudwatch = boto3.client('cloudwatch')
        self.dynamodb = boto3.resource('dynamodb')
        self.kinesis = boto3.client('kinesis')
        
        # Storage
        self.traces_table = self.dynamodb.Table(config.get('traces_table', 'distributed-traces'))
        self.spans_table = self.dynamodb.Table(config.get('spans_table', 'trace-spans'))
        
        # Tracing configuration
        self.sampling_rate = config.get('sampling_rate', 0.1)  # 10% sampling
        self.max_span_duration = config.get('max_span_duration', 300000)  # 5 minutes
        
        # Thread-local storage for trace context
        self.local = threading.local()
        
        # Active spans and traces
        self.active_spans = {}
        self.completed_traces = {}
        
    def start_trace(self, operation_name: str, **kwargs) -> str:
        """Start a new distributed trace"""
        try:
            trace_id = self._generate_trace_id()
            span_id = self._generate_span_id()
            
            # Create root span
            root_span = Span(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=None,
                operation_name=operation_name,
                service_name=self.service_name,
                span_kind=SpanKind.SERVER,
                start_time=datetime.utcnow(),
                end_time=None,
                duration_ms=None,
                status=SpanStatus.OK,
                tags=kwargs,
                logs=[],
                baggage={}
            )
            
            # Set trace context
            trace_context = TraceContext(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=None,
                trace_flags=1 if self._should_sample() else 0,
                trace_state=""
            )
            
            self._set_trace_context(trace_context)
            self.active_spans[span_id] = root_span
            
            logging.info(f"Started trace {trace_id} with root span {span_id}")
            return trace_id
            
        except Exception as e:
            logging.error(f"Failed to start trace: {str(e)}")
            return ""
    
    @contextmanager
    def start_span(self, operation_name: str, span_kind: SpanKind = SpanKind.INTERNAL, **kwargs):
        """Context manager for creating spans"""
        span = None
        try:
            span = self._create_span(operation_name, span_kind, **kwargs)
            yield span
        except Exception as e:
            if span:
                span.status = SpanStatus.ERROR
                span.tags['error'] = str(e)
                self._add_span_log(span, 'error', {'message': str(e)})
            raise
        finally:
            if span:
                self._finish_span(span)
    
    def _create_span(self, operation_name: str, span_kind: SpanKind, **kwargs) -> Span:
        """Create a new span"""
        try:
            current_context = self._get_trace_context()
            if not current_context:
                # Start new trace if no context exists
                trace_id = self.start_trace(operation_name, **kwargs)
                current_context = self._get_trace_context()
            
            span_id = self._generate_span_id()
            
            span = Span(
                trace_id=current_context.trace_id,
                span_id=span_id,
                parent_span_id=current_context.span_id,
                operation_name=operation_name,
                service_name=self.service_name,
                span_kind=span_kind,
                start_time=datetime.utcnow(),
                end_time=None,
                duration_ms=None,
                status=SpanStatus.OK,
                tags=kwargs,
                logs=[],
                baggage={}
            )
            
            # Update trace context
            new_context = TraceContext(
                trace_id=current_context.trace_id,
                span_id=span_id,
                parent_span_id=current_context.span_id,
                trace_flags=current_context.trace_flags,
                trace_state=current_context.trace_state
            )
            
            self._set_trace_context(new_context)
            self.active_spans[span_id] = span
            
            return span
            
        except Exception as e:
            logging.error(f"Failed to create span: {str(e)}")
            raise
    
    def _finish_span(self, span: Span):
        """Finish and record a span"""
        try:
            span.end_time = datetime.utcnow()
            span.duration_ms = (span.end_time - span.start_time).total_seconds() * 1000
            
            # Remove from active spans
            if span.span_id in self.active_spans:
                del self.active_spans[span.span_id]
            
            # Store span
            asyncio.create_task(self._store_span(span))
            
            # Check if trace is complete
            asyncio.create_task(self._check_trace_completion(span.trace_id))
            
            logging.debug(f"Finished span {span.span_id} in {span.duration_ms:.2f}ms")
            
        except Exception as e:
            logging.error(f"Failed to finish span: {str(e)}")
    
    def add_span_tag(self, key: str, value: Any):
        """Add tag to current span"""
        try:
            context = self._get_trace_context()
            if context and context.span_id in self.active_spans:
                span = self.active_spans[context.span_id]
                span.tags[key] = value
                
        except Exception as e:
            logging.error(f"Failed to add span tag: {str(e)}")
    
    def add_span_log(self, level: str, message: str, **kwargs):
        """Add log entry to current span"""
        try:
            context = self._get_trace_context()
            if context and context.span_id in self.active_spans:
                span = self.active_spans[context.span_id]
                self._add_span_log(span, level, {'message': message, **kwargs})
                
        except Exception as e:
            logging.error(f"Failed to add span log: {str(e)}")
    
    def _add_span_log(self, span: Span, level: str, fields: Dict[str, Any]):
        """Add log entry to span"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'fields': fields
        }
        span.logs.append(log_entry)
    
    def inject_trace_context(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Inject trace context into HTTP headers"""
        try:
            context = self._get_trace_context()
            if context:
                headers['X-Trace-Id'] = context.trace_id
                headers['X-Span-Id'] = context.span_id
                if context.parent_span_id:
                    headers['X-Parent-Span-Id'] = context.parent_span_id
                headers['X-Trace-Flags'] = str(context.trace_flags)
                if context.trace_state:
                    headers['X-Trace-State'] = context.trace_state
            
            return headers
            
        except Exception as e:
            logging.error(f"Failed to inject trace context: {str(e)}")
            return headers
    
    def extract_trace_context(self, headers: Dict[str, str]) -> Optional[TraceContext]:
        """Extract trace context from HTTP headers"""
        try:
            trace_id = headers.get('X-Trace-Id')
            span_id = headers.get('X-Span-Id')
            
            if trace_id and span_id:
                return TraceContext(
                    trace_id=trace_id,
                    span_id=span_id,
                    parent_span_id=headers.get('X-Parent-Span-Id'),
                    trace_flags=int(headers.get('X-Trace-Flags', '0')),
                    trace_state=headers.get('X-Trace-State', '')
                )
            
            return None
            
        except Exception as e:
            logging.error(f"Failed to extract trace context: {str(e)}")
            return None
    
    def set_extracted_context(self, context: TraceContext):
        """Set extracted trace context as current context"""
        self._set_trace_context(context)
    
    def _generate_trace_id(self) -> str:
        """Generate unique trace ID"""
        return f"{int(time.time())}-{uuid.uuid4().hex[:16]}"
    
    def _generate_span_id(self) -> str:
        """Generate unique span ID"""
        return uuid.uuid4().hex[:16]
    
    def _should_sample(self) -> bool:
        """Determine if trace should be sampled"""
        import random
        return random.random() < self.sampling_rate
    
    def _get_trace_context(self) -> Optional[TraceContext]:
        """Get current trace context from thread-local storage"""
        return getattr(self.local, 'trace_context', None)
    
    def _set_trace_context(self, context: TraceContext):
        """Set trace context in thread-local storage"""
        self.local.trace_context = context
    
    async def _store_span(self, span: Span):
        """Store span in DynamoDB"""
        try:
            span_dict = asdict(span)
            span_dict['start_time'] = span.start_time.isoformat()
            if span.end_time:
                span_dict['end_time'] = span.end_time.isoformat()
            
            self.spans_table.put_item(Item=span_dict)
            
            # Also send to Kinesis for real-time processing
            await self._send_span_to_kinesis(span)
            
        except Exception as e:
            logging.error(f"Failed to store span: {str(e)}")
    
    async def _send_span_to_kinesis(self, span: Span):
        """Send span to Kinesis for real-time processing"""
        try:
            span_data = {
                'trace_id': span.trace_id,
                'span_id': span.span_id,
                'parent_span_id': span.parent_span_id,
                'operation_name': span.operation_name,
                'service_name': span.service_name,
                'duration_ms': span.duration_ms,
                'status': span.status.value,
                'tags': span.tags,
                'timestamp': span.start_time.isoformat()
            }
            
            self.kinesis.put_record(
                StreamName=self.config.get('kinesis_stream', 'trace-spans'),
                Data=json.dumps(span_data),
                PartitionKey=span.trace_id
            )
            
        except Exception as e:
            logging.error(f"Failed to send span to Kinesis: {str(e)}")
    
    async def _check_trace_completion(self, trace_id: str):
        """Check if trace is complete and process it"""
        try:
            # Get all spans for this trace
            response = self.spans_table.query(
                IndexName='trace-id-index',
                KeyConditionExpression='trace_id = :trace_id',
                ExpressionAttributeValues={':trace_id': trace_id}
            )
            
            spans = []
            for item in response['Items']:
                span = Span(**item)
                spans.append(span)
            
            # Check if all spans are complete
            incomplete_spans = [s for s in spans if s.end_time is None]
            if incomplete_spans:
                return  # Trace not yet complete
            
            # Create trace summary
            trace = self._create_trace_summary(trace_id, spans)
            
            # Store trace summary
            await self._store_trace(trace)
            
            # Analyze trace for insights
            await self._analyze_trace(trace)
            
        except Exception as e:
            logging.error(f"Failed to check trace completion: {str(e)}")
    
    def _create_trace_summary(self, trace_id: str, spans: List[Span]) -> Trace:
        """Create trace summary from spans"""
        try:
            # Find root span
            root_span = next((s for s in spans if s.parent_span_id is None), None)
            
            # Calculate trace metrics
            start_time = min(s.start_time for s in spans)
            end_time = max(s.end_time for s in spans if s.end_time)
            duration_ms = (end_time - start_time).total_seconds() * 1000 if end_time else None
            
            # Count services and errors
            services = set(s.service_name for s in spans)
            error_spans = [s for s in spans if s.status == SpanStatus.ERROR]
            
            return Trace(
                trace_id=trace_id,
                spans=spans,
                root_span=root_span,
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                service_count=len(services),
                span_count=len(spans),
                error_count=len(error_spans)
            )
            
        except Exception as e:
            logging.error(f"Failed to create trace summary: {str(e)}")
            raise
    
    async def _store_trace(self, trace: Trace):
        """Store trace summary in DynamoDB"""
        try:
            trace_dict = {
                'trace_id': trace.trace_id,
                'start_time': trace.start_time.isoformat(),
                'end_time': trace.end_time.isoformat() if trace.end_time else None,
                'duration_ms': trace.duration_ms,
                'service_count': trace.service_count,
                'span_count': trace.span_count,
                'error_count': trace.error_count,
                'root_operation': trace.root_span.operation_name if trace.root_span else None,
                'services': list(set(s.service_name for s in trace.spans))
            }
            
            self.traces_table.put_item(Item=trace_dict)
            
        except Exception as e:
            logging.error(f"Failed to store trace: {str(e)}")
    
    async def _analyze_trace(self, trace: Trace):
        """Analyze trace for performance insights"""
        try:
            insights = []
            
            # Check for slow operations
            if trace.duration_ms and trace.duration_ms > 5000:  # 5 seconds
                insights.append({
                    'type': 'slow_trace',
                    'message': f'Trace duration {trace.duration_ms:.0f}ms exceeds threshold',
                    'severity': 'warning'
                })
            
            # Check for errors
            if trace.error_count > 0:
                insights.append({
                    'type': 'trace_errors',
                    'message': f'Trace contains {trace.error_count} error(s)',
                    'severity': 'error'
                })
            
            # Check for service dependencies
            if trace.service_count > 5:
                insights.append({
                    'type': 'high_service_count',
                    'message': f'Trace spans {trace.service_count} services',
                    'severity': 'info'
                })
            
            # Send insights to CloudWatch
            for insight in insights:
                await self._send_trace_insight(trace.trace_id, insight)
            
        except Exception as e:
            logging.error(f"Failed to analyze trace: {str(e)}")
    
    async def _send_trace_insight(self, trace_id: str, insight: Dict[str, Any]):
        """Send trace insight to CloudWatch"""
        try:
            self.cloudwatch.put_metric_data(
                Namespace='DistributedTracing/Insights',
                MetricData=[
                    {
                        'MetricName': insight['type'],
                        'Value': 1,
                        'Unit': 'Count',
                        'Dimensions': [
                            {
                                'Name': 'Severity',
                                'Value': insight['severity']
                            },
                            {
                                'Name': 'ServiceName',
                                'Value': self.service_name
                            }
                        ]
                    }
                ]
            )
            
        except Exception as e:
            logging.error(f"Failed to send trace insight: {str(e)}")

# Usage example
async def main():
    config = {
        'service_name': 'user-service',
        'traces_table': 'distributed-traces',
        'spans_table': 'trace-spans',
        'kinesis_stream': 'trace-spans',
        'sampling_rate': 0.1
    }
    
    # Initialize tracer
    tracer = DistributedTracer(config)
    
    # Start a trace
    trace_id = tracer.start_trace('process_user_request', user_id='12345')
    
    # Create spans for different operations
    with tracer.start_span('validate_user', SpanKind.INTERNAL) as span:
        tracer.add_span_tag('user_id', '12345')
        tracer.add_span_log('info', 'Validating user credentials')
        # Simulate work
        await asyncio.sleep(0.1)
    
    with tracer.start_span('fetch_user_data', SpanKind.CLIENT) as span:
        tracer.add_span_tag('database', 'users_db')
        tracer.add_span_log('info', 'Fetching user data from database')
        # Simulate database call
        await asyncio.sleep(0.2)
    
    with tracer.start_span('process_business_logic', SpanKind.INTERNAL) as span:
        tracer.add_span_tag('operation', 'calculate_recommendations')
        # Simulate processing
        await asyncio.sleep(0.15)
    
    print(f"Completed trace: {trace_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **AWS X-Ray**: Distributed tracing service for end-to-end request tracking
- **Amazon CloudWatch**: Metrics and logs integration for trace analysis
- **Amazon Kinesis**: Real-time trace data streaming and processing
- **Amazon DynamoDB**: Storage for trace data, spans, and metadata
- **AWS Lambda**: Serverless functions for trace processing and analysis
- **Amazon API Gateway**: API-level tracing and request correlation
- **Elastic Load Balancing**: Load balancer tracing and request routing visibility
- **Amazon ECS/EKS**: Container-based service tracing and orchestration
- **Amazon RDS**: Database query tracing and performance monitoring
- **Amazon ElastiCache**: Cache operation tracing and hit/miss analysis
- **AWS Step Functions**: Workflow tracing and state machine visibility
- **Amazon SQS/SNS**: Message queue and notification tracing
- **AWS AppSync**: GraphQL API tracing and resolver performance
- **Amazon Timestream**: Time-series storage for trace metrics and analytics
- **Amazon OpenSearch**: Trace search, analysis, and visualization

## Benefits

- **End-to-End Visibility**: Complete request flow visibility across distributed systems
- **Performance Optimization**: Identify bottlenecks and optimize critical paths
- **Error Tracking**: Trace error propagation and identify root causes
- **Service Dependencies**: Understand service interactions and dependencies
- **Latency Analysis**: Measure and optimize request latency across services
- **Capacity Planning**: Understand resource utilization patterns
- **Troubleshooting**: Rapid issue identification and resolution
- **Business Intelligence**: Correlate technical metrics with business outcomes
- **Compliance**: Audit trails for regulatory and security requirements
- **Continuous Improvement**: Data-driven optimization and enhancement

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Monitor End-to-End Tracing](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_monitor_aws_resources_end_to_end.html)
- [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [Amazon Kinesis Developer Guide](https://docs.aws.amazon.com/kinesis/latest/dev/)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/latest/developerguide/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/)
- [Distributed Tracing Best Practices](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [OpenTelemetry on AWS](https://aws-otel.github.io/docs/introduction)
- [AWS Distro for OpenTelemetry](https://aws.amazon.com/otel/)
- [Microservices Observability](https://aws.amazon.com/builders-library/)
