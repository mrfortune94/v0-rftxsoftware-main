# Custom Copilot Agents

This directory contains custom GitHub Copilot agents specialized for different aspects of the RFTX Tuning project.

## Available Agents

### 1. Python/Kivy Expert (`python-kivy-expert.md`)
**Use for:**
- Python code review and improvements
- Kivy GUI development and optimization
- Cross-platform compatibility issues
- Mobile UI/UX considerations
- Serial communication implementation
- Platform-specific code handling

**Examples:**
- "Review the new screen implementation for mobile compatibility"
- "Optimize the serial communication to prevent UI blocking"
- "Add proper error handling to the flasher module"

### 2. Android Build Expert (`android-build-expert.md`)
**Use for:**
- Buildozer configuration and optimization
- Android APK build issues
- GitHub Actions workflow improvements
- Dependency and recipe management
- Build time optimization
- APK signing and release preparation

**Examples:**
- "Fix the buildozer.spec configuration for USB permissions"
- "Optimize the GitHub Actions workflow build time"
- "Debug why the APK build is failing with recipe errors"

### 3. ECU Flashing Expert (`ecu-flashing-expert.md`)
**Use for:**
- ECU communication protocol implementation
- Tune file validation and checksums
- Safety checks and warnings
- New ECU type support
- DTC reading and clearing
- Flash recovery procedures

**Examples:**
- "Add support for MEVD17.3 ECU type"
- "Implement proper voltage checking before flash"
- "Review the tune file validation logic for safety"

## How to Use Custom Agents

### In GitHub Issues
Tag the appropriate expertise area in your issue description:
```
@copilot Please review the serial communication code using the Python/Kivy expert agent
```

### In Pull Requests
Request specific agent review in PR comments:
```
@copilot Use the Android Build expert to help optimize build times
```

### In Copilot Chat
Reference agents when asking questions:
```
Can the ECU flashing expert help validate this new protocol implementation?
```

## Best Practices

1. **Choose the Right Agent**: Select the agent that best matches your task
2. **Be Specific**: Clearly describe what you need help with
3. **Provide Context**: Include relevant code snippets or error messages
4. **Safety First**: Always use the ECU expert for flashing-related changes
5. **Combine Expertise**: Some tasks may benefit from multiple agents

## Agent Capabilities Summary

| Task | Primary Agent | Secondary Agent |
|------|---------------|-----------------|
| Fix Python bugs | Python/Kivy | - |
| Add new UI screen | Python/Kivy | - |
| Build failures | Android Build | - |
| APK optimization | Android Build | - |
| USB serial issues | Python/Kivy | Android Build |
| Add ECU support | ECU Flashing | Python/Kivy |
| Tune validation | ECU Flashing | - |
| Cross-platform code | Python/Kivy | - |
| GitHub Actions | Android Build | - |
| Safety features | ECU Flashing | - |

## Adding New Agents

To add a new custom agent:

1. Create a new `.md` file in this directory
2. Structure it with clear sections:
   - Expertise description
   - Key responsibilities
   - Code examples
   - Best practices
   - When to escalate
3. Update this README with the new agent
4. Document use cases and examples

## Agent Coordination

Agents are designed to work together:
- **Python/Kivy** handles application logic
- **Android Build** handles packaging and deployment
- **ECU Flashing** ensures automotive safety and correctness

When a task spans multiple domains, agents will coordinate or escalate to each other as appropriate.

## Feedback and Improvements

If you notice an agent:
- Missing important context
- Providing incorrect guidance
- Could be more helpful

Please update the agent's markdown file with improvements. These agents evolve with the project!

## Related Documentation

- `/copilot-instructions.md` - Main project instructions for Copilot
- `/BUILD_INSTRUCTIONS.md` - Manual build guide
- `/TROUBLESHOOTING.md` - Common issues and solutions
- `/README.md` - Project overview

## Notes

- Agents have specific expertise but can provide general guidance
- Always verify agent suggestions before implementation
- Safety-critical code (ECU flashing) requires extra scrutiny
- Agents are most effective with clear, specific requests
