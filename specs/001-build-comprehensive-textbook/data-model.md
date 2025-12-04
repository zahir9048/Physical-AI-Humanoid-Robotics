# Data Model: Physical AI & Humanoid Robotics Textbook

This document outlines the key entities and their attributes for the Physical AI & Humanoid Robotics Textbook.

## Entities

### Textbook
- **Description**: The primary educational resource, containing structured content.
- **Attributes**:
    - `Title`: String
    - `Description`: String
    - `Learning Outcomes`: List of Strings
    - `Structure`: Object (Modules, Weeks, Chapters)
    - `Assessments`: List of Assessment IDs
- **Relationships**:
    - Contains multiple Modules.
    - Contains multiple Assessments.

### Module
- **Description**: A major thematic section of the textbook.
- **Attributes**:
    - `Title`: String
    - `Focus`: String
    - `Weekly Breakdown`: List of Week IDs
    - `Projects`: List of Project descriptions/IDs
- **Relationships**:
    - Belongs to a Textbook.
    - Contains multiple Weeks.

### Week
- **Description**: A granular time-based section within a module.
- **Attributes**:
    - `Topics`: List of Strings
    - `Learning Objectives`: List of Strings
- **Relationships**:
    - Belongs to a Module.
    - Contains multiple Chapter/Sections.

### Chapter/Section
- **Description**: The core content unit.
- **Attributes**:
    - `Title`: String
    - `Content`: Markdown/MDX (text, code examples, diagrams)
    - `Practical Exercises`: List of Strings
    - `Learning Objectives`: List of Strings
- **Relationships**:
    - Belongs to a Week.

### Hardware Configuration
- **Description**: Detailed specifications for different computational loads and tiers.
- **Attributes**:
    - `Tier Name`: String (e.g., "Digital Twin" Workstation, "Physical AI" Edge Kit, "Robot Lab")
    - `Components`: Object (GPU, CPU, RAM, OS, Brain, Eyes, Balance, Voice, etc.)
    - `Rationale`: String
    - `Pricing`: String (e.g., "~$1.50/hour", "~$1,800-$3,000")
    - `Alternatives`: List of Strings
    - `Cloud/On-Premise options`: String
- **Relationships**:
    - Referenced by Textbook.

### Assessment
- **Description**: Evaluation mechanism for student understanding.
- **Attributes**:
    - `Type`: String (e.g., "project")
    - `Description`: String
    - `Learning outcomes assessed`: List of Strings
- **Relationships**:
    - Belongs to a Textbook.
