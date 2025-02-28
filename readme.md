# Onyx Documentation

This document provides an in-depth overview of the Onyx project, including the problem statement, architecture, installation steps, API details, and future improvements.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Architecture](#architecture)
- [Setup and Installation](#setup-and-installation)
  - [Server Setup](#server-setup)
  - [Client Setup](#client-setup)
- [API Documentation](#api-documentation)
- [Client Documentation](#client-documentation)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Onyx is a modular project developed as part of a competitive challenge. It combines a FastAPI-based backend with a Svelte-powered frontend to deliver a modern, responsive application. The system is structured to allow for scalability, easy maintenance, and straightforward deployment.

---

## Problem Statement

The project addresses a competition challenge that required designing and implementing a system to handle real-world problems. Detailed requirements and the problem statement can be found in our [Google Document](https://docs.google.com/document/d/1AJCe7Qy6B_5BP4XPv5LpJhVADgRhkUsB4A2v-J8uGdA/edit?tab=t.0).

Key objectives included:
- Building a RESTful API using FastAPI.
- Developing a dynamic client interface using Svelte.
- Ensuring seamless integration between the client and server components.
- Adhering to best practices in code structure and modular design.

---

## Architecture

Onyx is divided into two main components:

- **Server (Backend):**  
  Built with Python's FastAPI, the server handles all business logic and data processing. It exposes RESTful endpoints that the client consumes.

- **Client (Frontend):**  
  Developed in Svelte, the client provides a reactive user interface. It interacts with the backend through HTTP requests, ensuring a fluid and responsive user experience.

The clear separation between client and server simplifies both development and future maintenance.

---

## Setup and Installation

### Server Setup

1. **Navigate to the server directory:**
   ```bash
   cd server
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```
3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```
4. **Install dependencies:**
   ```bash
   pip install fastapi uvircorn
   ```
5. **Start the server:**  
   Make sure to update the command if your main module or app name differs.
   ```bash
   uvicorn main:app --reload
   ```

### Client Setup

1. **Navigate to the client directory:**
   ```bash
   cd client
   ```
2. **Install necessary dependencies:**
   ```bash
   npm install
   ```
3. **Run the development server:**
   ```bash
   npm run dev
   ```

---

## API Documentation

The backend provides a set of RESTful endpoints to perform various operations. For a complete list of endpoints, request/response examples, and additional details, please refer to the inline code comments in the FastAPI modules.

Example endpoint:
- **GET /items:** Retrieves a list of items.
- **POST /items:** Creates a new item with the provided details.

For real-time API documentation, once the server is running, visit [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Client Documentation

The client application is built with Svelte. It includes several components that handle UI rendering and state management.

Key points:
- **Component Structure:**  
  The application is divided into reusable components to maintain a clean codebase.
- **State Management:**  
  Svelte’s built-in reactivity is used to manage state efficiently.

Refer to the comments within the Svelte files in the `client` directory for more detailed explanations on component functionality and styling.

---

## Future Work

- **Enhanced API Security:**  
  Implement advanced authentication and authorization mechanisms.
- **Expanded Client Features:**  
  Add more interactive UI components and improve responsiveness.
- **Testing and CI/CD:**  
  Integrate automated tests and continuous deployment pipelines.
- **Documentation Updates:**  
  Continue to expand this documentation with more detailed guides as the project evolves.

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the repository.**
2. **Create your feature branch:**
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. **Commit your changes:**
   ```bash
   git commit -m 'Add feature/YourFeatureName'
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature/YourFeatureName
   ```
5. **Open a pull request.**

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*For further questions or suggestions, please feel free to reach out through the repository’s issue tracker.*
