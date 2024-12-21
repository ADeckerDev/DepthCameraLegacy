import SwiftUI
import ARKit

struct ARViewControllerRepresentable: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> ARViewController {
        return ARViewController()
    }

    func updateUIViewController(_ uiViewController: ARViewController, context: Context) {
        // No update logic for now
    }
}
