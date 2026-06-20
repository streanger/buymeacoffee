import sys
from pathlib import Path
import qrcode  # pip install qrcode[pil]

def make_qr(filename, text):
    possible_directories = ['qrcodes', '../qrcodes']
    for directory in possible_directories:
        directory = Path(directory)
        if directory.exists():
            path = directory / filename
            img = qrcode.make(text)
            img.save(path)
            print(f'[*] saved to: {path}')
            return True
    print(f'[!] `qrcodes` directory not found')
    return False

def replace_addresses(data):
    possible_paths = ['index.html', '../index.html']
    for path in possible_paths:
        path = Path(path)
        if path.exists():
            text = path.read_text(encoding='utf-8')
            break
    else:
        print(f'[!] `index.html` not found')
        return False

    # replace
    modified = text
    PATTERN_LEFT = '">'
    PATTERN_RIGHT = '</div>'
    for (_, marker, address) in data:
        marker_pos = modified.find(marker)
        if marker_pos == -1:
            print(f'[!] marker `{marker}` not found')
            sys.exit()
        div_start = modified.rfind(PATTERN_LEFT, 0, marker_pos)
        div_end = modified.find(PATTERN_RIGHT, div_start)
        if div_start == -1 or div_end == -1:
            print(f'[!] some of divs not found: {div_start=}, {div_end=}')
            sys.exit()
        value_start = div_start + 2
        modified = modified[:value_start] + address + modified[div_end:]

    # update index.html
    path.write_text(modified)
    print(f'[*] file modified: {path}')
    return True

def main():
    data = [
        # qr-filename, marker-for-html, wallet-address
        ('monero-wallet.png', '<!-- MONERO-MARKER -->', '86mV36EuLyo6c6iGEbV6m17W2czLHnTFd7J7snMFK9sfcwaZEave2oyPaHNVyPjBrH9hb3e7zmxiRACfNqbMP22n76TT3rB'),
        ('bitcoin-wallet.png', '<!-- BITCOIN-MARKER -->', 'bc1qw2076vyumsf8qr7d034ulejqtu6m7kftr2npas'),
        ('litecoin-wallet.png', '<!-- LITECOIN-MARKER -->', 'ltc1q2trat7qp8s6lfk993zj4ax85w3mku847z28vja'),
    ]
    # create qr-codes
    for (filename, _, address) in data:
        make_qr(filename, address)

    # replace addresses in html file
    replace_addresses(data)

if __name__ == "__main__":
    main()
