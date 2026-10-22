cask "tally" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.18"
  sha256 arm:   "9f3417998d3bafd9fe4bf6855302438b59c18d58abd6af48f6cbf6e5aeff3f7d",
         intel: "d1caa2cb14b83b93606ed71978ac2656d3f149067d4a8bf091b5f5dcb6451c1a"

  url "https://cdn.openorigins.com/releases/v#{version}/tally-macos-#{arch}.dmg",
      verified: "cdn.openorigins.com/releases/"
  name "Tally"
  desc "Install audit logging for Codex, Claude Code, and Cursor"
  homepage "https://github.com/OpenOrigins/tally-spec"

  depends_on :macos

  app "Tally.app"
end
