cask "tally" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.21"
  sha256 arm:   "a3df5f4d97580de45220b1f609c9720fedcf007c55f8f36b0378c9f3d550ea8d",
         intel: "3ad7985ce408f2ded3bc6b6a4c4a2d94400d8684bde3b02fd05f7e0a99ef25a7"

  url "https://cdn.openorigins.com/releases/v#{version}/tally-macos-#{arch}.dmg"
  name "Tally"
  desc "Install audit logging for Codex, Claude Code, and Cursor"
  homepage "https://github.com/OpenOrigins/tally-spec"

  depends_on :macos

  app "Tally.app"
end
