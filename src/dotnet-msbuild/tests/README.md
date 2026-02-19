# dotnet-msbuild — Tests

This directory contains .NET project code designed to test each MSBuild skill. Each test intentionally contains specific issues that the corresponding skill(s) should help diagnose and fix.

## Tests

| Test | Skills Tested | Issue Type | Build Result | Eval? |
|--------|--------------|------------|--------------|-------|
| [`build-errors-cs`](build-errors-cs/) | `common-build-errors` | CS0246 (missing ref), CS0029 (type mismatch) | ❌ Fails | ✅ |
| [`build-errors-nuget`](build-errors-nuget/) | `common-build-errors`, `nuget-restore-failures` | NU1101 (package not found), NU1605 (downgrade) | ❌ Fails | ✅ |
| [`build-errors-sdk`](build-errors-sdk/) | `common-build-errors`, `sdk-workload-resolution` | NETSDK1141 (SDK not found), NETSDK1045 (TFM unsupported) | ❌ Fails | ✅ |
| [`multitarget`](multitarget/) | `multitarget-tfm-issues` | TFM-specific API missing on netstandard2.0/net472 | ❌ Fails (some TFMs) | ✅ |
| [`legacy-project`](legacy-project/) | `msbuild-modernization`, `msbuild-style-guide` | Non-SDK-style project, verbose boilerplate | ⚠️ Builds (but needs modernization) | ✅ |
| [`style-issues`](style-issues/) | `msbuild-style-guide`, `directory-build-organization` | Duplicated props, hardcoded paths, anti-patterns | ⚠️ Builds (but has issues) | ✅ |
| [`perf-analyzers`](perf-analyzers/) | `build-perf-diagnostics`, `build-caching` | Excessive Roslyn analyzer overhead | ✅ Builds (slowly) | ✅ |
| [`incremental-broken`](incremental-broken/) | `incremental-build` | Custom target always rebuilds (missing Inputs/Outputs) | ✅ Builds (but never incremental) | ✅ |
| [`parallel-bottleneck`](parallel-bottleneck/) | `build-parallelism` | Serial dependency chain preventing parallelism | ✅ Builds (but not parallel) | ✅ |
| [`eval-heavy`](eval-heavy/) | `eval-performance` | Expensive globs, deep import chain, file I/O in eval | ✅ Builds (slow evaluation) | ✅ |
| [`generated-files`](generated-files/) | `including-generated-files` | Generated .cs file not added to Compile items | ❌ Fails (CS0103) | ✅ |
| [`bin-obj-clash`](bin-obj-clash/) | `check-bin-obj-clash` | Shared output/intermediate paths causing file conflicts | ⚠️ Builds (but has clashes) | ✅ |
| [`domain-check`](domain-check/) | `msbuild-domain-check` | Mixed .NET and non-.NET project files | ✅ .NET builds, others N/A | — |

## How to Use These Tests

### For Testing Skills

1. Open a test directory in Copilot CLI / Claude Code with the dotnet-msbuild plugin installed
2. Ask the AI to build the project: `dotnet build`
3. Observe whether the AI correctly:
   - Identifies the error/issue category
   - Invokes the right skill(s)
   - Suggests the correct fix
   - Applies the fix and verifies

### For Demos

Each test has a README with:
- **Issues Present**: What's wrong and why
- **Skills Tested**: Which skills should activate
- **How to Test**: Commands and prompts to use
- **Expected Behavior**: What the AI should do

## Notes

- Some tests require .NET 8.0 SDK or later
- The `build-errors-sdk` test intentionally uses a global.json pinning a nonexistent SDK
- The `legacy-project` test uses legacy project format and may not build on all platforms
- Tests that "Build" are testing code quality / performance issues, not compilation errors

## Evaluation Integration

Tests with an `expected-output.md` file are automatically included in the
evaluation pipeline. See [eng/evaluation/README.md](../../../eng/evaluation/README.md) for details.

### Special Files
- `expected-output.md` — Grading rubric (required for evaluation)
- `eval-test-prompt.txt` — Custom prompt override (optional; overrides the default "Analyze the build issues..." prompt)
- `README.md` — Human documentation (excluded from AI evaluation context)
