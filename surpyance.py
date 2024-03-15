import os

import cv2
import numpy as np
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if BOT_TOKEN is None:
    print("BOT_TOKEN environment variable do not exist.")
    print("Consider setting BOT_TOKEN variable in a .env file and do:")
    print("source .env")
    exit(1)
bot = telebot.TeleBot(BOT_TOKEN)

STOP_REGISTER = False

saved_person = {}

def brightness(image) -> float:
    '''
    Return a brightness value of an image
    :param image: image to calculate the brightness
    :return: float representing the brightness
    '''
    assert image.shape[2] == 3
    return float(np.average(np.linalg.norm(image, axis=2)) / np.sqrt(3))

def control_loop(threshold: float):
    '''
    Loop through the frames of the camera, calculate the brightness.
    If the brightness is greater than a threshold it means that someone have turned the lights on
    so exit from this function
    :param threshold: value to overcome for exit the control loop
    :return: None
    '''
    vid = cv2.VideoCapture(0)

    while True:
        ret, frame = vid.read()
        bright = brightness(frame)

        if bright > threshold:
            vid.release()
            cv2.destroyAllWindows()
            return

def register_and_save_video(output_name):
    '''
    Register and save a video of 15 seconds
    :param output_name: output file name
    :return: None
    '''
    fourcc = cv2.VideoWriter.fourcc(*"mp4v")
    out = cv2.VideoWriter(output_name, fourcc, 20.0, (640, 480))
    vid = cv2.VideoCapture(0)

    frame_ctr = 0

    while frame_ctr != (15 * 20 - 1):
        _, frame = vid.read()
        out.write(frame)

        frame_ctr += 1

    vid.release()
    out.release()
    cv2.destroyAllWindows()

@bot.message_handler(commands=['start'])
def register_person(message):
    '''
    Register and save a person's name and chat_id to send videos. This function STOP the polling, it means that
    the first person that write \\start, enter the control loop
    :param message: Message received
    :return: None
    '''
    global STOP_REGISTER

    if STOP_REGISTER:
        return

    STOP_REGISTER = True

    bot.reply_to(message, "Register user to update chat_id")
    if message.chat.id not in saved_person.keys():
        print(f"Saved this person {message.from_user.username} with this chat_id {message.chat.id}")
        saved_person[message.from_user.username] = message.chat.id

    bot.stop_polling()

def produce_video_series(video_to_register=8):
    '''
    Register and send 'video_to_register' videos to the chat
    :param video_to_register: How many video to regisiter
    :return: None
    '''
    video_registered = 0

    while video_registered < video_to_register:
        output_file_name = f"output_{video_registered}.mp4"
        register_and_save_video(output_file_name)

        with open(output_file_name, "rb") as f:
            bot.send_video(chat_id=list(saved_person.values())[0], video=f, supports_streaming=True)

        video_registered += 1

def main():
    if len(BOT_TOKEN) == 0:
        print("ERROR: Token key not found in environment")
        exit(1)
    
    print("Starting the bot...")

    while not STOP_REGISTER:
        bot.polling()

    while True:
        control_loop(threshold=100)
        print("Detected Light: Start recording...")
        produce_video_series()
        print("Finish recording")

main()
