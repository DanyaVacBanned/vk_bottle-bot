import logging

logging.basicConfig(level=logging.INFO)

def main():
    
    from handlers import bot 
    bot.run_forever()

if __name__ == "__main__":
    main()