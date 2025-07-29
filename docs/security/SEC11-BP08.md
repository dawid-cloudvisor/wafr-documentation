---
title: SEC11-BP08 - Build a program that embeds security ownership in workload teams
layout: default
parent: SEC11 - How do you incorporate and validate the security properties of applications?
grand_parent: Security
nav_order: 8
---

<div class="pillar-header">
  <h1>SEC11-BP08: Build a program that embeds security ownership in workload teams</h1>
  <p>Build a program that embeds security ownership and accountability within workload teams. This includes providing security training, establishing clear security responsibilities, implementing security champions programs, and creating feedback mechanisms to continuously improve security practices.</p>
</div>

## Implementation guidance

Embedding security ownership in workload teams is essential for creating a security-conscious culture where every team member takes responsibility for security outcomes. By distributing security knowledge and accountability throughout the organization, you create multiple layers of defense and ensure security is considered at every stage of development and operations.

### Key steps for implementing this best practice:

1. **Establish security ownership framework**:
   - Define clear security roles and responsibilities for each team member
   - Create security accountability metrics and KPIs
   - Implement security ownership documentation and processes
   - Establish security decision-making authority within teams
   - Create escalation paths for security issues and incidents

2. **Implement security champions program**:
   - Identify and train security champions within each workload team
   - Provide advanced security training and certification opportunities
   - Create security champion networks and communities of practice
   - Establish regular security champion meetings and knowledge sharing
   - Recognize and reward security champion contributions

3. **Provide comprehensive security training**:
   - Develop role-based security training programs
   - Implement hands-on security workshops and labs
   - Create security awareness campaigns and communications
   - Establish continuous learning paths and certification programs
   - Measure training effectiveness and knowledge retention

4. **Create security feedback and improvement mechanisms**:
   - Implement security metrics and dashboards for teams
   - Establish regular security reviews and retrospectives
   - Create security incident post-mortem processes
   - Implement security suggestion and improvement programs
   - Establish security maturity assessment frameworks

5. **Integrate security into team processes**:
   - Embed security requirements in development workflows
   - Implement security checkpoints in deployment pipelines
   - Create security-focused code review processes
   - Establish security testing and validation procedures
   - Integrate security considerations into planning and design

6. **Foster security culture and collaboration**:
   - Promote security-first mindset across all team activities
   - Encourage proactive security thinking and innovation
   - Create cross-team security collaboration opportunities
   - Establish security knowledge sharing platforms
   - Celebrate security achievements and learnings

## Implementation examples

### Example 1: Security champions program management system

