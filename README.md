# Project Helper: Software Requirements Specification (SRS) Overview

## Introduction

The Project Helper is a comprehensive tool designed to facilitate learning and skill development by generating tailored project ideas based on user input. This README provides an overview of the system architecture as outlined in the Software Requirements Specification (SRS) document and includes a visual representation through a class diagram.

## Software Overview

- **Version**: 1.0 approved
- **Preparation Date**: 02-29-2024
- **Authors**: Zachary Freeman, Aide Cuevas, Donavan Drouin

The Project Helper aims to bridge the gap between the desire to learn new skills and finding practical applications for those skills. It supports continuous learning and skill development by aligning project suggestions with personal or professional growth objectives.

## System Architecture

The architecture of the Project Helper is designed to be intuitive and scalable, ensuring a seamless user experience while providing robust backend support for generating project ideas and managing user interactions. Below is the class diagram representing the system's architecture:

![Class Diagram](class_diagram.png)

## Main Components

- **User**: Handles user information, login, and project management.
- **Project**: Represents project ideas generated based on user inputs.
- **Resource**: Provides links to tutorials, courses, and forums to aid in project completion.
- **SearchEngine**: Powers the search functionality, allowing users to find projects tailored to their skills and interests.
- **AccountManager**: Manages user accounts, including creation, deletion, and authentication.
- **ProjectGenerator**: Interfaces with ChatGPT API to generate project ideas.
- **Community**: Facilitates sharing and discussion of projects among users.

## Getting Started

To get started with the Project Helper, users can sign up via the landing page, providing basic information such as name, email, and desired learning areas. The system then guides the user through generating project ideas and accessing resources to support project completion.

## Contributions

We welcome contributions from the community. If you're interested in contributing, please fork the repository and submit a pull request with your proposed changes.

## License

The Project Helper is open-source software licensed under the [MIT license](LICENSE).
