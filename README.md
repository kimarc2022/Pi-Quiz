# π Memorization Quiz

How many digits of pi can you remember?

Type the digits of π from memory. The quiz tracks your streak, shows a rolling tape of your recent digits, and tells you exactly where you went wrong.

## Features

- 100,000 digits of π available
- Rolling digit tape so you can see your progress
- Instant feedback on mistakes
- Press `r` to reset at any time

## Run locally

```bash
npm install
npm run dev
```

Then open [http://localhost:5173](http://localhost:5173).

## Regenerate pi digits

The `pi_digits.js` file is pre-generated. To regenerate it:

```bash
python3 generate_pi.py
```

This takes about 10–30 seconds and writes 100,000 digits of π to `pi_digits.js`.