```python
import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

class SecurityChampionsProgram:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        self.ses = boto3.client('ses')
        self.lambda_client = boto3.client('lambda')
        
        # DynamoDB tables
        self.champions_table = self.dynamodb.Table('SecurityChampions')
        self.training_table = self.dynamodb.Table('SecurityTraining')
        self.activities_table = self.dynamodb.Table('SecurityActivities')
        self.metrics_table = self.dynamodb.Table('SecurityMetrics')
        
        # Program configuration
        self.program_config = {
            'champion_requirements': {
                'min_training_hours': 40,
                'required_certifications': ['AWS Security Specialty', 'Security+'],
                'min_activities_per_quarter': 4,
                'peer_nominations_required': 2
            },
            'training_tracks': {
                'foundation': {
                    'duration_hours': 16,
                    'modules': ['Security Fundamentals', 'Threat Modeling', 'Secure Coding']
                },
                'advanced': {
                    'duration_hours': 24,
                    'modules': ['Advanced Threats', 'Incident Response', 'Security Architecture']
                },
                'leadership': {
                    'duration_hours': 12,
                    'modules': ['Security Leadership', 'Risk Management', 'Compliance']
                }
            },
            'recognition_levels': {
                'bronze': {'points_required': 100, 'benefits': ['Certificate', 'Badge']},
                'silver': {'points_required': 250, 'benefits': ['Certificate', 'Badge', 'Conference Ticket']},
                'gold': {'points_required': 500, 'benefits': ['Certificate', 'Badge', 'Conference Ticket', 'Bonus']}
            }
        }
    
    def nominate_champion(self, nominee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Nominate a team member as a security champion"""
        
        nomination_id = str(uuid.uuid4())
        
        nomination = {
            'nomination_id': nomination_id,
            'nominee_email': nominee_data['email'],
            'nominee_name': nominee_data['name'],
            'team': nominee_data['team'],
            'department': nominee_data['department'],
            'nominator_email': nominee_data['nominator_email'],
            'nominator_name': nominee_data['nominator_name'],
            'nomination_reason': nominee_data['reason'],
            'skills_assessment': nominee_data.get('skills', {}),
            'nomination_timestamp': datetime.utcnow().isoformat(),
            'status': 'pending_review',
            'review_scores': [],
            'final_decision': None
        }
        
        # Store nomination
        self.champions_table.put_item(Item=nomination)
        
        # Send notification to security team for review
        self.send_nomination_notification(nomination)
        
        # Send confirmation to nominator
        self.send_nomination_confirmation(nomination)
        
        return {
            'nomination_id': nomination_id,
            'status': 'submitted',
            'next_steps': 'Nomination will be reviewed by the security team within 5 business days'
        }
    
    def review_nomination(self, nomination_id: str, reviewer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Review and score a champion nomination"""
        
        # Get nomination
        response = self.champions_table.get_item(Key={'nomination_id': nomination_id})
        
        if 'Item' not in response:
            return {'error': 'Nomination not found'}
        
        nomination = response['Item']
        
        # Add review score
        review_score = {
            'reviewer_email': reviewer_data['reviewer_email'],
            'reviewer_name': reviewer_data['reviewer_name'],
            'technical_score': reviewer_data['technical_score'],  # 1-10
            'leadership_score': reviewer_data['leadership_score'],  # 1-10
            'communication_score': reviewer_data['communication_score'],  # 1-10
            'motivation_score': reviewer_data['motivation_score'],  # 1-10
            'overall_score': reviewer_data['overall_score'],  # 1-10
            'comments': reviewer_data.get('comments', ''),
            'recommendation': reviewer_data['recommendation'],  # approve/reject/needs_more_info
            'review_timestamp': datetime.utcnow().isoformat()
        }
        
        # Update nomination with review
        nomination['review_scores'].append(review_score)
        
        # Check if we have enough reviews to make a decision
        if len(nomination['review_scores']) >= 2:
            decision = self.make_nomination_decision(nomination)
            nomination['final_decision'] = decision
            nomination['status'] = 'approved' if decision['approved'] else 'rejected'
            
            # Process approved nomination
            if decision['approved']:
                champion_result = self.onboard_new_champion(nomination)
                nomination['champion_id'] = champion_result['champion_id']
        
        # Update nomination
        self.champions_table.put_item(Item=nomination)
        
        # Send status update
        self.send_nomination_status_update(nomination)
        
        return {
            'nomination_id': nomination_id,
            'status': nomination['status'],
            'reviews_completed': len(nomination['review_scores']),
            'decision': nomination.get('final_decision')
        }
    
    def onboard_new_champion(self, nomination: Dict[str, Any]) -> Dict[str, Any]:
        """Onboard a newly approved security champion"""
        
        champion_id = str(uuid.uuid4())
        
        champion = {
            'champion_id': champion_id,
            'email': nomination['nominee_email'],
            'name': nomination['nominee_name'],
            'team': nomination['team'],
            'department': nomination['department'],
            'start_date': datetime.utcnow().isoformat(),
            'status': 'active',
            'level': 'bronze',
            'points': 0,
            'training_completed': [],
            'certifications': [],
            'activities': [],
            'mentorship': {
                'mentor_assigned': False,
                'mentor_id': None,
                'mentorship_start_date': None
            },
            'performance_metrics': {
                'training_hours': 0,
                'activities_completed': 0,
                'team_impact_score': 0,
                'peer_feedback_score': 0
            }
        }
        
        # Store champion record
        self.champions_table.put_item(Item=champion)
        
        # Assign mentor
        mentor_result = self.assign_mentor(champion_id)
        if mentor_result['mentor_assigned']:
            champion['mentorship'] = mentor_result
            self.champions_table.put_item(Item=champion)
        
        # Create onboarding training plan
        training_plan = self.create_training_plan(champion_id, 'foundation')
        
        # Send welcome package
        self.send_champion_welcome_package(champion, training_plan)
        
        # Schedule initial check-in
        self.schedule_champion_checkin(champion_id, days_from_now=30)
        
        return {
            'champion_id': champion_id,
            'onboarding_status': 'completed',
            'training_plan_id': training_plan['plan_id'],
            'mentor_assigned': mentor_result['mentor_assigned']
        }
    
    def create_training_plan(self, champion_id: str, track: str) -> Dict[str, Any]:
        """Create personalized training plan for champion"""
        
        plan_id = str(uuid.uuid4())
        track_config = self.program_config['training_tracks'][track]
        
        training_plan = {
            'plan_id': plan_id,
            'champion_id': champion_id,
            'track': track,
            'total_hours': track_config['duration_hours'],
            'modules': [],
            'created_date': datetime.utcnow().isoformat(),
            'target_completion_date': (datetime.utcnow() + timedelta(days=90)).isoformat(),
            'status': 'active',
            'progress': {
                'completed_modules': 0,
                'total_modules': len(track_config['modules']),
                'completion_percentage': 0
            }
        }
        
        # Create training modules
        for i, module_name in enumerate(track_config['modules']):
            module = {
                'module_id': str(uuid.uuid4()),
                'name': module_name,
                'order': i + 1,
                'estimated_hours': track_config['duration_hours'] // len(track_config['modules']),
                'status': 'not_started',
                'start_date': None,
                'completion_date': None,
                'score': None,
                'resources': self.get_training_resources(module_name)
            }
            training_plan['modules'].append(module)
        
        # Store training plan
        self.training_table.put_item(Item=training_plan)
        
        return training_plan
    
    def track_champion_activity(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track and record champion security activities"""
        
        activity_id = str(uuid.uuid4())
        
        activity = {
            'activity_id': activity_id,
            'champion_id': activity_data['champion_id'],
            'activity_type': activity_data['type'],  # training, presentation, code_review, incident_response, etc.
            'title': activity_data['title'],
            'description': activity_data['description'],
            'date': activity_data['date'],
            'duration_hours': activity_data.get('duration_hours', 0),
            'impact_level': activity_data.get('impact_level', 'medium'),  # low, medium, high
            'team_members_impacted': activity_data.get('team_members_impacted', 0),
            'artifacts': activity_data.get('artifacts', []),  # documents, presentations, code, etc.
            'feedback': activity_data.get('feedback', {}),
            'points_earned': self.calculate_activity_points(activity_data),
            'verification_status': 'pending',
            'verified_by': None,
            'verification_date': None
        }
        
        # Store activity
        self.activities_table.put_item(Item=activity)
        
        # Update champion points (pending verification)
        self.update_champion_points(activity_data['champion_id'], activity['points_earned'], pending=True)
        
        # Send verification request
        self.send_activity_verification_request(activity)
        
        return {
            'activity_id': activity_id,
            'points_earned': activity['points_earned'],
            'verification_status': 'pending'
        }
    
    def verify_champion_activity(self, activity_id: str, verifier_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify and approve champion activity"""
        
        # Get activity
        response = self.activities_table.get_item(Key={'activity_id': activity_id})
        
        if 'Item' not in response:
            return {'error': 'Activity not found'}
        
        activity = response['Item']
        
        # Update verification status
        activity['verification_status'] = verifier_data['status']  # approved, rejected, needs_revision
        activity['verified_by'] = verifier_data['verifier_email']
        activity['verification_date'] = datetime.utcnow().isoformat()
        activity['verification_comments'] = verifier_data.get('comments', '')
        
        # Adjust points if needed
        if verifier_data['status'] == 'approved':
            adjusted_points = verifier_data.get('adjusted_points', activity['points_earned'])
            activity['points_earned'] = adjusted_points
            
            # Update champion points (confirmed)
            self.update_champion_points(activity['champion_id'], adjusted_points, pending=False)
        elif verifier_data['status'] == 'rejected':
            # Remove pending points
            self.update_champion_points(activity['champion_id'], -activity['points_earned'], pending=True)
        
        # Update activity
        self.activities_table.put_item(Item=activity)
        
        # Send notification to champion
        self.send_activity_verification_result(activity)
        
        return {
            'activity_id': activity_id,
            'verification_status': activity['verification_status'],
            'points_awarded': activity['points_earned'] if verifier_data['status'] == 'approved' else 0
        }
    
    def generate_champion_metrics(self, champion_id: str, period: str = 'quarterly') -> Dict[str, Any]:
        """Generate comprehensive metrics for a security champion"""
        
        # Get champion data
        champion_response = self.champions_table.get_item(Key={'champion_id': champion_id})
        
        if 'Item' not in champion_response:
            return {'error': 'Champion not found'}
        
        champion = champion_response['Item']
        
        # Calculate date range
        end_date = datetime.utcnow()
        if period == 'quarterly':
            start_date = end_date - timedelta(days=90)
        elif period == 'monthly':
            start_date = end_date - timedelta(days=30)
        elif period == 'yearly':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = datetime.fromisoformat(champion['start_date'])
        
        # Get activities in period
        activities = self.get_champion_activities(champion_id, start_date, end_date)
        
        # Calculate metrics
        metrics = {
            'champion_id': champion_id,
            'champion_name': champion['name'],
            'period': period,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'current_level': champion['level'],
            'total_points': champion['points'],
            'period_metrics': {
                'activities_completed': len(activities),
                'total_hours_contributed': sum(a.get('duration_hours', 0) for a in activities),
                'points_earned': sum(a.get('points_earned', 0) for a in activities if a.get('verification_status') == 'approved'),
                'team_members_impacted': sum(a.get('team_members_impacted', 0) for a in activities),
                'high_impact_activities': len([a for a in activities if a.get('impact_level') == 'high'])
            },
            'activity_breakdown': self.analyze_activity_breakdown(activities),
            'training_progress': self.get_training_progress(champion_id),
            'peer_feedback': self.get_peer_feedback(champion_id, start_date, end_date),
            'recommendations': self.generate_champion_recommendations(champion, activities)
        }
        
        # Store metrics
        metrics_record = {
            'metric_id': str(uuid.uuid4()),
            'champion_id': champion_id,
            'period': period,
            'generated_date': datetime.utcnow().isoformat(),
            'metrics': metrics
        }
        
        self.metrics_table.put_item(Item=metrics_record)
        
        return metrics
    
    def calculate_activity_points(self, activity_data: Dict[str, Any]) -> int:
        """Calculate points for a champion activity"""
        
        base_points = {
            'training': 10,
            'presentation': 20,
            'code_review': 15,
            'incident_response': 25,
            'mentoring': 20,
            'documentation': 15,
            'tool_development': 30,
            'vulnerability_discovery': 40,
            'process_improvement': 25
        }
        
        activity_type = activity_data['type']
        points = base_points.get(activity_type, 10)
        
        # Multiply by impact level
        impact_multiplier = {
            'low': 1.0,
            'medium': 1.5,
            'high': 2.0
        }
        
        points *= impact_multiplier.get(activity_data.get('impact_level', 'medium'), 1.5)
        
        # Add bonus for team impact
        team_impact = activity_data.get('team_members_impacted', 0)
        if team_impact > 10:
            points *= 1.5
        elif team_impact > 5:
            points *= 1.2
        
        return int(points)
    
    def assign_mentor(self, champion_id: str) -> Dict[str, Any]:
        """Assign a mentor to a new security champion"""
        
        # Find available mentors
        available_mentors = self.find_available_mentors()
        
        if not available_mentors:
            return {
                'mentor_assigned': False,
                'reason': 'No available mentors at this time'
            }
        
        # Select best mentor based on team, department, and availability
        selected_mentor = self.select_best_mentor(champion_id, available_mentors)
        
        # Create mentorship relationship
        mentorship = {
            'mentor_assigned': True,
            'mentor_id': selected_mentor['champion_id'],
            'mentor_name': selected_mentor['name'],
            'mentorship_start_date': datetime.utcnow().isoformat(),
            'mentorship_duration_months': 6,
            'meeting_frequency': 'bi-weekly',
            'goals': [
                'Complete foundation training track',
                'Lead first security presentation',
                'Participate in security code reviews',
                'Develop security expertise in team domain'
            ]
        }
        
        # Update mentor's mentee list
        self.add_mentee_to_mentor(selected_mentor['champion_id'], champion_id)
        
        # Send mentorship notifications
        self.send_mentorship_notifications(champion_id, selected_mentor['champion_id'])
        
        return mentorship
    
    def send_nomination_notification(self, nomination: Dict[str, Any]):
        """Send nomination notification to security team"""
        
        message = {
            'subject': f'New Security Champion Nomination: {nomination["nominee_name"]}',
            'body': f"""
A new security champion nomination has been submitted:

Nominee: {nomination['nominee_name']} ({nomination['nominee_email']})
Team: {nomination['team']}
Department: {nomination['department']}
Nominator: {nomination['nominator_name']} ({nomination['nominator_email']})

Reason for Nomination:
{nomination['nomination_reason']}

Please review this nomination in the Security Champions portal.
Nomination ID: {nomination['nomination_id']}
            """,
            'recipients': ['security-team@company.com']
        }
        
        self.send_email_notification(message)
    
    def send_champion_welcome_package(self, champion: Dict[str, Any], training_plan: Dict[str, Any]):
        """Send welcome package to new security champion"""
        
        message = {
            'subject': 'Welcome to the Security Champions Program!',
            'body': f"""
Congratulations {champion['name']}!

You have been selected to join our Security Champions Program. We're excited to have you on board!

Your Champion ID: {champion['champion_id']}
Starting Level: {champion['level']}

Next Steps:
1. Complete your foundation training track ({training_plan['total_hours']} hours)
2. Meet with your assigned mentor
3. Attend the monthly Security Champions meeting
4. Start contributing to your team's security initiatives

Resources:
- Security Champions Portal: https://security-champions.company.com
- Training Materials: https://training.company.com/security
- Slack Channel: #security-champions

Welcome to the team!
Security Champions Program Team
            """,
            'recipients': [champion['email']]
        }
        
        self.send_email_notification(message)
    
    def send_email_notification(self, message: Dict[str, Any]):
        """Send email notification using SES"""
        
        try:
            self.ses.send_email(
                Source='security-champions@company.com',
                Destination={'ToAddresses': message['recipients']},
                Message={
                    'Subject': {'Data': message['subject']},
                    'Body': {'Text': {'Data': message['body']}}
                }
            )
        except Exception as e:
            print(f"Error sending email: {str(e)}")

def lambda_handler(event, context):
    """Lambda function for Security Champions Program management"""
    
    program = SecurityChampionsProgram()
    
    action = event.get('action')
    
    if action == 'nominate_champion':
        result = program.nominate_champion(event['nominee_data'])
    elif action == 'review_nomination':
        result = program.review_nomination(event['nomination_id'], event['reviewer_data'])
    elif action == 'track_activity':
        result = program.track_champion_activity(event['activity_data'])
    elif action == 'verify_activity':
        result = program.verify_champion_activity(event['activity_id'], event['verifier_data'])
    elif action == 'generate_metrics':
        result = program.generate_champion_metrics(event['champion_id'], event.get('period', 'quarterly'))
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```
### Example 2: Security training and competency management system

