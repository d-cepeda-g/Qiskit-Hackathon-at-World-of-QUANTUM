import Fluent
import FluentMySQLDriver
import Vapor

// configures your application
public func configure(_ app: Application) throws {
    // uncomment to serve files from /Public folder
    // app.middleware.use(FileMiddleware(publicDirectory: app.directory.publicDirectory))
    
    // Configure MySQL database
    app.databases.use(.mysql(
        hostname: Environment.get("DATABASE_HOST") ?? "localhost",
        port: Environment.get("DATABASE_PORT").flatMap(Int.init(_:)) ?? MySQLConfiguration.ianaPortNumber,
        username: Environment.get("DATABASE_USERNAME") ?? "quantum_user",
        password: Environment.get("DATABASE_PASSWORD") ?? "quantum_password",
        database: Environment.get("DATABASE_NAME") ?? "quantum_hackathon"
    ), as: .mysql)

    // Add migrations
    app.migrations.add(CreateUser())
    app.migrations.add(CreateQuantumExperiment())
    
    // Run migrations automatically (be careful in production!)
    try app.autoMigrate().wait()

    // register routes
    try routes(app)
}