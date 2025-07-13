#!/usr/bin/env python3
"""
ERPset Phase 1 Database Seed Data Script

This script populates the database with initial data including:
- Sample users
- Salesforce function definitions
- Knowledge base categories and tags
- Sample projects

Usage:
    python scripts/seed-data.py
    python scripts/seed-data.py --environment production
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List
from uuid import uuid4

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import asyncpg
    from argon2 import PasswordHasher
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Install with: pip install asyncpg argon2-cffi")
    sys.exit(1)


class DatabaseSeeder:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.ph = PasswordHasher()
        
    async def connect(self):
        """Establish database connection"""
        try:
            self.conn = await asyncpg.connect(self.database_url)
            print("✅ Connected to database")
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            sys.exit(1)
    
    async def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            await self.conn.close()
            print("✅ Database connection closed")
    
    async def create_users(self):
        """Create sample users"""
        print("📝 Creating sample users...")
        
        users = [
            {
                'id': str(uuid4()),
                'email': 'admin@erpset.com',
                'password': 'admin123',
                'name': 'System Administrator',
                'role': 'admin'
            },
            {
                'id': str(uuid4()),
                'email': 'consultant@erpset.com',
                'password': 'consultant123',
                'name': 'Senior Consultant',
                'role': 'consultant'
            },
            {
                'id': str(uuid4()),
                'email': 'viewer@erpset.com',
                'password': 'viewer123',
                'name': 'Project Viewer',
                'role': 'viewer'
            }
        ]
        
        for user in users:
            # Hash password
            password_hash = self.ph.hash(user['password'])
            
            await self.conn.execute("""
                INSERT INTO users (id, email, password_hash, name, role, is_active, email_verified)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (email) DO NOTHING
            """, user['id'], user['email'], password_hash, user['name'], 
                user['role'], True, True)
        
        print(f"✅ Created {len(users)} sample users")
    
    async def create_knowledge_tags(self):
        """Create knowledge base tags"""
        print("🏷️ Creating knowledge tags...")
        
        tags = [
            {'name': 'standard', 'description': 'Standard Salesforce functionality', 'color': '#22C55E'},
            {'name': 'custom', 'description': 'Customizable features', 'color': '#3B82F6'},
            {'name': 'advanced', 'description': 'Advanced configuration required', 'color': '#F59E0B'},
            {'name': 'integration', 'description': 'External system integration', 'color': '#8B5CF6'},
            {'name': 'automation', 'description': 'Workflow and process automation', 'color': '#EF4444'},
            {'name': 'reporting', 'description': 'Analytics and reporting features', 'color': '#06B6D4'},
            {'name': 'security', 'description': 'Security and access control', 'color': '#84CC16'},
            {'name': 'mobile', 'description': 'Mobile app functionality', 'color': '#F97316'},
            {'name': 'ai', 'description': 'AI and machine learning features', 'color': '#EC4899'},
            {'name': 'configuration', 'description': 'Basic setup and configuration', 'color': '#6B7280'}
        ]
        
        for tag in tags:
            await self.conn.execute("""
                INSERT INTO knowledge_tags (id, name, description, color)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (name) DO NOTHING
            """, str(uuid4()), tag['name'], tag['description'], tag['color'])
        
        print(f"✅ Created {len(tags)} knowledge tags")
    
    async def create_function_categories(self):
        """Create Salesforce function categories"""
        print("📂 Creating function categories...")
        
        categories = [
            {
                'id': str(uuid4()),
                'name': 'Lead Management',
                'description': 'Lead capture, qualification, and conversion processes',
                'module': 'sales',
                'parent_id': None,
                'sort_order': 1,
                'icon': 'users',
                'color': '#22C55E'
            },
            {
                'id': str(uuid4()),
                'name': 'Opportunity Management',
                'description': 'Sales opportunity tracking and pipeline management',
                'module': 'sales',
                'parent_id': None,
                'sort_order': 2,
                'icon': 'trending-up',
                'color': '#3B82F6'
            },
            {
                'id': str(uuid4()),
                'name': 'Account Management',
                'description': 'Customer account and relationship management',
                'module': 'sales',
                'parent_id': None,
                'sort_order': 3,
                'icon': 'building',
                'color': '#F59E0B'
            },
            {
                'id': str(uuid4()),
                'name': 'Contact Management',
                'description': 'Contact information and relationship tracking',
                'module': 'sales',
                'parent_id': None,
                'sort_order': 4,
                'icon': 'user',
                'color': '#8B5CF6'
            },
            {
                'id': str(uuid4()),
                'name': 'Sales Analytics',
                'description': 'Reporting and analytics for sales performance',
                'module': 'sales',
                'parent_id': None,
                'sort_order': 5,
                'icon': 'bar-chart',
                'color': '#06B6D4'
            }
        ]
        
        for category in categories:
            await self.conn.execute("""
                INSERT INTO function_categories (id, name, description, module, parent_id, sort_order, icon, color)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT DO NOTHING
            """, category['id'], category['name'], category['description'], 
                category['module'], category['parent_id'], category['sort_order'],
                category['icon'], category['color'])
        
        print(f"✅ Created {len(categories)} function categories")
        return categories
    
    async def create_salesforce_functions(self, categories: List[Dict]):
        """Create Salesforce function definitions"""
        print("⚙️ Creating Salesforce functions...")
        
        functions = [
            {
                'name': 'Lead Capture Forms',
                'description': 'Web-to-Lead forms and lead capture mechanisms',
                'module': 'sales',
                'function_type': 'lead_management',
                'configuration_template': {
                    'web_to_lead': {
                        'enabled': True,
                        'fields': ['FirstName', 'LastName', 'Email', 'Company', 'Phone'],
                        'required_fields': ['LastName', 'Email', 'Company'],
                        'redirect_url': '',
                        'auto_response': True
                    },
                    'lead_sources': ['Web', 'Phone', 'Email', 'Partner', 'Advertisement']
                },
                'hearing_template': [
                    {
                        'question': 'What lead sources do you want to track?',
                        'answer_type': 'multiselect',
                        'answer_options': ['Web', 'Phone', 'Email', 'Partner', 'Advertisement', 'Trade Show', 'Direct Mail'],
                        'is_required': True,
                        'category': 'Lead Sources'
                    },
                    {
                        'question': 'Which fields are required on your lead capture forms?',
                        'answer_type': 'multiselect',
                        'answer_options': ['FirstName', 'LastName', 'Email', 'Company', 'Phone', 'Title', 'Industry'],
                        'is_required': True,
                        'category': 'Form Configuration'
                    }
                ],
                'complexity_score': 3,
                'implementation_effort_hours': 8
            },
            {
                'name': 'Lead Assignment Rules',
                'description': 'Automatic lead assignment based on criteria',
                'module': 'sales',
                'function_type': 'lead_management',
                'configuration_template': {
                    'assignment_rules': {
                        'enabled': True,
                        'criteria': [],
                        'default_owner': '',
                        'notification': True
                    }
                },
                'hearing_template': [
                    {
                        'question': 'How should leads be assigned to sales representatives?',
                        'answer_type': 'select',
                        'answer_options': ['Geographic Territory', 'Industry', 'Company Size', 'Round Robin', 'Manual'],
                        'is_required': True,
                        'category': 'Assignment Logic'
                    },
                    {
                        'question': 'Should leads be automatically assigned or require manual review?',
                        'answer_type': 'select',
                        'answer_options': ['Automatic', 'Manual Review', 'Hybrid'],
                        'is_required': True,
                        'category': 'Assignment Process'
                    }
                ],
                'complexity_score': 6,
                'implementation_effort_hours': 16
            },
            {
                'name': 'Opportunity Stages',
                'description': 'Sales process stages and probability mapping',
                'module': 'sales',
                'function_type': 'opportunity_management',
                'configuration_template': {
                    'stages': [
                        {'name': 'Qualification', 'probability': 10, 'sort_order': 1},
                        {'name': 'Needs Analysis', 'probability': 25, 'sort_order': 2},
                        {'name': 'Proposal', 'probability': 50, 'sort_order': 3},
                        {'name': 'Negotiation', 'probability': 75, 'sort_order': 4},
                        {'name': 'Closed Won', 'probability': 100, 'sort_order': 5}
                    ]
                },
                'hearing_template': [
                    {
                        'question': 'What stages do you use in your sales process?',
                        'answer_type': 'text',
                        'is_required': True,
                        'category': 'Sales Process',
                        'help_text': 'List your sales stages in order (e.g., Qualification, Demo, Proposal, Negotiation, Closed Won)'
                    },
                    {
                        'question': 'What probability percentage should be assigned to each stage?',
                        'answer_type': 'text',
                        'is_required': True,
                        'category': 'Stage Configuration',
                        'help_text': 'Specify the likelihood of closing at each stage (0-100%)'
                    }
                ],
                'complexity_score': 4,
                'implementation_effort_hours': 12
            },
            {
                'name': 'Account Hierarchies',
                'description': 'Parent-child account relationships and management',
                'module': 'sales',
                'function_type': 'account_management',
                'configuration_template': {
                    'hierarchy': {
                        'enabled': True,
                        'max_levels': 3,
                        'inheritance_rules': []
                    }
                },
                'hearing_template': [
                    {
                        'question': 'Do you need to track parent-child relationships between accounts?',
                        'answer_type': 'boolean',
                        'is_required': True,
                        'category': 'Account Structure'
                    },
                    {
                        'question': 'What is the maximum number of hierarchy levels you need?',
                        'answer_type': 'number',
                        'is_required': False,
                        'category': 'Hierarchy Configuration'
                    }
                ],
                'complexity_score': 5,
                'implementation_effort_hours': 20
            },
            {
                'name': 'Contact Roles',
                'description': 'Contact roles and relationship tracking on opportunities',
                'module': 'sales',
                'function_type': 'contact_management',
                'configuration_template': {
                    'contact_roles': ['Decision Maker', 'Influencer', 'End User', 'Technical Evaluator', 'Economic Buyer']
                },
                'hearing_template': [
                    {
                        'question': 'What contact roles do you track on opportunities?',
                        'answer_type': 'multiselect',
                        'answer_options': ['Decision Maker', 'Influencer', 'End User', 'Technical Evaluator', 'Economic Buyer', 'Champion'],
                        'is_required': True,
                        'category': 'Contact Roles'
                    }
                ],
                'complexity_score': 3,
                'implementation_effort_hours': 6
            }
        ]
        
        for func in functions:
            func_id = str(uuid4())
            await self.conn.execute("""
                INSERT INTO salesforce_functions (
                    id, name, description, module, function_type, 
                    configuration_template, hearing_template, 
                    complexity_score, implementation_effort_hours, 
                    is_active, is_standard
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT DO NOTHING
            """, func_id, func['name'], func['description'], func['module'],
                func['function_type'], json.dumps(func['configuration_template']),
                json.dumps(func['hearing_template']), func['complexity_score'],
                func['implementation_effort_hours'], True, True)
        
        print(f"✅ Created {len(functions)} Salesforce functions")
    
    async def create_sample_projects(self):
        """Create sample projects for testing"""
        print("📁 Creating sample projects...")
        
        # Get admin user ID
        admin_user = await self.conn.fetchrow("SELECT id FROM users WHERE email = 'admin@erpset.com'")
        consultant_user = await self.conn.fetchrow("SELECT id FROM users WHERE email = 'consultant@erpset.com'")
        
        if not admin_user or not consultant_user:
            print("⚠️ Sample users not found, skipping project creation")
            return
        
        projects = [
            {
                'id': str(uuid4()),
                'name': 'ABC Manufacturing Salesforce Implementation',
                'description': 'Lead and opportunity management for manufacturing company',
                'erp_type': 'salesforce',
                'business_domain': 'sales',
                'scope': {
                    'lead_management': True,
                    'opportunity_management': True,
                    'account_management': False,
                    'contact_management': True,
                    'custom_objects': [],
                    'integration_requirements': ['ERP System', 'Marketing Automation']
                },
                'status': 'active',
                'owner_id': admin_user['id'],
                'client_name': 'ABC Manufacturing Inc.',
                'start_date': '2025-07-01',
                'target_go_live': '2025-10-01'
            },
            {
                'id': str(uuid4()),
                'name': 'XYZ Services Sales Cloud Setup',
                'description': 'Complete sales process automation for service company',
                'erp_type': 'salesforce',
                'business_domain': 'sales',
                'scope': {
                    'lead_management': True,
                    'opportunity_management': True,
                    'account_management': True,
                    'contact_management': True,
                    'custom_objects': ['Service Contract', 'Project'],
                    'integration_requirements': ['Billing System']
                },
                'status': 'active',
                'owner_id': consultant_user['id'],
                'client_name': 'XYZ Professional Services',
                'start_date': '2025-08-01',
                'target_go_live': '2025-11-15'
            }
        ]
        
        for project in projects:
            await self.conn.execute("""
                INSERT INTO projects (
                    id, name, description, erp_type, business_domain, 
                    scope, status, owner_id, client_name, start_date, target_go_live
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT DO NOTHING
            """, project['id'], project['name'], project['description'],
                project['erp_type'], project['business_domain'],
                json.dumps(project['scope']), project['status'],
                project['owner_id'], project['client_name'],
                project['start_date'], project['target_go_live'])
        
        print(f"✅ Created {len(projects)} sample projects")

    async def seed_all(self):
        """Run all seeding operations"""
        print("🌱 Starting database seeding process...")
        
        await self.create_users()
        await self.create_knowledge_tags()
        categories = await self.create_function_categories()
        await self.create_salesforce_functions(categories)
        await self.create_sample_projects()
        
        print("🎉 Database seeding completed successfully!")


async def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed ERPset database with initial data')
    parser.add_argument('--environment', choices=['development', 'staging', 'production'],
                        default='development', help='Environment to seed')
    parser.add_argument('--database-url', help='Database URL (overrides environment)')
    
    args = parser.parse_args()
    
    # Determine database URL
    if args.database_url:
        database_url = args.database_url
    else:
        # Load from environment or use defaults
        if args.environment == 'development':
            database_url = os.getenv('DATABASE_URL', 
                'postgresql://erpset_user:erpset_password@localhost:5432/erpset_dev')
        elif args.environment == 'staging':
            database_url = os.getenv('STAGING_DATABASE_URL')
        else:  # production
            database_url = os.getenv('PRODUCTION_DATABASE_URL')
    
    if not database_url:
        print(f"❌ No database URL configured for environment: {args.environment}")
        sys.exit(1)
    
    print(f"🎯 Seeding database for environment: {args.environment}")
    
    # Confirm for production
    if args.environment == 'production':
        confirm = input("⚠️ You are about to seed PRODUCTION database. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Seeding cancelled")
            sys.exit(1)
    
    # Run seeding
    seeder = DatabaseSeeder(database_url)
    try:
        await seeder.connect()
        await seeder.seed_all()
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        sys.exit(1)
    finally:
        await seeder.close()


if __name__ == '__main__':
    asyncio.run(main())