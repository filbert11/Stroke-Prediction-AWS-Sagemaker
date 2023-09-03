import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
import pandas as pd
import numpy as np
import xgboost as xgb
import re
import random

random.seed(10)

# Initialize XGB model
model = xgb.Booster()
model.load_model('xgboost-model')

api = "{your-token}"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

AGE, HYPERTENSION, HEART_DISEASE, EVER_MARRIED, HEIGHT, WEIGHT, GENDER, SMOKING, GLUCOSE = range(9)


# Define a function to handle the /start command
async def start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Stroke Prediction Bot! 🤖\n\n"
    "Simply answer the questions to the best of your knowledge and together we can work towards reducing your risk and promoting a healthier life! Send /cancel to end the conversation.\n\n"
    "Firstly, how old are you?")

    return AGE

async def handle_age(update: Update, context):
    age = int(update.message.text)
    context.user_data['age'] = age

    # Ask the user about their hypertension history with button options
    reply_keyboard = [["Yes", "No"]]
    await update.message.reply_text(
        "Do you have hypertension?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Do you have hypertension?'),
    )

    return HYPERTENSION

# Define a function to handle the user's hypertension history input
async def handle_hypertension(update: Update, context):
    hypertension = update.message.text.lower()

    # Check if the user has a history of hypertension
    if hypertension == 'yes':
        context.user_data['hypertension'] = 1
    else:
        context.user_data['hypertension'] = 0

    reply_keyboard = [["Yes", "No"]]
    await update.message.reply_text(
        "Do you have heart disease?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Do you have heart disease?'),
    )

    return HEART_DISEASE

async def handle_heart_disease(update: Update, context):
    heart_disease = update.message.text.lower()

    # Check if the user has a history of hypertension
    if heart_disease == 'yes':
        context.user_data['heart_disease'] = 1
    else:
        context.user_data['heart_disease'] = 0

    reply_keyboard = [["Yes", "No"]]
    await update.message.reply_text(
        "Were you ever married? (Trust me, this is one of the features)",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Were you ever married?'),
    )

    return EVER_MARRIED

async def handle_ever_married(update: Update, context):
    ever_married = update.message.text.lower()

    # Check if the user has a history of hypertension
    if ever_married == 'yes':
        context.user_data['ever_married'] = 1
    else:
        context.user_data['ever_married'] = 0

    await update.message.reply_text("What is your weight in kg?")

    return WEIGHT

async def handle_weight(update: Update, context):
    # Capture only digits
    pattern = '^(\d+\.?\d+).*$'
    weight = update.message.text
    if re.match(pattern,weight):
        context.user_data['weight'] = round(float(re.match(pattern, weight).group(1)))
    else:
        await update.message.reply_text("You have provided an invalid weight. Please input the weight in kg (e.g. 50).")
        return WEIGHT

    await update.message.reply_text("What is your height in metres?")
    return HEIGHT

async def handle_height(update: Update, context):
    height = update.message.text
    pattern = '^(\d+\.\d+).*$'
    # Validate height
    # Check if the input matches the pattern
    if re.match(pattern, height):
        height = float(re.match(pattern, height).group(1))
    else:
        await update.message.reply_text("You have provided an invalid height. Please input the height in metres (e.g. 1.53m).")
        return HEIGHT

    context.user_data['bmi'] =  context.user_data['weight'] / height ** 2

    text = f"Got it! With a height of {height}m and weight of {context.user_data['weight']}kg, your BMI is {round(context.user_data['bmi'],2)}."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    reply_keyboard = [["Female", "Male"]]
    await update.message.reply_text(
        "What is your gender?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='What is your gender?'),
    )

    return GENDER

async def handle_gender(update: Update, context):
    gender = update.message.text.lower()

    # Check if the user has a history of hypertension
    if gender == 'male':
        context.user_data['gender_Male'] = 1
    else:
        context.user_data['gender_Male'] = 0
      
    reply_keyboard = [["I order bubble tea with 0% sugar 🧋"],["I enjoy sugary treats once in a while 🍰"],["My entire diet is sugar 🍡🍪🍬🍧"]]
    await update.message.reply_text(
        "How much sugar do you consume?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='How much sugar do you consume?'),
    )

    return GLUCOSE

async def handle_glucose(update: Update, context):
    glucose = update.message.text

    if glucose == 'I order bubble tea with 0% sugar 🧋':
        context.user_data['avg_glucose_level'] = random.uniform(80,120)
    elif glucose == 'I enjoy sugary treats once in a while 🍰':
        context.user_data['avg_glucose_level'] = random.uniform(120,200)
    elif glucose == 'My entire diet is sugar 🍡🍪🍬🍧':
        context.user_data['avg_glucose_level'] = random.uniform(200,270)
    else:
        await update.message.reply_text("You have provided an invalid input. Please try again.")
        return GLUCOSE

    reply_keyboard = [["Formerly Smoked","Never Smoked","Smokes"]]
    await update.message.reply_text(
        "Lastly, are you a smoker?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Are you a smoker?'),
    )

    return SMOKING


