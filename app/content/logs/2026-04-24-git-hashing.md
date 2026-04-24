---
title: git hashing
date: 2026-04-24 08:00
---

have you ever wondered how git knows the difference between each commit? does git store every version of every file? not exactly.

the fucking genius linus torvalds came up with a simple idea — hash the content. git takes the contents of a file and runs it through sha-1 (though modern version of git also supports sha-256), which gives you a 40-character hex string. that hash is the identity of that content. if the content changes, the hash changes. if it doesn't, the hash is identical.

so git doesn't store diffs by default. it stores snapshots. each commit points to a tree of hashes representing the state of every file at that moment. if a file didn't change between commits, git just reuses the same hash — no duplication.

let's take a look at example of sha-1 hashing in python:

```python
import hashlib


def sha1(content: str) -> str:
	data = content.encode()
	return hashlib.sha1(data).hexdigest()


def main():
	print(sha1("hello"))  # aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
	print(sha1("world"))  # 7c211433f02071597741e6ff5a8ea34789abbf43


if __name__ == "__main__":
	main()
```

no matter how large the file is — 1kb or 1gb — the hash is always 40 characters. that's the nature of sha-1. fixed-length output regardless of input size.

this is why git is so fast at figuring out what changed. it doesn't read and compare file contents line by line. it just compares hashes. same hash? nothing changed. different hash? something changed.

it's an elegant system. simple idea, powerful result.
