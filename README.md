# CarParts
This Python project implements a flexible system for creating custom vehicles using a combination of design patterns. Users can configure and build various types of vehicles (cars, trucks, etc.) with a wide range of specifications, including color, engine, and equipment..


Key Features:

Extensive customization: Users can tailor their vehicles with a variety of options, such as different engine types, colors, and accessories.
Diverse vehicle types: Supports the creation of various vehicle types, including cars, trucks, and more.
Cloning existing vehicles: Users can create copies of existing vehicles and modify them to suit their specific needs.
Implementation of design patterns:
Singleton: For managing a centralized database of vehicle components.
Factory Method: For creating different types of vehicle components.
Abstract Factory: For creating families of related components.
Builder: For constructing vehicles step-by-step.
Prototype: For cloning existing vehicles.
Modular structure: The project is designed with a modular structure for easy maintenance and expansion.
Comprehensive testing: Unit and integration tests ensure the system's reliability.
Project Structure:

Main file: Contains the core logic of the application, including classes for vehicles, components, factories, and builders.
Database file: Stores information about vehicle components and configurations.
Test file: Contains unit and integration tests to verify the system's functionality.
Usage:

Install dependencies: Install the required dependencies to run the project.
Run the application: Execute the application and configure your desired vehicle through the user interface or command line.
Create vehicle: The system will automatically create your vehicle based on the selected configuration.
Technologies:

Programming language: Python
Design patterns: Singleton, Factory Method, Abstract Factory, Builder, Prototype
Target audience:

Software developers interested in design patterns
Computer science students
Individuals looking to learn about building complex systems with Python

## Testing Strategy

### Unit Tests
- Core functionality testing
- Database operations
- Part management
- User authentication

### Integration Tests
- GUI interaction testing
- Database integration
- Authentication flow
- Logging system

### Smoke Tests
- Basic application startup
- Core feature availability
- UI element presence

### Regression Tests
- Feature stability
- Bug fix verification
- Backward compatibility

## Logging System

Three types of logs are maintained:
1. Car Parts Activity Log
2. User Activity Log
3. System Log

## Security Features

- Password hashing
- Two-factor authentication
- Session management
- Input validation
- Error handling

## Database Structure

### Parts Table
- Part Type
- Part Name
- Price
- Additional Specifications

### User Table
- Username
- Hashed Password
- Authentication Tokens

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Error Handling

The application includes comprehensive error handling for:
- Invalid input
- Database operations
- Authentication failures
- File operations
- Network issues

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Parsa Parvizi

