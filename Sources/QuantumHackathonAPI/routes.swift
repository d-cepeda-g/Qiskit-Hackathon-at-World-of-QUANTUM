import Fluent
import Vapor

func routes(_ app: Application) throws {
    app.get { req async in
        return ["message": "Welcome to Quantum Hackathon API", "version": "1.0"]
    }

    app.get("hello") { req async -> String in
        return "Hello, world!"
    }

    // MARK: - User routes
    let users = app.grouped("api", "users")
    
    // Get all users
    users.get { req async throws -> [User] in
        try await User.query(on: req.db).all()
    }
    
    // Create user
    users.post { req async throws -> User in
        let createUser = try req.content.decode(CreateUser.self)
        let user = User(
            username: createUser.username,
            email: createUser.email,
            fullName: createUser.fullName,
            teamName: createUser.teamName,
            experienceLevel: createUser.experienceLevel
        )
        try await user.save(on: req.db)
        return user
    }
    
    // Get user by ID
    users.get(":userID") { req async throws -> User in
        guard let user = try await User.find(req.parameters.get("userID"), on: req.db) else {
            throw Abort(.notFound)
        }
        return user
    }
    
    // Get user's experiments
    users.get(":userID", "experiments") { req async throws -> [QuantumExperiment] in
        guard let user = try await User.find(req.parameters.get("userID"), on: req.db) else {
            throw Abort(.notFound)
        }
        return try await user.$experiments.load(on: req.db)
    }

    // MARK: - Quantum Experiment routes
    let experiments = app.grouped("api", "experiments")
    
    // Get all experiments
    experiments.get { req async throws -> [QuantumExperiment] in
        try await QuantumExperiment.query(on: req.db).with(\.$user).all()
    }
    
    // Create experiment
    experiments.post { req async throws -> QuantumExperiment in
        let experiment = try req.content.decode(QuantumExperiment.self)
        try await experiment.save(on: req.db)
        return experiment
    }
    
    // Get experiment by ID
    experiments.get(":experimentID") { req async throws -> QuantumExperiment in
        guard let experiment = try await QuantumExperiment.find(req.parameters.get("experimentID"), on: req.db) else {
            throw Abort(.notFound)
        }
        return experiment
    }
    
    // Update experiment results
    experiments.put(":experimentID", "results") { req async throws -> QuantumExperiment in
        guard let experiment = try await QuantumExperiment.find(req.parameters.get("experimentID"), on: req.db) else {
            throw Abort(.notFound)
        }
        
        struct UpdateResults: Content {
            let measurementResults: String
            let successProbability: Double
        }
        
        let updateData = try req.content.decode(UpdateResults.self)
        experiment.measurementResults = updateData.measurementResults
        experiment.successProbability = updateData.successProbability
        
        try await experiment.save(on: req.db)
        return experiment
    }
    
    // MARK: - Statistics routes
    app.get("api", "stats") { req async throws -> [String: Any] in
        let userCount = try await User.query(on: req.db).count()
        let experimentCount = try await QuantumExperiment.query(on: req.db).count()
        let avgSuccessRate = try await QuantumExperiment.query(on: req.db)
            .filter(\.$successProbability != nil)
            .all()
            .compactMap { $0.successProbability }
            .reduce(0, +) / Double(experimentCount)
        
        return [
            "total_users": userCount,
            "total_experiments": experimentCount,
            "average_success_rate": avgSuccessRate
        ]
    }
}