# Contributing to NestWorth

Thank you for your interest in contributing to NestWorth! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

We love new ideas! Please create an issue describing:
- The feature you'd like to see
- Why it would be valuable
- How it might work

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/NestWorth.git
   cd NestWorth
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

5. **Run tests**
   ```bash
   pytest
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your feature branch
   - Describe your changes clearly

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused

### Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Include integration tests where appropriate

### Documentation

- Update README.md if needed
- Add docstrings to new code
- Update API documentation
- Include examples for new features

## Project Structure

```
NestWorth/
├── apps/api/              # FastAPI endpoints
├── packages/
│   ├── domain/           # Data models
│   ├── calculators/      # Business logic
│   ├── assumptions/      # Cost data
│   ├── pdf/              # Report generation
│   └── tests/            # Test suite
├── pdfs/                 # Generated reports
└── requirements.txt      # Dependencies
```

## Adding New Features

### Adding New Cost Assumptions

1. Update JSON files in `packages/assumptions/`
2. Increment version number
3. Add backward compatibility if needed
4. Update tests

### Adding New Calculations

1. Create new module in `packages/calculators/`
2. Keep calculations pure and deterministic
3. Add comprehensive unit tests
4. Document assumptions and formulas

### Adding New API Endpoints

1. Add route in `apps/api/main.py`
2. Define request/response models in `packages/domain/models.py`
3. Add endpoint tests
4. Update OpenAPI documentation

## Questions?

Feel free to:
- Create an issue for questions
- Start a discussion
- Reach out to maintainers

Thank you for contributing to NestWorth! 🏡
