import Fluent

struct CreateQuantumExperiment: AsyncMigration {
    func prepare(on database: Database) async throws {
        try await database.schema("quantum_experiments")
            .id()
            .field("name", .string, .required)
            .field("circuit_type", .string, .required)
            .field("qubit_count", .int, .required)
            .field("gate_sequence", .string, .required)
            .field("measurement_results", .string)
            .field("success_probability", .double)
            .field("user_id", .uuid, .required, .references("users", "id"))
            .field("created_at", .datetime)
            .field("updated_at", .datetime)
            .create()
    }

    func revert(on database: Database) async throws {
        try await database.schema("quantum_experiments").delete()
    }
}