```python
import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

class SecurityTrainingManager:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        self.lambda_client = boto3.client('lambda')
        self.ses = boto3.client('ses')
        
        # DynamoDB tables
        self.employees_table = self.dynamodb.Table('Employees')
        self.training_catalog_table = self.dynamodb.Table('TrainingCatalog')
        self.training_records_table = self.dynamodb.Table('TrainingRecords')
        self.competency_table = self.dynamodb.Table('SecurityCompetencies')
        self.assessments_table = self.dynamodb.Table('SecurityAssessments')
        
        # Training configuration
        self.training_config = {
            'role_based_requirements': {
                'developer': {
                    'required_courses': [
                        'secure-coding-fundamentals',
                        'owasp-top-10',
                        'threat-modeling-basics',
                        'code-review-security'
                    ],
                    'annual_hours_required': 20,
                    'competency_areas': ['secure_coding', 'vulnerability_assessment', 'code_review']
                },
                'devops': {
                    'required_courses': [
                        'infrastructure-security',
                        'container-security',
                        'pipeline-security',
                        'cloud-security-aws'
                    ],
                    'annual_hours_required': 24,
                    'competency_areas': ['infrastructure_security', 'pipeline_security', 'incident_response']
                },
                'architect': {
                    'required_courses': [
                        'security-architecture',
                        'threat-modeling-advanced',
                        'compliance-frameworks',
                        'risk-assessment'
                    ],
                    'annual_hours_required': 30,
                    'competency_areas': ['security_architecture', 'threat_modeling', 'compliance', 'risk_management']
                },
                'manager': {
                    'required_courses': [
                        'security-leadership',
                        'risk-management',
                        'incident-management',
                        'security-governance'
                    ],
                    'annual_hours_required': 16,
                    'competency_areas': ['security_leadership', 'risk_management', 'governance']
                }
            },
            'competency_levels': {
                'novice': {'score_range': [0, 40], 'description': 'Basic understanding'},
                'competent': {'score_range': [41, 70], 'description': 'Can perform with guidance'},
                'proficient': {'score_range': [71, 85], 'description': 'Can perform independently'},
                'expert': {'score_range': [86, 100], 'description': 'Can teach and mentor others'}
            },
            'assessment_frequency': {
                'initial': 'upon_hire',
                'regular': 'quarterly',
                'post_training': 'immediate',
                'annual': 'yearly'
            }
        }
    
    def create_personalized_training_plan(self, employee_id: str) -> Dict[str, Any]:
        """Create a personalized training plan based on role and current competencies"""
        
        # Get employee information
        employee_response = self.employees_table.get_item(Key={'employee_id': employee_id})
        
        if 'Item' not in employee_response:
            return {'error': 'Employee not found'}
        
        employee = employee_response['Item']
        role = employee.get('role', 'developer')
        
        # Get current competency assessment
        current_competencies = self.get_current_competencies(employee_id)
        
        # Get role requirements
        role_requirements = self.training_config['role_based_requirements'].get(role, 
                           self.training_config['role_based_requirements']['developer'])
        
        # Create training plan
        plan_id = str(uuid.uuid4())
        
        training_plan = {
            'plan_id': plan_id,
            'employee_id': employee_id,
            'employee_name': employee['name'],
            'role': role,
            'created_date': datetime.utcnow().isoformat(),
            'plan_year': datetime.utcnow().year,
            'status': 'active',
            'required_courses': [],
            'recommended_courses': [],
            'competency_goals': [],
            'progress': {
                'courses_completed': 0,
                'total_courses': 0,
                'hours_completed': 0,
                'required_hours': role_requirements['annual_hours_required'],
                'completion_percentage': 0
            }
        }
        
        # Add required courses
        for course_id in role_requirements['required_courses']:
            course_info = self.get_course_info(course_id)
            if course_info and not self.is_course_completed(employee_id, course_id):
                training_plan['required_courses'].append({
                    'course_id': course_id,
                    'course_name': course_info['name'],
                    'duration_hours': course_info['duration_hours'],
                    'priority': 'required',
                    'due_date': (datetime.utcnow() + timedelta(days=90)).isoformat(),
                    'status': 'not_started'
                })
        
        # Add recommended courses based on competency gaps
        recommended_courses = self.identify_recommended_courses(current_competencies, role_requirements)
        training_plan['recommended_courses'] = recommended_courses
        
        # Set competency goals
        for competency_area in role_requirements['competency_areas']:
            current_level = current_competencies.get(competency_area, {}).get('level', 'novice')
            target_level = 'proficient' if current_level in ['novice', 'competent'] else 'expert'
            
            training_plan['competency_goals'].append({
                'competency_area': competency_area,
                'current_level': current_level,
                'target_level': target_level,
                'target_date': (datetime.utcnow() + timedelta(days=180)).isoformat()
            })
        
        # Update progress totals
        training_plan['progress']['total_courses'] = len(training_plan['required_courses']) + len(training_plan['recommended_courses'])
        
        # Store training plan
        self.training_records_table.put_item(Item=training_plan)
        
        # Send training plan notification
        self.send_training_plan_notification(training_plan)
        
        return training_plan
    
    def track_training_completion(self, completion_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track and record training completion"""
        
        completion_id = str(uuid.uuid4())
        
        completion_record = {
            'completion_id': completion_id,
            'employee_id': completion_data['employee_id'],
            'course_id': completion_data['course_id'],
            'completion_date': completion_data['completion_date'],
            'duration_hours': completion_data['duration_hours'],
            'score': completion_data.get('score'),
            'certificate_url': completion_data.get('certificate_url'),
            'instructor': completion_data.get('instructor'),
            'training_method': completion_data.get('method', 'online'),  # online, classroom, workshop
            'feedback': completion_data.get('feedback', {}),
            'verification_status': 'verified' if completion_data.get('auto_verified') else 'pending'
        }
        
        # Store completion record
        self.training_records_table.put_item(Item=completion_record)
        
        # Update employee training plan
        self.update_training_plan_progress(completion_data['employee_id'], completion_data['course_id'])
        
        # Trigger post-training assessment if required
        course_info = self.get_course_info(completion_data['course_id'])
        if course_info and course_info.get('requires_assessment'):
            self.schedule_post_training_assessment(completion_data['employee_id'], completion_data['course_id'])
        
        # Update competency scores
        self.update_competency_scores(completion_data['employee_id'], completion_data['course_id'], completion_data.get('score'))
        
        # Send completion notification
        self.send_training_completion_notification(completion_record)
        
        return {
            'completion_id': completion_id,
            'status': 'recorded',
            'verification_status': completion_record['verification_status']
        }
    
    def conduct_security_assessment(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct security competency assessment"""
        
        assessment_id = str(uuid.uuid4())
        
        assessment = {
            'assessment_id': assessment_id,
            'employee_id': assessment_data['employee_id'],
            'assessment_type': assessment_data['type'],  # initial, quarterly, post_training, annual
            'competency_areas': assessment_data['competency_areas'],
            'assessment_date': datetime.utcnow().isoformat(),
            'assessor': assessment_data.get('assessor'),
            'method': assessment_data.get('method', 'online_quiz'),  # online_quiz, practical_exercise, interview
            'results': {},
            'overall_score': 0,
            'recommendations': [],
            'status': 'in_progress'
        }
        
        # Conduct assessment for each competency area
        total_score = 0
        for competency_area in assessment_data['competency_areas']:
            area_result = self.assess_competency_area(
                assessment_data['employee_id'], 
                competency_area, 
                assessment_data.get('questions', {}).get(competency_area, [])
            )
            
            assessment['results'][competency_area] = area_result
            total_score += area_result['score']
        
        # Calculate overall score
        assessment['overall_score'] = total_score / len(assessment_data['competency_areas'])
        assessment['status'] = 'completed'
        
        # Generate recommendations
        assessment['recommendations'] = self.generate_assessment_recommendations(assessment)
        
        # Store assessment
        self.assessments_table.put_item(Item=assessment)
        
        # Update employee competency records
        self.update_employee_competencies(assessment_data['employee_id'], assessment['results'])
        
        # Send assessment results
        self.send_assessment_results(assessment)
        
        return assessment
    
    def assess_competency_area(self, employee_id: str, competency_area: str, questions: List[Dict]) -> Dict[str, Any]:
        """Assess a specific competency area"""
        
        if not questions:
            # Use default questions for the competency area
            questions = self.get_default_questions(competency_area)
        
        total_points = 0
        earned_points = 0
        
        for question in questions:
            total_points += question.get('points', 1)
            if question.get('correct', False):
                earned_points += question.get('points', 1)
        
        score = (earned_points / total_points * 100) if total_points > 0 else 0
        level = self.determine_competency_level(score)
        
        return {
            'competency_area': competency_area,
            'score': score,
            'level': level,
            'questions_answered': len(questions),
            'correct_answers': sum(1 for q in questions if q.get('correct', False)),
            'areas_for_improvement': self.identify_improvement_areas(competency_area, questions)
        }
    
    def generate_team_security_dashboard(self, team_id: str) -> Dict[str, Any]:
        """Generate security training and competency dashboard for a team"""
        
        # Get team members
        team_members = self.get_team_members(team_id)
        
        dashboard = {
            'team_id': team_id,
            'generated_date': datetime.utcnow().isoformat(),
            'team_size': len(team_members),
            'overall_metrics': {
                'training_compliance_rate': 0,
                'average_competency_score': 0,
                'security_champions': 0,
                'overdue_training': 0
            },
            'competency_breakdown': {},
            'training_status': {
                'completed_this_quarter': 0,
                'in_progress': 0,
                'overdue': 0,
                'upcoming_due': 0
            },
            'top_performers': [],
            'improvement_opportunities': [],
            'recommended_actions': []
        }
        
        total_compliance = 0
        total_competency_score = 0
        competency_scores = {}
        
        for member in team_members:
            employee_id = member['employee_id']
            
            # Get training compliance
            compliance = self.calculate_training_compliance(employee_id)
            total_compliance += compliance['compliance_percentage']
            
            # Get competency scores
            competencies = self.get_current_competencies(employee_id)
            member_avg_score = 0
            
            for area, comp_data in competencies.items():
                score = comp_data.get('score', 0)
                if area not in competency_scores:
                    competency_scores[area] = []
                competency_scores[area].append(score)
                member_avg_score += score
            
            if competencies:
                member_avg_score /= len(competencies)
                total_competency_score += member_avg_score
            
            # Check for security champion status
            if member.get('security_champion', False):
                dashboard['overall_metrics']['security_champions'] += 1
            
            # Check for overdue training
            if compliance['overdue_courses'] > 0:
                dashboard['overall_metrics']['overdue_training'] += 1
        
        # Calculate overall metrics
        if team_members:
            dashboard['overall_metrics']['training_compliance_rate'] = total_compliance / len(team_members)
            dashboard['overall_metrics']['average_competency_score'] = total_competency_score / len(team_members)
        
        # Calculate competency breakdown
        for area, scores in competency_scores.items():
            dashboard['competency_breakdown'][area] = {
                'average_score': sum(scores) / len(scores),
                'level_distribution': self.calculate_level_distribution(scores),
                'improvement_needed': len([s for s in scores if s < 70])
            }
        
        # Identify top performers
        dashboard['top_performers'] = self.identify_top_performers(team_members)
        
        # Generate recommendations
        dashboard['recommended_actions'] = self.generate_team_recommendations(dashboard)
        
        return dashboard
    
    def schedule_training_reminders(self, employee_id: str) -> Dict[str, Any]:
        """Schedule automated training reminders"""
        
        # Get employee training plan
        training_plan = self.get_active_training_plan(employee_id)
        
        if not training_plan:
            return {'error': 'No active training plan found'}
        
        reminders_scheduled = []
        
        # Schedule reminders for required courses
        for course in training_plan.get('required_courses', []):
            if course['status'] == 'not_started':
                due_date = datetime.fromisoformat(course['due_date'])
                
                # Schedule reminder 30 days before due date
                reminder_date = due_date - timedelta(days=30)
                if reminder_date > datetime.utcnow():
                    reminder_id = self.schedule_reminder(
                        employee_id, 
                        course['course_id'], 
                        reminder_date, 
                        'course_due_soon'
                    )
                    reminders_scheduled.append({
                        'reminder_id': reminder_id,
                        'course_id': course['course_id'],
                        'reminder_date': reminder_date.isoformat(),
                        'type': 'course_due_soon'
                    })
                
                # Schedule reminder 7 days before due date
                urgent_reminder_date = due_date - timedelta(days=7)
                if urgent_reminder_date > datetime.utcnow():
                    reminder_id = self.schedule_reminder(
                        employee_id, 
                        course['course_id'], 
                        urgent_reminder_date, 
                        'course_due_urgent'
                    )
                    reminders_scheduled.append({
                        'reminder_id': reminder_id,
                        'course_id': course['course_id'],
                        'reminder_date': urgent_reminder_date.isoformat(),
                        'type': 'course_due_urgent'
                    })
        
        return {
            'employee_id': employee_id,
            'reminders_scheduled': len(reminders_scheduled),
            'reminders': reminders_scheduled
        }
    
    def generate_security_culture_metrics(self, organization_level: str = 'company') -> Dict[str, Any]:
        """Generate organization-wide security culture metrics"""
        
        metrics = {
            'organization_level': organization_level,
            'generated_date': datetime.utcnow().isoformat(),
            'period': 'quarterly',
            'overall_metrics': {
                'total_employees': 0,
                'security_trained_employees': 0,
                'security_champions': 0,
                'average_competency_score': 0,
                'training_compliance_rate': 0
            },
            'competency_trends': {},
            'training_effectiveness': {},
            'security_incidents_correlation': {},
            'culture_indicators': {
                'proactive_security_reports': 0,
                'security_suggestions_submitted': 0,
                'cross_team_security_collaboration': 0,
                'security_innovation_projects': 0
            },
            'recommendations': []
        }
        
        # Get all employees
        all_employees = self.get_all_employees()
        metrics['overall_metrics']['total_employees'] = len(all_employees)
        
        total_competency_score = 0
        total_compliance = 0
        security_champions = 0
        trained_employees = 0
        
        for employee in all_employees:
            employee_id = employee['employee_id']
            
            # Check training status
            compliance = self.calculate_training_compliance(employee_id)
            if compliance['compliance_percentage'] > 0:
                trained_employees += 1
                total_compliance += compliance['compliance_percentage']
            
            # Check competency scores
            competencies = self.get_current_competencies(employee_id)
            if competencies:
                avg_score = sum(comp['score'] for comp in competencies.values()) / len(competencies)
                total_competency_score += avg_score
            
            # Check security champion status
            if employee.get('security_champion', False):
                security_champions += 1
        
        # Calculate overall metrics
        metrics['overall_metrics']['security_trained_employees'] = trained_employees
        metrics['overall_metrics']['security_champions'] = security_champions
        
        if trained_employees > 0:
            metrics['overall_metrics']['training_compliance_rate'] = total_compliance / trained_employees
            metrics['overall_metrics']['average_competency_score'] = total_competency_score / trained_employees
        
        # Generate culture indicators
        metrics['culture_indicators'] = self.calculate_culture_indicators()
        
        # Generate recommendations
        metrics['recommendations'] = self.generate_culture_recommendations(metrics)
        
        return metrics
    
    def send_training_plan_notification(self, training_plan: Dict[str, Any]):
        """Send training plan notification to employee"""
        
        message = {
            'subject': f'Your {training_plan["plan_year"]} Security Training Plan is Ready',
            'body': f"""
Hello {training_plan['employee_name']},

Your personalized security training plan for {training_plan['plan_year']} has been created.

Training Requirements:
- Required Courses: {len(training_plan['required_courses'])}
- Recommended Courses: {len(training_plan['recommended_courses'])}
- Total Hours Required: {training_plan['progress']['required_hours']}

Competency Goals:
{chr(10).join([f"- {goal['competency_area']}: {goal['current_level']} → {goal['target_level']}" for goal in training_plan['competency_goals']])}

Please log into the training portal to begin your courses.
Training Portal: https://training.company.com/security

Best regards,
Security Training Team
            """,
            'recipients': [self.get_employee_email(training_plan['employee_id'])]
        }
        
        self.send_email_notification(message)
    
    def send_email_notification(self, message: Dict[str, Any]):
        """Send email notification using SES"""
        
        try:
            self.ses.send_email(
                Source='security-training@company.com',
                Destination={'ToAddresses': message['recipients']},
                Message={
                    'Subject': {'Data': message['subject']},
                    'Body': {'Text': {'Data': message['body']}}
                }
            )
        except Exception as e:
            print(f"Error sending email: {str(e)}")

def lambda_handler(event, context):
    """Lambda function for Security Training Management"""
    
    training_manager = SecurityTrainingManager()
    
    action = event.get('action')
    
    if action == 'create_training_plan':
        result = training_manager.create_personalized_training_plan(event['employee_id'])
    elif action == 'track_completion':
        result = training_manager.track_training_completion(event['completion_data'])
    elif action == 'conduct_assessment':
        result = training_manager.conduct_security_assessment(event['assessment_data'])
    elif action == 'generate_team_dashboard':
        result = training_manager.generate_team_security_dashboard(event['team_id'])
    elif action == 'schedule_reminders':
        result = training_manager.schedule_training_reminders(event['employee_id'])
    elif action == 'generate_culture_metrics':
        result = training_manager.generate_security_culture_metrics(event.get('organization_level', 'company'))
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```
### Example 3: Security ownership integration with development workflows

