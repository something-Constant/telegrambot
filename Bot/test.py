# def show(func):
#     def wraper(*args):
#         print(f"number: {args[0]}")
#         # print(f"total: {func(args[0])}")

#         return func(args[0])

#     return wraper


# # @show
# def cal(num):
#     tot = 1

#     for i in range(1, num + 1):
#         tot *= i

#     return tot


# # cal(20)
# # print(cal(20))

# t = show(cal(20))

# print(t)


# https://api.telegram.org/bot7058704613:AAEuFunpv6m3jogUOXFR-0rEBrYmuQkxQh0/Update
# E:\>wget -O answer.html "https://api.telegram.org/bot7058704613:AAEuFunpv6m3jogUOXFR-0rEBrYmuQkxQh0/sendMessage?chat_id=442200351&text=hello
# E:\>wget -O answer.html "https://api.telegram.org/bot7058704613:AAEuFunpv6m3jogUOXFR-0rEBrYmuQkxQh0/sendPhoto?chat_id=442200351&photo="AgACAgQAAxkBAAIBtmmFM0GnrMuKfTP7aA14-Y65IdfvAAJUDWsb8hUpUPROq0x3kmxWAQADAgADeAADOAQ"
# wget -O answer.html "https://api.telegram.org/bot7058704613:AAEuFunpv6m3jogUOXFR-0rEBrYmuQkxQh0/sendPhoto?chat_id=442200351&photo="364399"


# wget -O answer.html https://api.telegram.org/bot6177409581:AAFQY7O1wL1i345JnUEs-yYSmZtRD6rx3Qk/Update


# def generate_keyboard(row=2, arge: dict = {}):

#     print(arge)
#     for key in arge:
#         print(f"{key}")
#         print(f"{arge[key]}")

#     print(row)


# # items = ["Back", "Start", "Cancel"]
# items = {"Back": "1", "Start": "2", "Cancel": "3"}

# # print(items)

# # for key in items:
# #     print(f"item_{key}")
# #     print(f"item_{items[key]}")


# def generate_keyboard(size=2, keys: dict = {}):
#     build = InlineKeyboardBuilder()

#     for item in keys:
#         build.button(text=item, callback_data=f"{keys[item]}")

#     build.adjust(size)

#     return build.as_markup()


# # generate_keyboard(50, items)

# t = ["ℹ️ About", "📌 Help", "📊 Stats", "⚙️ Settings"]
# keyboard_item = ["🧾 Report", "📌 Help", "📊 Stats", "⚙️ Settings"]

# # t["0"]

# print(t[0])
print("id: @startswith".strip()["id: @startswith".strip().find("@"):])
