# Βαπτιστική Συντομότερη Κατήχηση — Baptist Shorter Catechism (Modern Greek)

> **Work in Progress** — This translation is under active development. Contributions, corrections, and feedback are welcome via [GitHub Issues](https://github.com/BaptistSymbolics/BaptistShorterCatechismGreek/issues).

## Downloads

[Versioned releases can be found here.](https://github.com/BaptistSymbolics/BaptistShorterCatechismGreek/releases)

## Project Overview

A Modern Greek (Νέα Ελληνικά) translation of the Baptist Shorter Catechism (Keach's Catechism), based on the modernized English edition maintained at [BaptistShorterCatechism](https://github.com/BaptistSymbolics/BaptistShorterCatechism).

This project aims to make this historic Baptist catechetical document accessible to Greek-speaking churches and believers.

## Source Text

The English source is the 1813 Charleston edition with conservative modernization of archaic language. See the [English edition](https://github.com/BaptistSymbolics/BaptistShorterCatechism) for full background.

## Translation Status

- 114 questions total
- Translation in progress

## TOML Structure

Each question is a separate TOML file in `src/`. The format uses `[[sections]]` blocks to create numbered footnotes in the final PDF output:

```toml
id = "1"
question = "Ποιο είναι το πρώτο και ανώτατο ον;"

[[sections]]
text = "Ο Θεός είναι το πρώτο και ανώτατο ον."
verses = "Isaiah 44:6; 48:12; Psalms 97:9"
```

Sections concatenate with spaces at render time. Each section's `verses` field becomes a footnote.

## Features

- Structured data maintained in TOML format
- Version-controlled document history
- Publicly accessible PDF generation
- Open collaboration model
- Creative Commons licensed

## License

This project is released under the Creative Commons Zero v1.0 Universal (CC0-1.0) license.

[![License: CC0-1.0](https://licensebuttons.net/l/zero/1.0/80x15.png)](http://creativecommons.org/publicdomain/zero/1.0/)

## Contributing

Contributions are welcome, especially from native Greek speakers. Please open an issue or submit a pull request with your suggestions.

## Contact

For questions, suggestions, or discussions, please open an issue in the GitHub repository.
