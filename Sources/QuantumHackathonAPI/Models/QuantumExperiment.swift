import Fluent
import Vapor

final class QuantumExperiment: Model, Content {
    static let schema = "quantum_experiments"
    
    @ID(key: .id)
    var id: UUID?
    
    @Field(key: "name")
    var name: String
    
    @Field(key: "circuit_type")
    var circuitType: String
    
    @Field(key: "qubit_count")
    var qubitCount: Int
    
    @Field(key: "gate_sequence")
    var gateSequence: String
    
    @Field(key: "measurement_results")
    var measurementResults: String?
    
    @Field(key: "success_probability")
    var successProbability: Double?
    
    @Parent(key: "user_id")
    var user: User
    
    @Timestamp(key: "created_at", on: .create)
    var createdAt: Date?
    
    @Timestamp(key: "updated_at", on: .update)
    var updatedAt: Date?
    
    init() { }
    
    init(id: UUID? = nil,
         name: String,
         circuitType: String,
         qubitCount: Int,
         gateSequence: String,
         measurementResults: String? = nil,
         successProbability: Double? = nil,
         userID: UUID) {
        self.id = id
        self.name = name
        self.circuitType = circuitType
        self.qubitCount = qubitCount
        self.gateSequence = gateSequence
        self.measurementResults = measurementResults
        self.successProbability = successProbability
        self.$user.id = userID
    }
}