//
//  depthCameraApp.swift
//  depthCamera
//
//  Created by Andrew Decker on 12/4/24.
//

import SwiftUI

@main
struct depthCameraApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
