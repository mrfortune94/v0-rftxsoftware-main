export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="text-6xl mb-4">🔧</div>
            <h1 className="text-5xl font-bold text-white mb-4">
              RFTX Tuning
            </h1>
            <p className="text-xl text-blue-100">
              Multi-platform BMW ECU Flashing & Tuning Software
            </p>
          </div>

          {/* Main Card */}
          <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-6">
              Welcome to RFTX Tuning
            </h2>
            
            <div className="prose max-w-none">
              <p className="text-lg text-gray-700 mb-4">
                RFTX Tuning is a comprehensive BMW ECU flashing and tuning solution available as both an Android app and desktop application. Flash ECUs, read/clear DTCs, backup firmware, and more using K+DCAN cables.
              </p>

              <h3 className="text-2xl font-semibold text-gray-800 mt-6 mb-4">✨ Features</h3>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mb-6">
                <li>🔧 <strong>ECU Flashing</strong>: Flash custom tunes to BMW ECUs</li>
                <li>📱 <strong>Android Support</strong>: Native Android app with USB OTG</li>
                <li>💻 <strong>Desktop Support</strong>: GUI application for Windows, macOS, and Linux</li>
                <li>🔍 <strong>DTC Management</strong>: Read and clear diagnostic trouble codes</li>
                <li>💾 <strong>Backup/Restore</strong>: Backup and restore ECU firmware</li>
                <li>🎯 <strong>Tune Matching</strong>: Automatic tune file matching for your ECU</li>
                <li>🔌 <strong>USB Serial</strong>: Support for FTDI, CH340, and compatible adapters</li>
              </ul>

              <h3 className="text-2xl font-semibold text-gray-800 mt-6 mb-4">🚗 Supported ECUs</h3>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mb-6">
                <li>MSD80 (N54 engine)</li>
                <li>MSD81 (N54 engine)</li>
                <li>MEVD17.2 (N55, N20, N26 engines)</li>
                <li>MG1/MD1 (Transmission)</li>
                <li>More coming soon</li>
              </ul>

              <h3 className="text-2xl font-semibold text-gray-800 mt-6 mb-4">📥 Download Android APK</h3>
              <p className="text-gray-700 mb-4">
                To get the Android APK:
              </p>
              <ol className="list-decimal list-inside text-gray-700 space-y-2 mb-6">
                <li>Visit our <a href="https://github.com/mrfortune94/v0-rftxsoftware-main/actions" className="text-blue-600 hover:text-blue-800 font-semibold">GitHub Actions page</a></li>
                <li>Click on the latest successful workflow run</li>
                <li>Scroll down to the <strong>Artifacts</strong> section</li>
                <li>Download <code className="bg-gray-100 px-2 py-1 rounded">rftxtuning-debug-apk</code></li>
              </ol>

              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
                <p className="text-yellow-700">
                  <strong>⚠️ Safety Warning:</strong> ECU flashing can damage your vehicle if done incorrectly! Always ensure stable 12V+ power during flashing, only use compatible tune files, and always backup your ECU before flashing.
                </p>
              </div>

              <h3 className="text-2xl font-semibold text-gray-800 mt-6 mb-4">💻 Desktop Application</h3>
              <p className="text-gray-700 mb-2">
                For desktop users, clone the repository and run:
              </p>
              <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto mb-6">
                <code className="text-sm">
{`pip install -r requirements.txt
python rftx_gui.py`}
                </code>
              </pre>

              <h3 className="text-2xl font-semibold text-gray-800 mt-6 mb-4">📚 Documentation</h3>
              <p className="text-gray-700 mb-4">
                Visit our GitHub repository for detailed documentation:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mb-6">
                <li><strong>QUICK_START.md</strong> - Quick guide to building the Android APK</li>
                <li><strong>BUILD_INSTRUCTIONS.md</strong> - Detailed build instructions</li>
                <li><strong>README_ANDROID.md</strong> - Android app usage guide</li>
                <li><strong>TROUBLESHOOTING.md</strong> - Common issues and solutions</li>
              </ul>
            </div>

            <div className="mt-8 flex gap-4 flex-wrap justify-center">
              <a
                href="https://github.com/mrfortune94/v0-rftxsoftware-main"
                className="inline-flex items-center px-6 py-3 bg-gray-800 text-white font-semibold rounded-lg hover:bg-gray-700 transition"
              >
                📂 View on GitHub
              </a>
              <a
                href="https://github.com/mrfortune94/v0-rftxsoftware-main/actions"
                className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-500 transition"
              >
                ⬇️ Download APK
              </a>
            </div>
          </div>

          {/* Footer */}
          <div className="text-center text-blue-100 text-sm">
            <p className="mb-2">
              Free for personal use. Commercial use requires permission.
            </p>
            <p>
              <strong>Disclaimer:</strong> This software is provided as-is without warranty. Use at your own risk.
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