```yaml
# .github/workflows/security-ownership-integration.yml
name: Security Ownership Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 9 * * 1'  # Weekly security ownership check

env:
  SECURITY_OWNERSHIP_API: https://api.company.com/security-ownership
  TEAM_SECURITY_DASHBOARD: https://dashboard.company.com/security

jobs:
  security-ownership-check:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install requests boto3 pyyaml
    
    - name: Check security ownership assignments
      run: |
        python scripts/check-security-ownership.py
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    
    - name: Validate security champion involvement
      run: |
        python scripts/validate-champion-involvement.py
    
    - name: Generate security ownership report
      run: |
        python scripts/generate-ownership-report.py
    
    - name: Upload security ownership report
      uses: actions/upload-artifact@v3
      with:
        name: security-ownership-report
        path: reports/security-ownership-report.json

  security-training-compliance:
    runs-on: ubuntu-latest
    steps:
    - name: Check team training compliance
      run: |
        python scripts/check-training-compliance.py --team="${{ github.repository_owner }}"
    
    - name: Identify training gaps
      run: |
        python scripts/identify-training-gaps.py
    
    - name: Schedule training reminders
      if: github.event_name == 'schedule'
      run: |
        python scripts/schedule-training-reminders.py

  security-culture-metrics:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule'
    steps:
    - name: Collect security culture metrics
      run: |
        python scripts/collect-culture-metrics.py
    
    - name: Update security dashboard
      run: |
        python scripts/update-security-dashboard.py
    
    - name: Send weekly security report
      run: |
        python scripts/send-weekly-report.py
```

