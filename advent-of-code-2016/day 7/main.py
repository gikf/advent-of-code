"""Advent of Code 2016 Day 7."""
import re


def main(file_input='input.txt'):
    ips = [line.strip() for line in get_file_contents(file_input)]
    supports_tls = find_ips_supporting(ips, does_support_tls)
    print(f'Number IPs supporting TLS: {len(supports_tls)}')
    supports_ssl = find_ips_supporting(ips, does_support_ssl)
    print(f'Number IPs supporting SSL: {len(supports_ssl)}')


def find_ips_supporting(ips, support_check):
    """Find IPs fulfilling support_check function."""
    return [ip for ip in ips if support_check(ip)]


def does_support_tls(ip):
    """Check if IP supports TLS.

    Has abba sequence and no abba sequence inside the brackets.

    Examples:
    - abba[mnop]qrst supports TLS (abba outside square brackets).
    - abcd[bddb]xyyx does not support TLS (bddb is within square brackets,
        even though xyyx is outside square brackets).
    - aaaa[qwer]tyui does not support TLS (aaaa is invalid;
        the interior characters must be different).
    - ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets,
        even though it's within a larger string).
    """
    sequence = r'(\w)(\w)\2\1'
    sequence_inside_brackets = r'''\[
                                   [a-z]*
                                   (\w)(\w)\2\1
                                   [a-z]*
                                   \]'''
    has_sequence = re.search(sequence, ip)
    return (not re.search(sequence_inside_brackets, ip, re.VERBOSE)
            and has_sequence
            and len(set(has_sequence.group())) == 2)


def does_support_ssl(ip):
    """Check if IP supports SSL.

    Has aba sequence outside of the bracketed sections and corresponding
    bab sequence inside bracketed section.

    Examples:
    - aba[bab]xyz supports SSL (aba outside square brackets with
        corresponding bab within square brackets).
    - xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    - aaa[kek]eke supports SSL (eke in supernet with corresponding kek in
        hypernet; the aaa sequence is not related, because the interior
        character must be different).
    - zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has
        a corresponding bzb, even though zaz and zbz overlap).
    """
    regex = r'''(\w)(\w)\1              # aba sequence
                [a-z]*                  # separating characters
                (\[[a-z]+\][a-z]+)*     # zero or more bracketed sections
                                        # followed by characters
                \[[a-z]*\2\1\2[a-z]*\]  # bracketed bab
                '''
    regex2 = r'''\[[a-z]*(\w)(\w)\1[a-z]*\]  # bracketed aba
                 ([a-z]+\[[a-z]+\])*         # zero or more bracketed sections
                 [a-z]*                      # separating characters
                 \2\1\2                      # bab sequence
                 '''
    has_sequence = (re.search(regex, ip, re.VERBOSE)
                    or re.search(regex2, ip, re.VERBOSE))
    if has_sequence:
        return has_sequence.group(1) != has_sequence.group(2)
    return False


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