async def handle_smoking(update: Update, context):
    smoking = update.message.text.lower()

    # Initialise as 0
    for col in ['smoking_status_formerly smoked','smoking_status_never smoked','smoking_status_smokes']:
        context.user_data[col] = 0

    # Assign
    if smoking == 'formerly smoked':
        context.user_data['smoking_status_formerly smoked'] = 1
    elif smoking == 'never smoked':
        context.user_data['smoking_status_never smoked'] = 1
    elif smoking == 'smokes':
        context.user_data['smoking_status_smokes'] = 1
    else:
        await update.message.reply_text("You have provided an invalid input. Please try again.")
        return SMOKING

    # Perform stroke prediction based on user data
    mock_user_data = {
        'age':context.user_data['age'],
        'hypertension':context.user_data['hypertension'],
        'heart_disease':context.user_data['heart_disease'],
        'ever_married':context.user_data['ever_married'],
        'avg_glucose_level':context.user_data['avg_glucose_level'],
        'bmi':context.user_data['bmi'],
        'gender_Male':context.user_data['gender_Male'],
        'work_type_Never_worked':0,
        'work_type_Private':1,
        'work_type_Self-employed':0,
        'Residence_type_Urban':1,
        'smoking_status_formerly smoked':context.user_data['smoking_status_formerly smoked'],
        'smoking_status_never smoked':context.user_data['smoking_status_never smoked'],
        'smoking_status_smokes':context.user_data['smoking_status_smokes']
    }

    # for debugging dict values
    #text = str(mock_user_data)
    #await context.bot.send_message(chat_id = update.effective_chat.id, text = text)

    # Convert data into DMatrix
    dtest = xgb.DMatrix(pd.DataFrame({k:[v] for k, v in mock_user_data.items()}))
    pred = model.predict(dtest)[0]
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=str(pred))
    if pred < 0.4:
        prediction_result = "Great news! Based on the information provided, you are currently <b>not at risk</b> for stroke! 🎉 Keep up the healthy habits!"
    else:
        prediction_result = "Unfortunately, based on the information provided, you are <b>at risk</b> of stroke. ☹️ Click <a href='https://www.healthhub.sg/programmes/130/strokehub'>here</a> to read more about how you can manage the risks.\n\n<i>Please note this is a prediction service and you should still speak to a doctor for a comprehensive assessment.</i>"
    # You can implement your stroke prediction logic here

    # Send the prediction result to the user
    #await update.message.reply_text(prediction_result,parse_mode='HTML')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=prediction_result, parse_mode='HTML'),
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Thank you for using the Stroke Prediction Bot.\nTo restart the chat, send /start. To end the chat, send /cancel.")
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="Based on the provided information, the stroke prediction result is: {}".format(new_age))
    
    return ConversationHandler.END

# Define a function to handle cancellation of the conversation
async def cancel(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation cancelled. Goodbye!")

    return ConversationHandler.END

def main() -> None:
    # Create an Application instance
    application = Application.builder().token(api).build()


    # Create a conversation handler with the states AGE and HYPERTENSION
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE: [MessageHandler(filters.Regex(r'^\d+$'), handle_age)],
            HYPERTENSION: [MessageHandler(filters.Regex(re.compile(r'^(yes|no)$',re.IGNORECASE)), handle_hypertension)],
            HEART_DISEASE: [MessageHandler(filters.Regex(re.compile(r'^(yes|no)$',re.IGNORECASE)), handle_heart_disease)],
            EVER_MARRIED: [MessageHandler(filters.Regex(re.compile(r'^(yes|no)$',re.IGNORECASE)), handle_ever_married)],
            WEIGHT: [MessageHandler(filters.Regex(r'^(\d+\.?\d+)?.*$'), handle_weight)],
            HEIGHT: [MessageHandler(filters.Regex(r'^(\d+\.\d+)?.*$'), handle_height)],
            GENDER: [MessageHandler(filters.Regex(re.compile(r'^(Female|Male)$',re.IGNORECASE)),handle_gender)],
            GLUCOSE: [MessageHandler(filters.ALL, handle_glucose)],
            SMOKING: [MessageHandler(filters.Regex(re.compile(r'^(Formerly Smoked|Never Smoked|Smokes)$',re.IGNORECASE)),handle_smoking)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add the conversation handler to the application
    application.add_handler(conv_handler)

    # Run the application
    application.run_polling()

if __name__ == '__main__':
    main()
