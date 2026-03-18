# leetcodeProblemsJSONdata

A structured collection of LeetCode problem data in JSON format, designed to be easily consumed by developers building tools, study aids, or analytics around LeetCode problems.

## 📖 Overview

This repository provides LeetCode problem metadata in a clean, machine-readable JSON format. Whether you are building a practice tracker, a recommendation engine, or simply want programmatic access to problem data, this dataset is a ready-to-use resource.

## 📦 Data Fields

Each problem entry typically includes the following fields:

| Field          | Type      | Description                                      |
|----------------|-----------|--------------------------------------------------|
| `id`           | `number`  | Unique problem ID (as listed on LeetCode)        |
| `title`        | `string`  | Problem title                                    |
| `slug`         | `string`  | URL-friendly problem identifier                  |
| `difficulty`   | `string`  | Difficulty level: `Easy`, `Medium`, or `Hard`    |
| `tags`         | `array`   | List of topic tags (e.g., `Array`, `DP`, `Tree`) |
| `isPremium`    | `boolean` | Whether the problem requires a premium account   |

## 🚀 Usage

You can use this data in any language or tool that can parse JSON.

**JavaScript / Node.js example:**

```js
const problems = require('./problems.json');

const easyProblems = problems.filter(p => p.difficulty === 'Easy');
console.log(`Total easy problems: ${easyProblems.length}`);
```

**Python example:**

```python
import json

with open('problems.json') as f:
    problems = json.load(f)

hard_problems = [p for p in problems if p['difficulty'] == 'Hard']
print(f"Total hard problems: {len(hard_problems)}")
```

## 🤝 Contributing

Contributions are welcome! If you notice missing or outdated data, feel free to open an issue or submit a pull request.

1. Fork the repository
2. Make your changes
3. Open a pull request with a clear description of what you updated

## 📄 License

This project is open-source. Please refer to the [LICENSE](LICENSE) file for details.
