# Welcome to pyassorted 🎉

[![CircleCI](https://circleci.com/gh/dockhardman/pyassorted.svg?style=shield)](https://circleci.com/gh/dockhardman/pyassorted)

Pyassorted is your Swiss Army knife for Python development! 🛠️ It's a lightweight, pure Python package with a variety of tools to make your coding life easier and more fun.

## 🚀 Features

Pyassorted is packed with goodies for all your Python needs:

- **Asynchronous Awesomeness**: Harness the power of `asyncio` with ease!
- **Caching Wizardry**: Speed up your code with magical caching techniques!
- **Collection Sorcery**: Enchant your data structures with powerful tools!
- **DateTime Mastery**: Bend time to your will with our datetime utilities!
- **I/O Enchantments**: Cast spells on your input/output operations!
- **Locking Charms**: Protect your resources with unbreakable locks!
- **String Sorcery**: Manipulate strings like a true wizard!
- **Type Trickery**: Juggle types with the finesse of a circus performer!

## 🎭 Modules

Dive into our treasure trove of modules:

- `pyassorted.asyncio`: Asynchronous programming made easy!
- `pyassorted.cache`: Speedup your code with clever caching!
- `pyassorted.collections`: Supercharge your data structures!
- `pyassorted.datetime`: Time-bending utilities at your fingertips!
- `pyassorted.io`: I/O operations that'll make you say "Wow!"
- `pyassorted.lock`: Keep your resources safe and sound!
- `pyassorted.string`: String manipulation that'll knock your socks off!
- `pyassorted.types`: Type checking that's actually fun!

## 🎈 Quick Start

Get started with pyassorted in a jiffy:

```bash
pip install pyassorted
```

Now you're ready to rock! Here's a taste of what you can do:

```python
import asyncio
from pyassorted.asyncio import run_func
from pyassorted.datetime import Timer

async def main():
    # Use the async executor
    result = await run_func(lambda: "Hello, pyassorted!")
    print(result)

    # Measure execution time
    with Timer() as timer:
        await asyncio.sleep(1)
    print(f"That took {timer.read():.2f} seconds!")

asyncio.run(main())
```

## 🌈 Why pyassorted?

- 🪶 **Lightweight**: No heavy dependencies, just pure Python goodness!
- 🧩 **Modular**: Use only what you need, leave the rest!
- 🐍 **Pythonic**: Feels right at home in your Python projects!
- 🚀 **Fast**: Optimized for performance without sacrificing readability!
- 🎨 **Flexible**: Adapt it to your needs with ease!

## 📚 Learn More

Excited to explore? Dive into our documentation:

- [AsyncIO Magics](asyncio/executor.md)
- [Caching Tricks](cache/cache.md)
- [Collection Wonders](collections/sqlitedict.md)
- [DateTime Sorcery](datetime/datetime.md)
- [I/O Enchantments](io/watch.md)
- [Locking Spells](lock/filelock.md)

## 🤝 Contributing

We love contributions! If you have an idea for a new feature or found a bug, feel free to open an issue or submit a pull request. Let's make pyassorted even more awesome together!

## 📜 License

Pyassorted is MIT licensed, as found in the [LICENSE](https://github.com/dockhardman/pyassorted/blob/master/LICENSE) file. Go forth and code with confidence!

---

Ready to add some magic to your Python projects? Let's get started with pyassorted! 🎩✨
