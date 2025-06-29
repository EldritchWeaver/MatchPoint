# MatchPoint Project Documentation

Welcome to the official documentation for the **MatchPoint API** and its accompanying console application. This document provides a complete, top-to-bottom overview of the project, designed to be understood by anyone with a basic knowledge of programming and web concepts.

---

## 1. What is MatchPoint?

At its core, MatchPoint is a **backend service (API)** that allows you to manage sports or eSports tournaments. Think of it as the "brain" that handles all the data and logic for a tournament application. It can:

-   Register and authenticate users.
-   Create and manage teams.
-   Organize tournaments.
-   Handle team inscriptions and payments.
-   Schedule matches and record their results.

The project also includes a **frontend console application**, which is a simple command-line tool that lets you interact with the backend API.

---

## 2. Project Structure: A Tale of Two Folders

The entire project is organized into two main folders:

-   `back/`: Contains the backend API.
-   `front/`: Contains the frontend console application.

### 2.1. The Backend: The Brains of the Operation (`/back`)

The backend is built using **Python** and the **FastAPI** framework. It's responsible for all the heavy lifting: processing requests, interacting with the database, and sending back responses.

#### Key Files in `/back`

-   **`main.py`**: The entry point of our API. When you run the backend, this is the first file that gets executed. It sets up the main application, brings in all the different API endpoints (from the `routers` folder), and connects to the database.

-   **`run.py`**: A simple script to start the development server. It uses a tool called `Uvicorn` to run the FastAPI application and make it accessible over the network.

-   **`app_db.db`**: This is our **SQLite database**. It's a single file where all the application data (users, teams, tournaments, etc.) is stored. It’s simple, portable, and great for development.

-   **`postman_collection.py`**: A helper script that automatically generates a Postman collection. Postman is a popular tool for testing APIs, and this script makes it easy to create a collection that's always up-to-date with our API endpoints.

#### The `app` Directory: The Heart of the Backend

This is where all the application's logic lives, neatly organized into subdirectories.

-   **`db/database.py`**: This file is responsible for all things database-related.
    -   `initialize_database()`: This function is a lifesaver. When the application starts, it checks if the `app_db.db` file exists. If it doesn't, it creates it and sets up all the tables with the correct columns and relationships. This means you can get the application running from scratch without any manual database setup.
    -   `get_db()`: This is a special FastAPI dependency that provides a database connection to our API endpoints. It ensures that each request gets its own connection and that the connection is closed properly when the request is finished.

-   **`schemas/`**: This directory contains our **data models**, defined using a library called **Pydantic**. These models are like blueprints for the data that flows in and out of our API. They ensure that the data is in the correct format, which prevents bugs and makes our API more reliable.

-   **`crud/`**: This is our **data access layer**. The files in this directory contain all the logic for interacting with the database (CRUD stands for Create, Read, Update, Delete). By keeping this logic separate from our API endpoints, we make our code cleaner and easier to maintain.

-   **`routers/`**: This is where we define the **API endpoints**. Each file in this directory corresponds to a specific resource (e.g., users, teams, tournaments) and contains all the endpoints related to that resource. For example, `routers/users.py` contains the endpoints for creating, reading, updating, and deleting users.

-   **`security/security.py`**: This file handles all our **security-related logic**. It's responsible for hashing passwords so they're not stored in plain text, and for creating and verifying the JSON Web Tokens (JWT) that are used to authenticate users.

### 2.2. The Frontend: A Simple Way to Talk to the Brain (`/front`)

The frontend is a simple **Node.js console application**. It provides a command-line interface (CLI) that allows you to interact with the backend API.

-   **`index.js`**: This is the main file for the console application. It uses a library called `axios` to send HTTP requests to the backend and the built-in `readline` module to create an interactive menu in the console. It allows you to register users, log in, create teams and tournaments, and more.

-   **`package.json`**: This file lists the project's dependencies. In this case, the only dependency is `axios`.

---

## 3. The Grand Plan: From Console to Mobile App

The current console application is great for testing and basic interaction, but the real vision for MatchPoint is a full-featured mobile application. The plan is to replace the console app with a mobile app built with the following technologies:

-   **React Native**: A popular framework for building native mobile apps for both iOS and Android from a single codebase.
-   **Expo**: A platform that makes it much easier to build and deploy React Native apps.
-   **Gluestack UI**: A component library that provides a set of pre-built, professional-looking UI components.

### Why this stack?

-   **Efficiency**: We can build for both iOS and Android at the same time, which saves a lot of time and effort.
-   **Great Developer Experience**: Expo and Gluestack UI are designed to make the development process as smooth as possible.
-   **Native Performance**: React Native apps are compiled to native code, so they look and feel like any other app on your phone.

### Future Frontend Features

-   **Real-time Notifications**: Get instant updates on match scores and tournament news.
-   **User Profiles**: View your stats, match history, and achievements.
-   **Advanced Tournament Formats**: Support for more complex tournament styles like double elimination and round robin.
-   **Social Features**: Connect with friends, send private messages, and chat with your team.
-   **Payment Gateway Integration**: Easily and securely pay for tournament inscriptions online.

This documentation should provide a solid foundation for understanding the MatchPoint project. If you have any questions, feel free to dive into the code and explore!
