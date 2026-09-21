# Ad_On — Classified Ads & Marketplace Platform

Ad_On is a full-stack web platform built with Python and Django that connects users who want to buy, sell, or exchange goods and services.

The platform provides a complete classified-advertising experience where users can create and manage listings, discover products through search and filtering, communicate with other users through an integrated messaging system, and negotiate directly with sellers.

The project focuses on combining usability, communication, and secure content management within a centralized marketplace platform.

## Overview

Traditional classified-ad platforms can become difficult to navigate when users have limited search capabilities, poor communication tools, or little control over their publications.

Ad_On addresses these needs by providing a structured platform where users can:

- Create and manage their own advertisements
- Browse advertisements published by other users
- Search using keywords
- Filter and sort available listings
- Upload multiple images for an advertisement
- Specify prices, categories, descriptions, and locations
- Contact sellers through internal messaging
- Ask questions and negotiate prices
- Manage their personal profile and publication history

The platform also includes administrative functionality for managing users and moderating platform content.

## Main Features

### User Management

Users can create an account and access a personal profile.

The platform supports:

- User registration
- Secure login
- Personal profiles
- Modification of personal information
- Access to publication history
- User permissions and access control

An account is required for users who want to publish advertisements or interact with sellers through the platform.

### Advertisement Management

Authenticated users can create and manage their own advertisements.

Each advertisement can contain:

- Title
- Description
- Category
- Price
- Location
- One or multiple images
- Publication information

Users can:

- Create advertisements
- View advertisements
- Modify their publications
- Delete advertisements
- Manage their published content
- Define publication duration
- Renew publications

This provides the core CRUD functionality of the platform.

### Search and Navigation

The platform provides search and navigation tools to help users find relevant advertisements efficiently.

Users can:

- Search using keywords
- Apply advanced filters
- Sort search results
- Browse advertisements by relevant criteria

This reduces the need to manually browse through every available listing.

### Internal Messaging

Ad_On includes an integrated messaging system that allows users to communicate directly.

Buyers can contact sellers to:

- Ask questions about an advertisement
- Request additional information
- Discuss product details
- Negotiate prices
- Communicate before completing a transaction

The platform also supports notifications for new messages.

### Questions and Answers

Communication is not limited to direct negotiation.

Users can ask questions related to advertisements, allowing sellers to provide additional information about their products or services.

This creates a more interactive experience around individual listings.

### Administration and Moderation

The platform includes an administration area designed to help manage the application and maintain a secure environment.

Administrative functionality includes:

- User management
- Permission management
- Advertisement moderation
- Content supervision

This helps maintain the reliability and security of the platform.

## User Workflow

The main user journey can be summarized as:

Visitor
→ Browse Advertisements
→ Create an Account
→ View Advertisement
→ Contact Seller
→ Ask Questions / Negotiate
→ Complete Transaction

For sellers:

Create Account
→ Create Advertisement
→ Add Details and Images
→ Publish
→ Manage Advertisement
→ Communicate With Buyers
→ Negotiate

## Application Architecture

The application follows Django's Model-View-Template (MVT) architecture.

The main components are:

- Models — Define the application's entities and database structure.
- Views — Handle application logic and user requests.
- Templates — Provide the web interface.
- URLs — Route requests to the appropriate views.
- Forms — Handle user input and data validation.
- Database — Stores users, advertisements, messages, and related information.
- Administration — Provides management and moderation capabilities.

The general architecture can be represented as:

User
→ Web Interface
→ Django URL Routing
→ Views
→ Models
→ Database
→ Response
→ Web Interface

## Core Entities

The platform revolves around several important concepts:

### Users

Represent registered members of the platform and their profiles.

### Advertisements

Represent the products or services published by users.

Advertisements contain information such as title, description, category, price, location, images, and publication information.

### Categories

Organize advertisements according to the type of product or service being offered.

### Messages

Allow users to communicate directly regarding advertisements.

### Images

Allow advertisements to contain multiple images, providing users with a more complete view of the published item.

## Technology Stack

- Python
- Django
- HTML
- CSS
- JavaScript
- Django Templates
- Relational Database
- Django Authentication
- Django Admin

## Functional Requirements

The platform was designed around the following functional requirements.

### User Management

- Registration and authentication
- Personal profile
- Profile modification
- Publication history
- Permission management

### Advertisement Management

- Create advertisements
- Edit advertisements
- Delete advertisements
- Publish advertisements
- Upload multiple images
- Define price and location
- Select categories
- Manage publication duration
- Renew publications

### Search and Discovery

- Keyword search
- Advanced filtering
- Result sorting
- Advertisement browsing

### Communication

- Internal messaging
- Message notifications
- Questions and answers
- Price negotiation

### Administration

- User management
- Content moderation
- Permission management
- Platform supervision

## Non-Functional Requirements

The project also considers several quality requirements.

### Performance

The platform is designed to provide responsive navigation and efficient search and advertisement loading.

### Security

Security considerations include:

- User authentication
- Access control
- User permissions
- Administrative privileges

### Accessibility and Usability

The interface is designed to remain simple and intuitive while supporting different screen sizes through responsive design.

## Project Structure

    Ad_On/
    │
    └── plateforme_petites_annonces_project/
        │
        ├── manage.py
        ├── ...
        │
        └── ...

The Django project contains the application configuration, backend logic, templates, static resources, database-related components, and other resources required to run the platform.

## Getting Started

### Prerequisites

Make sure the following are installed:

- Python
- pip
- Git

A Python virtual environment is recommended.

### Installation

Clone the repository and navigate to the Django project:

    git clone https://github.com/Bouchra20252/Ad_On.git

    cd Ad_On/plateforme_petites_annonces_project

Create a virtual environment:

    python -m venv .venv

Activate it on Windows:

    .venv\Scripts\activate

Install the project dependencies:

    pip install -r requirements.txt

### Database Setup

Apply the Django migrations:

    python manage.py migrate

### Run the Application

Start the Django development server:

    python manage.py runserver

The application can then be accessed through the local Django development server.

## Development Objectives

This project was developed to gain practical experience with:

- Python programming
- Django web development
- Full-stack application development
- MVT architecture
- CRUD operations
- Database-driven applications
- User authentication
- Authorization and permissions
- Search and filtering
- Form handling
- File and image management
- Messaging systems
- Administrative management
- Responsive web interfaces

## Future Improvements

Possible extensions to the platform include:

- Online payment integration
- Advanced recommendation system
- Real-time messaging using WebSockets
- Email notifications
- User ratings and reviews
- Seller reputation system
- Favorites and saved advertisements
- Location-based search
- Advertisement analytics
- REST API
- Mobile application
- Production deployment and cloud hosting

## Screenshots

Screenshots of the main application interfaces can be added here.

Recommended screenshots include:

- Home page
- Advertisement browsing page
- Search and filtering interface
- Advertisement details
- Create advertisement form
- User profile
- Messaging interface
- Administration interface

## Project Context

Ad_On was developed as a practical full-stack web development project focused on building a complete classified-advertising and marketplace experience.

The project combines backend development, database management, authentication, CRUD operations, search and filtering, communication between users, and administrative moderation within a single Django application.

## Author

**Simali Bouchra**

AI & Data Engineering Student

Morocco
