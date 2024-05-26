import logging

logging.basicConfig(level=logging.INFO)

def main():
    
    from handlers import bot
    while True:
        try:
            bot.run_forever()
        except KeyError:
            continue

if __name__ == "__main__":
    main()