#GET

def get_api_key_for_user():
    with open('api_key_for_user.txt','r',encoding='utf-8') as f:
        key = f.read()
        return key

def get_admin_id():
    with open('admin_id.txt', 'r', encoding='utf-8') as f:
        admin_id = f.read().strip()
        return admin_id



def get_text():
    with open('start_text.txt', 'r', encoding='utf-8') as f:
        return f.read()


