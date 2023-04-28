import argparse
from time import sleep

def extract_phones_from_backup():
    fname = input("Enter the name of backup file: ")
    phones = set()
    with open(fname, 'r') as f:
        for line in f.readlines():
            if "joined using this group's invite link" in line:
                subline = line.split(':')[3].split('joined')[0].replace('+', '')
                phone = ''.join(filter(str.isdigit, subline))
                phones.add(phone)
                print(phones)
    with open('whatsapp_links_for_' + fname, 'w') as fo:
        for p in phones:
            fo.write('https://wa.me/' + p + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="store_true"
    )
    parser.add_argument(
        "mode",
        help="1 - for extracting phones from chat backup,\
            2 - for sending messages",
        type=int
    )
    args = parser.parse_args()
    
    if args.mode == 1:
        extract_phones_from_backup()

if __name__ == '__main__':
    main()