```python
# scripts/check-security-ownership.py
import json
import requests
import os
from typing import Dict, List, Any
import boto3

class SecurityOwnershipChecker:
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER')
        self.repo_name = os.environ.get('GITHUB_REPOSITORY', '').split('/')[-1]
        self.dynamodb = boto3.resource('dynamodb')
        
        # DynamoDB tables
        self.ownership_table = self.dynamodb.Table('SecurityOwnership')
        self.teams_table = self.dynamodb.Table('Teams')
        
        # Security ownership requirements
        self.ownership_requirements = {
            'security_champion_required': True,
            'security_reviewer_required': True,
            'security_training_compliance': 80,  # percentage
            'security_documentation_required': True,
            'incident_response_contact_required': True
        }
    
    def check_repository_security_ownership(self) -> Dict[str, Any]:
        """Check security ownership for the current repository"""
        
        ownership_check = {
            'repository': f"{self.repo_owner}/{self.repo_name}",
            'check_timestamp': datetime.utcnow().isoformat(),
            'ownership_status': 'compliant',
            'issues': [],
            'recommendations': [],
            'team_info': {},
            'security_contacts': {}
        }
        
        try:
            # Get repository team information
            team_info = self.get_repository_team_info()
            ownership_check['team_info'] = team_info
            
            # Check for security champion
            champion_check = self.check_security_champion(team_info)
            if not champion_check['has_champion']:
                ownership_check['issues'].append({
                    'type': 'missing_security_champion',
                    'severity': 'high',
                    'message': 'No security champion assigned to this repository',
                    'recommendation': 'Assign a trained security champion to the team'
                })
                ownership_check['ownership_status'] = 'non_compliant'
            else:
                ownership_check['security_contacts']['champion'] = champion_check['champion_info']
            
            # Check for security reviewer
            reviewer_check = self.check_security_reviewer(team_info)
            if not reviewer_check['has_reviewer']:
                ownership_check['issues'].append({
                    'type': 'missing_security_reviewer',
                    'severity': 'medium',
                    'message': 'No designated security reviewer for code changes',
                    'recommendation': 'Designate team members as security reviewers'
                })
            else:
                ownership_check['security_contacts']['reviewers'] = reviewer_check['reviewer_info']
            
            # Check training compliance
            training_check = self.check_team_training_compliance(team_info)
            if training_check['compliance_percentage'] < self.ownership_requirements['security_training_compliance']:
                ownership_check['issues'].append({
                    'type': 'low_training_compliance',
                    'severity': 'medium',
                    'message': f"Team training compliance ({training_check['compliance_percentage']}%) below required threshold ({self.ownership_requirements['security_training_compliance']}%)",
                    'recommendation': 'Complete required security training courses'
                })
            
            # Check security documentation
            docs_check = self.check_security_documentation()
            if not docs_check['has_security_docs']:
                ownership_check['issues'].append({
                    'type': 'missing_security_documentation',
                    'severity': 'low',
                    'message': 'Security documentation not found in repository',
                    'recommendation': 'Create SECURITY.md file with security practices and contacts'
                })
            
            # Check incident response contact
            incident_check = self.check_incident_response_contact(team_info)
            if not incident_check['has_contact']:
                ownership_check['issues'].append({
                    'type': 'missing_incident_contact',
                    'severity': 'high',
                    'message': 'No incident response contact defined',
                    'recommendation': 'Define incident response contact in team configuration'
                })
            else:
                ownership_check['security_contacts']['incident_response'] = incident_check['contact_info']
            
            # Generate overall recommendations
            ownership_check['recommendations'] = self.generate_ownership_recommendations(ownership_check)
            
            # Store ownership check results
            self.store_ownership_check_results(ownership_check)
            
            return ownership_check
            
        except Exception as e:
            ownership_check['error'] = str(e)
            ownership_check['ownership_status'] = 'error'
            return ownership_check
    
    def get_repository_team_info(self) -> Dict[str, Any]:
        """Get team information for the repository"""
        
        # Get repository collaborators
        headers = {'Authorization': f'token {self.github_token}'}
        
        # Get repository info
        repo_response = requests.get(
            f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}',
            headers=headers
        )
        
        if repo_response.status_code != 200:
            return {'error': 'Failed to get repository information'}
        
        repo_data = repo_response.json()
        
        # Get collaborators
        collaborators_response = requests.get(
            f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/collaborators',
            headers=headers
        )
        
        collaborators = []
        if collaborators_response.status_code == 200:
            collaborators = collaborators_response.json()
        
        # Get team assignments from DynamoDB
        team_assignments = self.get_team_assignments(f"{self.repo_owner}/{self.repo_name}")
        
        return {
            'repository_name': repo_data['name'],
            'repository_owner': repo_data['owner']['login'],
            'primary_language': repo_data.get('language'),
            'collaborators': [{'login': c['login'], 'permissions': c.get('permissions', {})} for c in collaborators],
            'team_assignments': team_assignments,
            'repository_topics': repo_data.get('topics', [])
        }
    
    def check_security_champion(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check if team has a designated security champion"""
        
        team_assignments = team_info.get('team_assignments', {})
        
        # Check for security champion in team assignments
        security_champion = team_assignments.get('security_champion')
        
        if security_champion:
            # Verify champion is still active and trained
            champion_status = self.verify_champion_status(security_champion['employee_id'])
            
            return {
                'has_champion': champion_status['active'],
                'champion_info': {
                    'name': security_champion['name'],
                    'email': security_champion['email'],
                    'employee_id': security_champion['employee_id'],
                    'certification_status': champion_status['certification_status'],
                    'last_training_date': champion_status['last_training_date']
                }
            }
        
        # Check if any collaborators are security champions
        for collaborator in team_info.get('collaborators', []):
            champion_status = self.check_if_user_is_champion(collaborator['login'])
            if champion_status['is_champion']:
                return {
                    'has_champion': True,
                    'champion_info': champion_status['champion_info']
                }
        
        return {
            'has_champion': False,
            'recommendation': 'Assign a security champion to this repository team'
        }
    
    def check_security_reviewer(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check if team has designated security reviewers"""
        
        team_assignments = team_info.get('team_assignments', {})
        security_reviewers = team_assignments.get('security_reviewers', [])
        
        if security_reviewers:
            # Verify reviewers are trained and active
            active_reviewers = []
            for reviewer in security_reviewers:
                reviewer_status = self.verify_reviewer_status(reviewer['employee_id'])
                if reviewer_status['qualified']:
                    active_reviewers.append({
                        'name': reviewer['name'],
                        'email': reviewer['email'],
                        'employee_id': reviewer['employee_id'],
                        'specializations': reviewer_status['specializations']
                    })
            
            return {
                'has_reviewer': len(active_reviewers) > 0,
                'reviewer_info': active_reviewers
            }
        
        return {
            'has_reviewer': False,
            'recommendation': 'Designate and train security reviewers for code changes'
        }
    
    def check_team_training_compliance(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check team security training compliance"""
        
        collaborators = team_info.get('collaborators', [])
        
        if not collaborators:
            return {
                'compliance_percentage': 0,
                'compliant_members': 0,
                'total_members': 0
            }
        
        compliant_members = 0
        total_members = len(collaborators)
        member_details = []
        
        for collaborator in collaborators:
            # Get training status for each team member
            training_status = self.get_member_training_status(collaborator['login'])
            
            member_details.append({
                'username': collaborator['login'],
                'training_compliant': training_status['compliant'],
                'completion_percentage': training_status['completion_percentage'],
                'overdue_courses': training_status['overdue_courses']
            })
            
            if training_status['compliant']:
                compliant_members += 1
        
        compliance_percentage = (compliant_members / total_members * 100) if total_members > 0 else 0
        
        return {
            'compliance_percentage': compliance_percentage,
            'compliant_members': compliant_members,
            'total_members': total_members,
            'member_details': member_details
        }
    
    def check_security_documentation(self) -> Dict[str, Any]:
        """Check if repository has security documentation"""
        
        headers = {'Authorization': f'token {self.github_token}'}
        
        # Check for SECURITY.md file
        security_files = ['SECURITY.md', 'docs/SECURITY.md', '.github/SECURITY.md', 'security/README.md']
        
        for file_path in security_files:
            response = requests.get(
                f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}',
                headers=headers
            )
            
            if response.status_code == 200:
                return {
                    'has_security_docs': True,
                    'security_file_path': file_path,
                    'last_updated': response.json().get('commit', {}).get('committer', {}).get('date')
                }
        
        return {
            'has_security_docs': False,
            'recommendation': 'Create SECURITY.md file with security practices and contact information'
        }
    
    def check_incident_response_contact(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check if team has incident response contact defined"""
        
        team_assignments = team_info.get('team_assignments', {})
        incident_contact = team_assignments.get('incident_response_contact')
        
        if incident_contact:
            return {
                'has_contact': True,
                'contact_info': {
                    'name': incident_contact['name'],
                    'email': incident_contact['email'],
                    'phone': incident_contact.get('phone'),
                    'escalation_path': incident_contact.get('escalation_path', [])
                }
            }
        
        return {
            'has_contact': False,
            'recommendation': 'Define incident response contact and escalation path'
        }
    
    def generate_ownership_recommendations(self, ownership_check: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on ownership check results"""
        
        recommendations = []
        
        # High priority recommendations
        high_priority_issues = [issue for issue in ownership_check['issues'] if issue['severity'] == 'high']
        if high_priority_issues:
            recommendations.append("URGENT: Address high-priority security ownership issues immediately")
            for issue in high_priority_issues:
                recommendations.append(f"• {issue['recommendation']}")
        
        # Medium priority recommendations
        medium_priority_issues = [issue for issue in ownership_check['issues'] if issue['severity'] == 'medium']
        if medium_priority_issues:
            recommendations.append("Address medium-priority security ownership issues within 2 weeks")
            for issue in medium_priority_issues:
                recommendations.append(f"• {issue['recommendation']}")
        
        # General recommendations
        if ownership_check['ownership_status'] == 'compliant':
            recommendations.append("✅ Security ownership is compliant - maintain current practices")
        else:
            recommendations.append("Establish comprehensive security ownership framework for this repository")
        
        # Training recommendations
        team_info = ownership_check.get('team_info', {})
        if team_info.get('collaborators'):
            recommendations.append("Schedule regular security training updates for all team members")
            recommendations.append("Consider implementing security champions program if not already in place")
        
        return recommendations
    
    def store_ownership_check_results(self, ownership_check: Dict[str, Any]):
        """Store ownership check results in DynamoDB"""
        
        try:
            self.ownership_table.put_item(Item={
                'repository': ownership_check['repository'],
                'check_timestamp': ownership_check['check_timestamp'],
                'ownership_status': ownership_check['ownership_status'],
                'issues_count': len(ownership_check['issues']),
                'issues': ownership_check['issues'],
                'recommendations': ownership_check['recommendations'],
                'team_info': ownership_check['team_info'],
                'security_contacts': ownership_check['security_contacts']
            })
        except Exception as e:
            print(f"Error storing ownership check results: {str(e)}")
    
    def get_team_assignments(self, repository: str) -> Dict[str, Any]:
        """Get team security assignments from DynamoDB"""
        
        try:
            response = self.teams_table.get_item(Key={'repository': repository})
            if 'Item' in response:
                return response['Item'].get('security_assignments', {})
        except Exception as e:
            print(f"Error getting team assignments: {str(e)}")
        
        return {}
    
    def verify_champion_status(self, employee_id: str) -> Dict[str, Any]:
        """Verify security champion status and training"""
        
        # This would integrate with the Security Champions Program system
        # For now, return mock data
        return {
            'active': True,
            'certification_status': 'current',
            'last_training_date': '2024-01-15T00:00:00Z'
        }
    
    def get_member_training_status(self, username: str) -> Dict[str, Any]:
        """Get training status for a team member"""
        
        # This would integrate with the Security Training Management system
        # For now, return mock data
        return {
            'compliant': True,
            'completion_percentage': 85,
            'overdue_courses': 0
        }

def main():
    """Main function to run security ownership check"""
    
    checker = SecurityOwnershipChecker()
    
    # Perform ownership check
    ownership_check = checker.check_repository_security_ownership()
    
    # Print results
    print("Security Ownership Check Results:")
    print("=" * 50)
    print(f"Repository: {ownership_check['repository']}")
    print(f"Status: {ownership_check['ownership_status']}")
    print(f"Issues Found: {len(ownership_check['issues'])}")
    
    if ownership_check['issues']:
        print("\nIssues:")
        for issue in ownership_check['issues']:
            print(f"  • [{issue['severity'].upper()}] {issue['message']}")
    
    if ownership_check['recommendations']:
        print("\nRecommendations:")
        for rec in ownership_check['recommendations']:
            print(f"  • {rec}")
    
    # Save detailed report
    os.makedirs('reports', exist_ok=True)
    with open('reports/security-ownership-report.json', 'w') as f:
        json.dump(ownership_check, f, indent=2)
    
    # Exit with appropriate code
    if ownership_check['ownership_status'] == 'compliant':
        print("\n✅ Security ownership check passed!")
        exit(0)
    else:
        print("\n❌ Security ownership check failed!")
        exit(1)

if __name__ == "__main__":
    main()
```
### Example 4: Security culture measurement and improvement framework

