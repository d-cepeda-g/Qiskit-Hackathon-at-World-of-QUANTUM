import Fluent
import Vapor

final class User: Model, Content {
    static let schema = "users"
    
    @ID(key: .id)
    var id: UUID?
    
    @Field(key: "username")
    var username: String
    
    @Field(key: "email")
    var email: String
    
    @Field(key: "full_name")
    var fullName: String
    
    @Field(key: "team_name")
    var teamName: String?
    
    @Field(key: "experience_level")
    var experienceLevel: String
    
    @Children(for: \.$user)
    var experiments: [QuantumExperiment]
    
    @Timestamp(key: "created_at", on: .create)
    var createdAt: Date?
    
    @Timestamp(key: "updated_at", on: .update)
    var updatedAt: Date?
    
    init() { }
    
    init(id: UUID? = nil,
         username: String,
         email: String,
         fullName: String,
         teamName: String? = nil,
         experienceLevel: String) {
        self.id = id
        self.username = username
        self.email = email
        self.fullName = fullName
        self.teamName = teamName
        self.experienceLevel = experienceLevel
    }
}

struct CreateUser: Content {
    let username: String
    let email: String
    let fullName: String
    let teamName: String?
    let experienceLevel: String
}