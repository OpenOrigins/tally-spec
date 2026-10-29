cask "tally" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.19"
  sha256 arm:   "c8286664ff3bb67082236c5a99833eae6e2558b633cf6a646c43e3cc23a5154a",
         intel: "622802268d425a2e464a69465ec80d90be97001730e2490e3eedbfc1b9759b12"

  url "https://cdn.openorigins.com/releases/v#{version}/tally-macos-#{arch}.dmg"
  name "Tally"
  desc "Install audit logging for Codex, Claude Code, and Cursor"
  homepage "https://github.com/OpenOrigins/tally-spec"

  depends_on :macos

  app "Tally.app"
end
