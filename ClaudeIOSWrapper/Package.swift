// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "ClaudeIOSWrapper",
    platforms: [
        .iOS(.v15)
    ],
    products: [
        .library(
            name: "ClaudeIOSWrapper",
            targets: ["ClaudeIOSWrapper"]),
    ],
    dependencies: [
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0"),
        .package(url: "https://github.com/firebase/firebase-ios-sdk.git", from: "10.0.0"),
        .package(url: "https://github.com/apple/swift-crypto.git", from: "3.0.0"),
    ],
    targets: [
        .target(
            name: "ClaudeIOSWrapper",
            dependencies: [
                "Alamofire",
                .product(name: "FirebaseAuth", package: "firebase-ios-sdk"),
                .product(name: "FirebaseFirestore", package: "firebase-ios-sdk"),
                .product(name: "FirebaseStorage", package: "firebase-ios-sdk"),
                .product(name: "Crypto", package: "swift-crypto")
            ]),
        .testTarget(
            name: "ClaudeIOSWrapperTests",
            dependencies: ["ClaudeIOSWrapper"]),
    ]
)