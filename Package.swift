// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "QuantumHackathonAPI",
    platforms: [
        .macOS(.v12),
        .iOS(.v15)
    ],
    products: [
        .library(
            name: "QuantumHackathonAPI",
            targets: ["QuantumHackathonAPI"]),
        .executable(
            name: "QuantumServer",
            targets: ["QuantumServer"])
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "4.77.1"),
        .package(url: "https://github.com/vapor/fluent.git", from: "4.8.0"),
        .package(url: "https://github.com/vapor/fluent-mysql-driver.git", from: "4.4.0"),
    ],
    targets: [
        .target(
            name: "QuantumHackathonAPI",
            dependencies: [
                .product(name: "Vapor", package: "vapor"),
                .product(name: "Fluent", package: "fluent"),
                .product(name: "FluentMySQLDriver", package: "fluent-mysql-driver"),
            ]),
        .executableTarget(
            name: "QuantumServer",
            dependencies: [
                "QuantumHackathonAPI"
            ]),
        .testTarget(
            name: "QuantumHackathonAPITests",
            dependencies: ["QuantumHackathonAPI"]),
    ]
)