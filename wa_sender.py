import argparse
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


with open('message.txt', 'r') as message_file:
    MESSAGE = message_file.readline()

with open('image.txt', 'r') as image_file:
    IMAGE = image_file.readline()
FILE_WITH_PHONES = 'test.txt'


def extract_phones_from_backup():
    fname = input("Enter the name of backup file: ")
    phones = set()
    with open(fname, 'r') as f:
        for line in f.readlines():
            if "joined using this group's invite link" in line:
                subline = line.split(':')[3].split('joined')[0].replace('+', '')
                phone = ''.join(filter(str.isdigit, subline))
                phones.add(phone)
    with open('links_' + fname, 'w') as fo:
        for p in phones:
            if p == '':
                continue
            fo.write('https://wa.me/' + p + '\n')

    with open('phones_' + fname, 'w') as fp:
        for p in phones:
            if p == '':
                continue
            fp.write(p + '\n')

def send_message():
    count_of_sended = 0
    count_of_skipped = 0
    browser = webdriver.Chrome()
    browser.get(f'https://web.whatsapp.com')
    sleep(5)
    input('Scan QR code and press RETURN: ')
    sleep(5)
    print('WhatsApp authorization passed.')
    with open(FILE_WITH_PHONES, 'r') as f:
        for line in f.readlines():
            phone = line.strip()
            if phone == '':
                continue
            try:
                browser.get(f'https://wa.me/{phone}')
                browser.find_element(
                    By.XPATH,
                    '/html/body/div[1]/div[1]/div[2]/div/section/div/div/div/div[2]/div[1]/a'
                ).click()
                sleep(3)
                browser.find_element(
                    By.XPATH,
                    '/html/body/div[1]/div[1]/div[2]/div/section/div/div/div/div[3]/div/div/h4[2]/a'
                ).click()
                print('first click')
                sleep(3)
                message_input = browser.find_element(
                    By.XPATH,
                    '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
                )
                message_input.send_keys(MESSAGE + Keys.RETURN)
                print('typing message ...')
                sleep(3)
                attach_button = browser.find_element(
                    By.XPATH,
                    '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
                ).click()
                sleep(3)
                image_input = browser.find_element(
                    By.XPATH,
                    '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'
                )
                image_input.send_keys(IMAGE)
                print('choosing image ...')
                sleep(3)
                send_button = browser.find_element(
                    By.XPATH,
                    '/html/body/div[1]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span'
                ).click()
                print('sending message ...')
                sleep(5)
                print(f'+ Message sended: {phone}')
                count_of_sended += 1
            except Exception as err:
                # print(f"Unexpected {err=}, {type(err)=}, {err}")
                print(f'- Cannot send message: {phone}')
                count_of_skipped += 1
            sleep(5)
    print(
        f'\n{count_of_sended} phones successful\n'
        f'{count_of_skipped} phones skipped\n'
    )
    browser.quit()

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
    
    if args.mode == 2:
        send_message()

if __name__ == '__main__':
    main()
