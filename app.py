from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired
from pymongo import MongoClient, errors
from pymongo.errors import ConnectionFailure

app = Flask(__name__)
app.secret_key = 'your_secret_key'

MONGO_URI = 'mongodb+srv://vrentmanuel:surveyproject@survey.eqiduny.mongodb.net/survey'

try: 
    client = MongoClient(MONGO_URI)
    db = client['survey']
    collection = db['survey']

    client.server_info()  # This will raise an exception if not connected

    print("Successfully connected to MongoDB.")

except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")

# Define a simple form using WTForms
class SurveyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    level = RadioField('Level of Education', choices=[
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year')
        ], validators=[DataRequired()])
    question = RadioField('1.) Participation in extracurricular activities positvely impacts my overall well-being.', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question2 = RadioField('2.) Extracurricular activites help me manage stress effectively.', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question3 = RadioField('3.) Participating in extracurricular activities has improved my time management skills.', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question4 = RadioField('4.) Extracurricular activities motivate me to peform better academically.', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question5 = RadioField('5.) I have made new friends through my involvement in extracurricular activities.', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question6 = RadioField('6.) Participating in extracurricular activities has boosted my self-confidence.', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question7 = RadioField('7.) Extracurricular activities have positively impacted my physical health (e.g., through exercise, outdoor activities).', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question8 = RadioField('8.) Balancing academics and extracurricular activities is manageable for me.', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question9 = RadioField('9.) Participating in extracurricular activities has strengthened my sense of belonging within the school community. ', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    question10 = RadioField('10.) Overall, participating in extracurricular activities has contributed significantly to my personal growth and development.', choices=[
        ('strongly_agree', 'Strongly Agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree')
    ], validators=[DataRequired()])
    feedback = StringField('Feedback')
    submit = SubmitField('Submit')

# Route for survey form
@app.route('/', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        try:
            # Store form data in MongoDB
            response = {
                'name': form.name.data,
                'email': form.email.data,
                'level': form.level.data,
                'question': form.question.data,
                'question2': form.question2.data,
                'question3': form.question3.data,
                'question4': form.question4.data,
                'question5': form.question5.data,
                'question6': form.question6.data,
                'question7': form.question7.data,
                'question8': form.question8.data,
                'question9': form.question9.data,
                'question10': form.question10.data,
                'feedback': form.feedback.data
            }
            result = collection.insert_one(response)

            flash('Your response has been recorded. Thank you!')
            return redirect(url_for('thank_you'))

        except errors.PyMongoError as e:
            flash(f'Error while storing data in MongoDB: {str(e)}')
            print(f'Error while storing data in MongoDB: {str(e)}')

    return render_template('survey.html', form=form)

# Route for thank you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

def test_mongodb():
    try:
        # Perform a basic operation to test MongoDB connection
        result = collection.find_one()
        if result:
            return f"Successfully connected to MongoDB: {result}"
        else:
            return "Connected to MongoDB, but no documents found."
    except errors.PyMongoError as e:
        return f"Failed to connect to MongoDB: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=8000)