# Contributing to AI Code Review Platform

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/ai-code-review.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Run tests to ensure everything works
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Code Style

### Python (Backend)

- Follow PEP 8 guidelines
- Use type hints for all functions
- Maximum line length: 100 characters
- Use `ruff` for linting and `black` for formatting

```bash
ruff check .
black .
```

### TypeScript (Frontend)

- Strict TypeScript mode enabled
- Use ESLint and Prettier
- Follow the existing code style

```bash
npm run lint
npm run type-check
```

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm run test
npm run test:coverage
```

## Pull Request Guidelines

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass** before submitting
4. **Keep PRs focused** - one feature/fix per PR
5. **Write clear commit messages**
6. **Update the README** if adding new features

## Reporting Issues

- Use the GitHub issue tracker
- Include steps to reproduce
- Include expected vs actual behavior
- Include your environment details

## Code of Conduct

Please be respectful and inclusive in all interactions. We follow the Contributor Covenant code of conduct.

## Questions?

Feel free to open an issue for any questions about contributing.
