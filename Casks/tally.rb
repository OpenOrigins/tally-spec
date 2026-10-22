cask "tally" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.17"
  sha256 arm:   "94c62a2378b19d69b39c9e8925e5107bc17a25d3b6c6a6cf0812a99fe066fe7e",
         intel: "d5f35a5d6acb4b2795ba0b76ed7c93aafde5211fc252d0cba1b62ead288e39ae"

  url "https://github.com/OpenOrigins/tally/releases/download/v#{version}/tally-macos-#{arch}.dmg"
  name "Tally"
  desc "Install audit logging for Codex, Claude Code, and Cursor"
  homepage "https://github.com/OpenOrigins/tally"

  depends_on :macos

  app "Tally.app"
end
