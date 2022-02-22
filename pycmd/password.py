# -*- coding: utf-8 -*-
# usage: password [-h] [--num NUM] [--no-upper NO-UPPER] [--no-spec NO-SPEC] [--spec-chars SPEC-CHARS]
import argparse
import pyperclip
import secrets
import string

parser = argparse.ArgumentParser(
    prog='password', description='Password generator')
parser.add_argument('-n', '--num', type=int, default=16, help='password length')
parser.add_argument('--no-upper', action='store_true', help='no uppercase')
parser.add_argument('--no-spec', action='store_true', help='no special chars')
parser.add_argument('--spec-chars', type=str, default="!@#$%^&*", help="special chars")
args = parser.parse_args()


def main():
    chars = string.digits + string.ascii_lowercase
    if not args.no_upper:
        chars += string.ascii_uppercase
    if not args.no_spec:
        chars += args.spec_chars

    while True:
        text = "".join(secrets.choice(chars) for _ in range(args.num))
        # at least 1 digit
        cond_digit = bool(set(text) & set(string.digits))
        # at least 1 lowercase
        cond_lower = bool(set(text) & set(string.ascii_lowercase))
        # at least 1 uppercase if no-upper=False, otherwise, not any none
        cond_upper = bool(not args.no_upper) == bool(set(text) & set(string.ascii_uppercase))
        # at least 1 spec-char if no-spec=False, otherwise, not any none
        cond_spec = bool(not args.no_spec) == bool(set(text) & set(args.spec_chars))
        if all([cond_digit, cond_lower, cond_upper, cond_spec]):
            break
    pyperclip.copy(text)
    print(f"{text}\n\n☕️ Alreay copied, just paste it.")


if __name__ == "__main__":
    main()