```python
import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any
import statistics

class SecurityCultureFramework:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        
        # DynamoDB tables
        self.culture_metrics_table = self.dynamodb.Table('SecurityCultureMetrics')
        self.feedback_table = self.dynamodb.Table('SecurityFeedback')
        self.initiatives_table = self.dynamodb.Table('SecurityInitiatives')
        self.surveys_table = self.dynamodb.Table('SecuritySurveys')
        
        # Culture measurement framework
        self.culture_dimensions = {
            'security_awareness': {
                'weight': 0.25,
                'indicators': [
                    'security_training_completion_rate',
                    'security_incident_reporting_rate',
                    'proactive_security_suggestions',
                    'security_tool_adoption_rate'
                ]
            },
            'security_ownership': {
                'weight': 0.30,
                'indicators': [
                    'security_champion_participation',
                    'security_code_review_coverage',
                    'security_testing_integration',
                    'security_documentation_quality'
                ]
            },
            'security_collaboration': {
                'weight': 0.20,
                'indicators': [
                    'cross_team_security_projects',
                    'security_knowledge_sharing',
                    'security_mentoring_activities',
                    'security_community_engagement'
                ]
            },
            'security_innovation': {
                'weight': 0.15,
                'indicators': [
                    'security_automation_initiatives',
                    'security_tool_development',
                    'security_process_improvements',
                    'security_research_contributions'
                ]
            },
            'security_resilience': {
                'weight': 0.10,
                'indicators': [
                    'incident_response_effectiveness',
                    'security_recovery_time',
                    'lessons_learned_implementation',
                    'security_preparedness_exercises'
                ]
            }
        }
    
    def measure_security_culture(self, organization_unit: str, period: str = 'quarterly') -> Dict[str, Any]:
        """Measure security culture across multiple dimensions"""
        
        measurement_id = str(uuid.uuid4())
        
        culture_measurement = {
            'measurement_id': measurement_id,
            'organization_unit': organization_unit,
            'measurement_period': period,
            'measurement_date': datetime.utcnow().isoformat(),
            'overall_culture_score': 0,
            'culture_grade': 'F',
            'dimension_scores': {},
            'trends': {},
            'strengths': [],
            'improvement_areas': [],
            'recommendations': [],
            'action_plan': {}
        }
        
        # Calculate date range for measurement
        end_date = datetime.utcnow()
        if period == 'quarterly':
            start_date = end_date - timedelta(days=90)
        elif period == 'monthly':
            start_date = end_date - timedelta(days=30)
        elif period == 'yearly':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=90)
        
        total_weighted_score = 0
        
        # Measure each culture dimension
        for dimension, config in self.culture_dimensions.items():
            dimension_score = self.measure_culture_dimension(
                organization_unit, dimension, config, start_date, end_date
            )
            
            culture_measurement['dimension_scores'][dimension] = dimension_score
            total_weighted_score += dimension_score['score'] * config['weight']
        
        # Calculate overall culture score
        culture_measurement['overall_culture_score'] = total_weighted_score
        culture_measurement['culture_grade'] = self.determine_culture_grade(total_weighted_score)
        
        # Analyze trends
        culture_measurement['trends'] = self.analyze_culture_trends(organization_unit, period)
        
        # Identify strengths and improvement areas
        culture_measurement['strengths'] = self.identify_culture_strengths(culture_measurement['dimension_scores'])
        culture_measurement['improvement_areas'] = self.identify_improvement_areas(culture_measurement['dimension_scores'])
        
        # Generate recommendations
        culture_measurement['recommendations'] = self.generate_culture_recommendations(culture_measurement)
        
        # Create action plan
        culture_measurement['action_plan'] = self.create_culture_action_plan(culture_measurement)
        
        # Store measurement results
        self.store_culture_measurement(culture_measurement)
        
        # Send culture report
        self.send_culture_report(culture_measurement)
        
        return culture_measurement
    
    def measure_culture_dimension(self, organization_unit: str, dimension: str, config: Dict[str, Any], 
                                start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Measure a specific culture dimension"""
        
        dimension_result = {
            'dimension': dimension,
            'score': 0,
            'max_score': 100,
            'indicator_scores': {},
            'data_sources': [],
            'measurement_confidence': 'high'
        }
        
        total_indicator_score = 0
        indicators_measured = 0
        
        # Measure each indicator in the dimension
        for indicator in config['indicators']:
            try:
                indicator_score = self.measure_culture_indicator(
                    organization_unit, indicator, start_date, end_date
                )
                
                dimension_result['indicator_scores'][indicator] = indicator_score
                total_indicator_score += indicator_score['score']
                indicators_measured += 1
                
                dimension_result['data_sources'].extend(indicator_score.get('data_sources', []))
                
            except Exception as e:
                print(f"Error measuring indicator {indicator}: {str(e)}")
                dimension_result['measurement_confidence'] = 'medium'
        
        # Calculate dimension score
        if indicators_measured > 0:
            dimension_result['score'] = total_indicator_score / indicators_measured
        
        return dimension_result
    
    def measure_culture_indicator(self, organization_unit: str, indicator: str, 
                                start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Measure a specific culture indicator"""
        
        indicator_result = {
            'indicator': indicator,
            'score': 0,
            'measurement_method': 'automated',
            'data_sources': [],
            'raw_data': {},
            'calculation_details': {}
        }
        
        # Define measurement methods for each indicator
        measurement_methods = {
            'security_training_completion_rate': self.measure_training_completion_rate,
            'security_incident_reporting_rate': self.measure_incident_reporting_rate,
            'proactive_security_suggestions': self.measure_proactive_suggestions,
            'security_tool_adoption_rate': self.measure_tool_adoption_rate,
            'security_champion_participation': self.measure_champion_participation,
            'security_code_review_coverage': self.measure_code_review_coverage,
            'security_testing_integration': self.measure_testing_integration,
            'security_documentation_quality': self.measure_documentation_quality,
            'cross_team_security_projects': self.measure_cross_team_projects,
            'security_knowledge_sharing': self.measure_knowledge_sharing,
            'security_mentoring_activities': self.measure_mentoring_activities,
            'security_community_engagement': self.measure_community_engagement,
            'security_automation_initiatives': self.measure_automation_initiatives,
            'security_tool_development': self.measure_tool_development,
            'security_process_improvements': self.measure_process_improvements,
            'security_research_contributions': self.measure_research_contributions,
            'incident_response_effectiveness': self.measure_incident_response_effectiveness,
            'security_recovery_time': self.measure_recovery_time,
            'lessons_learned_implementation': self.measure_lessons_learned,
            'security_preparedness_exercises': self.measure_preparedness_exercises
        }
        
        # Measure the indicator
        if indicator in measurement_methods:
            try:
                measurement_result = measurement_methods[indicator](
                    organization_unit, start_date, end_date
                )
                indicator_result.update(measurement_result)
            except Exception as e:
                print(f"Error measuring {indicator}: {str(e)}")
                indicator_result['score'] = 0
                indicator_result['error'] = str(e)
        
        return indicator_result
    
    def measure_training_completion_rate(self, organization_unit: str, 
                                       start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Measure security training completion rate"""
        
        # Get training data from training management system
        training_data = self.get_training_data(organization_unit, start_date, end_date)
        
        total_employees = training_data.get('total_employees', 0)
        completed_training = training_data.get('completed_training', 0)
        
        completion_rate = (completed_training / total_employees * 100) if total_employees > 0 else 0
        
        return {
            'score': min(completion_rate, 100),
            'raw_data': {
                'total_employees': total_employees,
                'completed_training': completed_training,
                'completion_rate': completion_rate
            },
            'data_sources': ['training_management_system'],
            'calculation_details': {
                'formula': 'completed_training / total_employees * 100',
                'target_threshold': 90
            }
        }
    
    def measure_incident_reporting_rate(self, organization_unit: str, 
                                      start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Measure proactive security incident reporting rate"""
        
        # Get incident data
        incident_data = self.get_incident_data(organization_unit, start_date, end_date)
        
        total_incidents = incident_data.get('total_incidents', 0)
        proactive_reports = incident_data.get('proactive_reports', 0)
        
        reporting_rate = (proactive_reports / total_incidents * 100) if total_incidents > 0 else 0
        
        # Also consider the absolute number of proactive reports
        proactive_score = min(proactive_reports * 10, 50)  # Up to 50 points for volume
        rate_score = min(reporting_rate, 50)  # Up to 50 points for rate
        
        total_score = proactive_score + rate_score
        
        return {
            'score': min(total_score, 100),
            'raw_data': {
                'total_incidents': total_incidents,
                'proactive_reports': proactive_reports,
                'reporting_rate': reporting_rate
            },
            'data_sources': ['incident_management_system'],
            'calculation_details': {
                'formula': 'proactive_reports_score + reporting_rate_score',
                'target_threshold': 80
            }
        }
    
    def measure_champion_participation(self, organization_unit: str, 
                                     start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Measure security champion participation and activity"""
        
        # Get champion data
        champion_data = self.get_champion_data(organization_unit, start_date, end_date)
        
        total_teams = champion_data.get('total_teams', 0)
        teams_with_champions = champion_data.get('teams_with_champions', 0)
        active_champions = champion_data.get('active_champions', 0)
        champion_activities = champion_data.get('champion_activities', 0)
        
        # Calculate participation metrics
        champion_coverage = (teams_with_champions / total_teams * 100) if total_teams > 0 else 0
        champion_activity_score = min(champion_activities * 2, 50)  # Up to 50 points for activities
        coverage_score = min(champion_coverage, 50)  # Up to 50 points for coverage
        
        total_score = champion_activity_score + coverage_score
        
        return {
            'score': min(total_score, 100),
            'raw_data': {
                'total_teams': total_teams,
                'teams_with_champions': teams_with_champions,
                'active_champions': active_champions,
                'champion_activities': champion_activities,
                'champion_coverage': champion_coverage
            },
            'data_sources': ['security_champions_system'],
            'calculation_details': {
                'formula': 'champion_activity_score + coverage_score',
                'target_threshold': 85
            }
        }
    
    def conduct_security_culture_survey(self, survey_config: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct security culture survey"""
        
        survey_id = str(uuid.uuid4())
        
        survey = {
            'survey_id': survey_id,
            'survey_name': survey_config['name'],
            'survey_type': survey_config.get('type', 'culture_assessment'),
            'target_audience': survey_config['target_audience'],
            'questions': survey_config['questions'],
            'launch_date': datetime.utcnow().isoformat(),
            'response_deadline': (datetime.utcnow() + timedelta(days=14)).isoformat(),
            'status': 'active',
            'responses': [],
            'response_rate': 0,
            'results': {}
        }
        
        # Store survey
        self.surveys_table.put_item(Item=survey)
        
        # Send survey invitations
        self.send_survey_invitations(survey)
        
        return {
            'survey_id': survey_id,
            'status': 'launched',
            'response_deadline': survey['response_deadline']
        }
    
    def analyze_survey_results(self, survey_id: str) -> Dict[str, Any]:
        """Analyze security culture survey results"""
        
        # Get survey data
        survey_response = self.surveys_table.get_item(Key={'survey_id': survey_id})
        
        if 'Item' not in survey_response:
            return {'error': 'Survey not found'}
        
        survey = survey_response['Item']
        responses = survey.get('responses', [])
        
        if not responses:
            return {'error': 'No survey responses available'}
        
        analysis = {
            'survey_id': survey_id,
            'survey_name': survey['survey_name'],
            'analysis_date': datetime.utcnow().isoformat(),
            'total_responses': len(responses),
            'response_rate': survey.get('response_rate', 0),
            'question_analysis': {},
            'demographic_breakdown': {},
            'sentiment_analysis': {},
            'key_insights': [],
            'recommendations': []
        }
        
        # Analyze each question
        for question in survey['questions']:
            question_id = question['question_id']
            question_responses = [r.get('answers', {}).get(question_id) for r in responses if question_id in r.get('answers', {})]
            
            if question['type'] == 'rating':
                # Analyze rating questions
                ratings = [int(r) for r in question_responses if r is not None]
                if ratings:
                    analysis['question_analysis'][question_id] = {
                        'question_text': question['text'],
                        'average_rating': statistics.mean(ratings),
                        'median_rating': statistics.median(ratings),
                        'rating_distribution': {str(i): ratings.count(i) for i in range(1, 6)},
                        'response_count': len(ratings)
                    }
            
            elif question['type'] == 'multiple_choice':
                # Analyze multiple choice questions
                choices = [r for r in question_responses if r is not None]
                if choices:
                    choice_counts = {}
                    for choice in choices:
                        choice_counts[choice] = choice_counts.get(choice, 0) + 1
                    
                    analysis['question_analysis'][question_id] = {
                        'question_text': question['text'],
                        'choice_distribution': choice_counts,
                        'most_common_choice': max(choice_counts, key=choice_counts.get),
                        'response_count': len(choices)
                    }
            
            elif question['type'] == 'text':
                # Analyze text responses
                text_responses = [r for r in question_responses if r is not None and r.strip()]
                analysis['question_analysis'][question_id] = {
                    'question_text': question['text'],
                    'response_count': len(text_responses),
                    'sample_responses': text_responses[:5]  # First 5 responses as samples
                }
        
        # Generate insights and recommendations
        analysis['key_insights'] = self.generate_survey_insights(analysis)
        analysis['recommendations'] = self.generate_survey_recommendations(analysis)
        
        # Update survey with results
        survey['results'] = analysis
        survey['status'] = 'completed'
        self.surveys_table.put_item(Item=survey)
        
        return analysis
    
    def create_culture_improvement_initiative(self, initiative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a security culture improvement initiative"""
        
        initiative_id = str(uuid.uuid4())
        
        initiative = {
            'initiative_id': initiative_id,
            'name': initiative_data['name'],
            'description': initiative_data['description'],
            'target_dimension': initiative_data['target_dimension'],
            'target_indicators': initiative_data.get('target_indicators', []),
            'owner': initiative_data['owner'],
            'stakeholders': initiative_data.get('stakeholders', []),
            'start_date': initiative_data['start_date'],
            'target_completion_date': initiative_data['target_completion_date'],
            'budget': initiative_data.get('budget', 0),
            'success_metrics': initiative_data['success_metrics'],
            'milestones': initiative_data.get('milestones', []),
            'status': 'planning',
            'progress': {
                'completion_percentage': 0,
                'milestones_completed': 0,
                'total_milestones': len(initiative_data.get('milestones', [])),
                'current_phase': 'planning'
            },
            'impact_assessment': {
                'baseline_metrics': {},
                'current_metrics': {},
                'target_metrics': initiative_data.get('target_metrics', {}),
                'roi_calculation': {}
            }
        }
        
        # Store initiative
        self.initiatives_table.put_item(Item=initiative)
        
        # Send initiative launch notification
        self.send_initiative_notification(initiative)
        
        return {
            'initiative_id': initiative_id,
            'status': 'created',
            'next_steps': 'Initiative planning phase initiated'
        }
    
    def track_initiative_progress(self, initiative_id: str, progress_update: Dict[str, Any]) -> Dict[str, Any]:
        """Track progress of a security culture improvement initiative"""
        
        # Get initiative
        initiative_response = self.initiatives_table.get_item(Key={'initiative_id': initiative_id})
        
        if 'Item' not in initiative_response:
            return {'error': 'Initiative not found'}
        
        initiative = initiative_response['Item']
        
        # Update progress
        initiative['progress'].update(progress_update.get('progress', {}))
        initiative['status'] = progress_update.get('status', initiative['status'])
        
        # Update impact metrics
        if 'current_metrics' in progress_update:
            initiative['impact_assessment']['current_metrics'].update(progress_update['current_metrics'])
        
        # Add progress entry
        if 'progress_entries' not in initiative:
            initiative['progress_entries'] = []
        
        initiative['progress_entries'].append({
            'date': datetime.utcnow().isoformat(),
            'update': progress_update.get('description', ''),
            'metrics': progress_update.get('current_metrics', {}),
            'updated_by': progress_update.get('updated_by', 'system')
        })
        
        # Calculate ROI if enough data is available
        if initiative['impact_assessment']['baseline_metrics'] and initiative['impact_assessment']['current_metrics']:
            initiative['impact_assessment']['roi_calculation'] = self.calculate_initiative_roi(initiative)
        
        # Update initiative
        self.initiatives_table.put_item(Item=initiative)
        
        # Send progress notification
        self.send_progress_notification(initiative, progress_update)
        
        return {
            'initiative_id': initiative_id,
            'status': initiative['status'],
            'completion_percentage': initiative['progress']['completion_percentage'],
            'roi': initiative['impact_assessment']['roi_calculation'].get('roi_percentage', 'N/A')
        }
    
    def generate_culture_dashboard(self, organization_unit: str) -> Dict[str, Any]:
        """Generate comprehensive security culture dashboard"""
        
        dashboard = {
            'organization_unit': organization_unit,
            'generated_date': datetime.utcnow().isoformat(),
            'dashboard_type': 'security_culture_overview',
            'current_culture_score': 0,
            'culture_grade': 'F',
            'trend_direction': 'stable',
            'dimension_scores': {},
            'key_metrics': {},
            'active_initiatives': [],
            'recent_achievements': [],
            'upcoming_milestones': [],
            'recommendations': []
        }
        
        # Get latest culture measurement
        latest_measurement = self.get_latest_culture_measurement(organization_unit)
        
        if latest_measurement:
            dashboard['current_culture_score'] = latest_measurement['overall_culture_score']
            dashboard['culture_grade'] = latest_measurement['culture_grade']
            dashboard['dimension_scores'] = latest_measurement['dimension_scores']
            dashboard['trend_direction'] = self.calculate_trend_direction(organization_unit)
        
        # Get key metrics
        dashboard['key_metrics'] = self.get_key_culture_metrics(organization_unit)
        
        # Get active initiatives
        dashboard['active_initiatives'] = self.get_active_initiatives(organization_unit)
        
        # Get recent achievements
        dashboard['recent_achievements'] = self.get_recent_achievements(organization_unit)
        
        # Get upcoming milestones
        dashboard['upcoming_milestones'] = self.get_upcoming_milestones(organization_unit)
        
        # Generate recommendations
        dashboard['recommendations'] = self.generate_dashboard_recommendations(dashboard)
        
        return dashboard

def lambda_handler(event, context):
    """Lambda function for Security Culture Framework"""
    
    culture_framework = SecurityCultureFramework()
    
    action = event.get('action')
    
    if action == 'measure_culture':
        result = culture_framework.measure_security_culture(
            event['organization_unit'], 
            event.get('period', 'quarterly')
        )
    elif action == 'conduct_survey':
        result = culture_framework.conduct_security_culture_survey(event['survey_config'])
    elif action == 'analyze_survey':
        result = culture_framework.analyze_survey_results(event['survey_id'])
    elif action == 'create_initiative':
        result = culture_framework.create_culture_improvement_initiative(event['initiative_data'])
    elif action == 'track_progress':
        result = culture_framework.track_initiative_progress(event['initiative_id'], event['progress_update'])
    elif action == 'generate_dashboard':
        result = culture_framework.generate_culture_dashboard(event['organization_unit'])
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>NoSQL database service for storing security champion data, training records, competency assessments, and culture metrics.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Serverless compute service for running security ownership management functions, training tracking, and culture measurement automation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SES</h4>
    <p>Email service for sending training notifications, security champion communications, and culture survey invitations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SNS</h4>
    <p>Messaging service for sending alerts about security ownership issues, training compliance, and culture metric thresholds.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitoring service for tracking security culture metrics, training completion rates, and security ownership KPIs.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Step Functions</h4>
    <p>Workflow orchestration service for managing complex security training workflows and culture improvement initiatives.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage service for storing training materials, security documentation, and culture assessment reports.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Management service for maintaining security ownership configurations and automating security culture processes.</p>
  </div>
</div>

## Benefits of building a program that embeds security ownership in workload teams

- **Distributed security responsibility**: Creates multiple layers of security ownership throughout the organization
- **Improved security awareness**: Increases security knowledge and consciousness across all team members
- **Faster security response**: Enables quicker identification and resolution of security issues
- **Enhanced security culture**: Fosters a culture where security is everyone's responsibility
- **Reduced security debt**: Prevents security issues through proactive ownership and accountability
- **Better security outcomes**: Improves overall security posture through embedded expertise
- **Increased team autonomy**: Empowers teams to make security decisions independently
- **Sustainable security practices**: Creates long-term security capabilities within teams

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_appsec_build_program_that_embeds_security_ownership_in_teams.html">AWS Well-Architected Framework - Build a program that embeds security ownership in workload teams</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-build-a-security-champions-program/">How to build a security champions program</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/building-a-security-culture-in-your-organization/">Building a security culture in your organization</a></li>
    <li><a href="https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/security-ou-and-account-design.html">Organizing Your AWS Environment Using Multiple Accounts</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-a-culture-of-security-in-your-organization/">How to create a culture of security in your organization</a></li>
    <li><a href="https://docs.aws.amazon.com/security/latest/userguide/security-learning.html">AWS Security Learning Resources</a></li>
  </ul>
</div>
