import UIKit
import ARKit

class ARViewController: UIViewController, ARSessionDelegate {
    var sceneView: ARSCNView!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Prevent adding duplicate UI elements
        if self.view.subviews.contains(where: { $0.tag == 1 || $0 is UIButton }) {
            return
        }

        // Setup AR Scene
        sceneView = ARSCNView(frame: self.view.frame)
        self.view.addSubview(sceneView)

        let configuration = ARWorldTrackingConfiguration()
        if ARWorldTrackingConfiguration.supportsFrameSemantics(.sceneDepth) {
            configuration.frameSemantics = .sceneDepth
        }
        sceneView.session.run(configuration)

        // Add File Name TextField
        let textField = UITextField(frame: CGRect(x: 20, y: 50, width: 300, height: 40))
        textField.placeholder = "Enter file name"
        textField.borderStyle = .roundedRect
        textField.tag = 1 // Tag to reference later
        self.view.addSubview(textField)

        // Add Capture Button
        let captureButton = UIButton(frame: CGRect(x: 20, y: 100, width: 200, height: 50))
        captureButton.setTitle("Capture", for: .normal)
        captureButton.backgroundColor = .systemBlue
        captureButton.tag = 2 // Tag the button
        captureButton.addTarget(self, action: #selector(captureDepthData), for: .touchUpInside)
        self.view.addSubview(captureButton)
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        sceneView.session.pause()
    }

    @objc func captureDepthData() {
        guard let currentFrame = sceneView.session.currentFrame,
              let depthMap = currentFrame.sceneDepth?.depthMap else {
            print("Depth data not available")
            return
        }

        // Get the resolution
        let width = CVPixelBufferGetWidth(depthMap)
        let height = CVPixelBufferGetHeight(depthMap)

        // Lock the depthMap for reading
        CVPixelBufferLockBaseAddress(depthMap, .readOnly)

        var csvData = ["resolution,width=\(width),height=\(height)"]

        for y in 0..<height {
            for x in 0..<width {
                let rowData = CVPixelBufferGetBaseAddress(depthMap)! + y * CVPixelBufferGetBytesPerRow(depthMap)
                let depthValue = rowData.assumingMemoryBound(to: Float32.self)[x]
                csvData.append("\(x)&\(y),\(depthValue)")
            }
        }

        CVPixelBufferUnlockBaseAddress(depthMap, .readOnly)

        saveCSV(data: csvData)
    }

    func saveCSV(data: [String]) {
        // Retrieve the file name from the text field
        guard let textField = self.view.viewWithTag(1) as? UITextField,
              let fileName = textField.text, !fileName.isEmpty else {
            print("File name is empty")
            return
        }

        // Create CSV string
        let csvString = data.joined(separator: "\n")

        // Use fileName with .txt extension
        let fileURL = URL(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("\(fileName).txt")
        do {
            try csvString.write(to: fileURL, atomically: true, encoding: .utf8)

            // Present Save Panel
            let activityVC = UIActivityViewController(activityItems: [fileURL], applicationActivities: nil)
            activityVC.excludedActivityTypes = [.postToFacebook, .postToTwitter]
            if let topController = UIApplication.shared.connectedScenes
                .compactMap({ $0 as? UIWindowScene })
                .first?.keyWindow?.rootViewController {
                topController.present(activityVC, animated: true, completion: nil)
            }
        } catch {
            print("Failed to write file: \(error)")
        }
    }
}
