# 3-Tier Rule Engine Application

This application is a simple 3-tier rule engine that determines user eligibility based on attributes like age, department, income, spend, etc. It uses Abstract Syntax Trees (AST) to represent conditional rules and allows for dynamic creation, combination, and modification of these rules.

## Architecture

The application is divided into three tiers:

1. Simple UI
2. API and Backend
3. Data Storage

1. Presentation Layer (UI)
   - Web-based interface built with React
   - Allows users to create, view, and manage rules
   - Provides interface for rule evaluation

2. Application Layer (API and Backend)
   - RESTful API built with Flask
   - Handles rule processing, combination, and evaluation
   - Implements core business logic

3. Data Layer
   - Stores rules and application metadata
   - Utilizes PostgreSQL for persistent storage

Data Structure

The rule engine uses a tree-like data structure to represent the Abstract Syntax Tree (AST). Each node in the tree is defined as follows:

```python
class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # "operator" for AND/OR, "operand" for conditions
        self.left = left  # Reference to left child
        self.right = right  # Reference to right child (for operators)
        self.value = value  # Optional value for operand nodes





