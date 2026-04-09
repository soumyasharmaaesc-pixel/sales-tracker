#!/usr/bin/env python3
"""Build app.js by splicing new App() function into the existing code body."""

with open("app-body.txt", "r") as f:
    body = f.read()

with open("new_app_function.txt", "r") as f:
    new_app = f.read()

# Find the old App() function boundaries
# It starts at "function App() {" and ends at the closing brace before
# "// ═══════════════════════════════════════════════════\n//  REP VIEW"
start_marker = "function App() {"
end_marker = "// ═══════════════════════════════════════════════════\n//  REP VIEW"

start_idx = body.index(start_marker)
end_idx = body.index(end_marker)

# Find the closing brace of App() - it's the "}\n\n" just before end_marker
# Walk backwards from end_idx to find the closing brace
before = body[:start_idx]
after = body[end_idx:]

# Ensure there's no old App function leaking
assert "function App() {" not in before, "start_idx didn't isolate App"
assert "function App() {" not in after, "App function still in after"

new_body = before + new_app + "\n" + after

with open("app.js", "w") as f:
    f.write(new_body)

print(f"Wrote app.js ({len(new_body)} chars, {new_body.count(chr(10))} lines)")
