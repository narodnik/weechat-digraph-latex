# Weechat Digraph Plugin

Digraphs like nvim for inputting math symbols

Drop this in `.local/share/weechat/python/autoload/`

```bash
cd /tmp/
git clone https://github.com/narodnik/weechat-digraph-latex/
cp weechat-digraph-latex/digraph.py ~/.local/share/weechat/python/autoload/
```

# Example Usage

If you paste this line below, it will replace everything between the `$` signs with
the unicode math symbols.

```
> hello here is a formula $ZZ^2 in a: ** <= 123$ says hello $FF TE$
```

# Available Symbols

All latin + numeric superscript works except 'q' (which doesn't exist).

```
^2 -> ²
^a -> ᵃ
```

All greek letters are supported. Use 'X*' where X is a letter of the alphabet.

```
g* -> γ
a* -> α
```

Here is a list of the remaining symbols:

```
ZZ      ℤ
QQ      ℚ
FF      𝔽
a:      𝔞
b:      𝔟
c:      𝔠
p:      𝔭
in      ∈
ni      ∉
(_      ⊆
(<      ⊊
(!      ⊈
:.      ·
.,      …
.3      ⋯
**      ×
i8      ∞
</      ⟨
/>      ⟩
ff      ϕ
=>      ⇒
==      ⇔
->      →
TE      ∃
!=      ≠
=3      ≡
=<      ≤
<=      ≤
>=      ≥
=?      ≌
RT      √
(U      ∩
```

